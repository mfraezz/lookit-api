import uuid

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify
from kombu.utils import cached_property

from accounts.models import Child, DemographicData, Organization, User
from accounts.utils import build_study_group_name
from guardian.shortcuts import assign_perm, get_groups_with_perms
from project.fields.datetime_aware_jsonfield import DateTimeAwareJSONField
from transitions.extensions import GraphMachine as Machine

from . import workflow


class Study(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    name = models.CharField(max_length=255, blank=False, null=False)
    date_modified = models.DateTimeField(auto_now=True)
    short_description = models.TextField()
    long_description = models.TextField()
    criteria = models.TextField()
    duration = models.TextField()
    contact_info = models.TextField()
    max_age = models.TextField(default='')
    min_age = models.TextField(default='')
    image = models.ImageField(null=True, upload_to='study_images/')
    comments = models.TextField(blank=True, null=True)
    organization = models.ForeignKey(
        Organization,
        on_delete=models.DO_NOTHING,
        related_name='studies',
        related_query_name='study'
    )
    structure = DateTimeAwareJSONField(default=dict)
    display_full_screen = models.BooleanField(default=True)
    exit_url = models.URLField(default='https://lookit.mit.edu/')
    state = models.CharField(
        choices=workflow.STATE_CHOICES,
        max_length=25,
        default=workflow.STATE_CHOICES.created,
        db_index=True
    )
    public = models.BooleanField(default=False)
    creator = models.ForeignKey(User)

    def __init__(self, *args, **kwargs):
        super(Study, self).__init__(*args, **kwargs)
        self.machine = Machine(
            self,
            states=workflow.states,
            transitions=workflow.transitions,
            initial=self.state,
            send_event=True,
            before_state_change='check_permission',
            after_state_change='_finalize_state_change'
        )

    def __str__(self):
        return f'<Study: {self.name}>'

    class Meta:
        permissions = (
            ('can_view_study', 'Can View Study'),
            ('can_create_study', 'Can Create Study'),
            ('can_edit_study', 'Can Edit Study'),
            ('can_remove_study', 'Can Remove Study'),
            ('can_activate_study', 'Can Activate Study'),
            ('can_deactivate_study', 'Can Deactivate Study'),
            ('can_pause_study', 'Can Pause Study'),
            ('can_resume_study', 'Can Resume Study'),
            ('can_approve_study', 'Can Approve Study'),
            ('can_submit_study', 'Can Submit Study'),
            ('can_retract_study', 'Can Retract Study'),
            ('can_resubmit_study', 'Can Resubmit Study'),
            ('can_edit_study_permissions', 'Can Edit Study Permissions'),
            ('can_view_study_permissions', 'Can View Study Permissions'),
            ('can_view_study_responses', 'Can View Study Responses'),
            ('can_view_study_video_responses', 'Can View Study Video Responses'),
            ('can_view_study_demographics', 'Can View Study Demographics'),
        )

    @cached_property
    def begin_date(self):
        try:
            return self.logs.filter(action='active').first().created_at
        except AttributeError:
            return None

    @property
    def end_date(self):
        if not self.begin_date:
            return None
        try:
            end_date = self.logs.filter(action='deactivate').first().created_at
        except AttributeError:
            return None
        else:
            return end_date if end_date > begin_date else None

    @property
    def study_admin_group(self):
        ''' Fetches the study admin group '''
        groups = get_groups_with_perms(self)
        for group in groups:
            if 'STUDY' in group.name and 'ADMIN' in group.name:
                return group
        return None

    @property
    def study_read_group(self):
        ''' Fetches the study read group '''
        groups = get_groups_with_perms(self)
        for group in groups:
            if 'STUDY' in group.name and 'READ' in group.name:
                return group
        return None

    # @property
    # def completed_responses_count(self):
    #     return self.responses.filter(completed=True).count()
    #
    # @property
    # def incomplete_responses_count(self):
    #     return self.responses.filter(completed=False).count()

    # WORKFLOW CALLBACKS
    def check_permission(self, ev):
        user = ev.kwargs.get('user')
        if user.is_superuser:
            return
        raise

    def clone(self):
        ''' Create a new, unsaved copy of this study. '''
        copy = self.__class__.objects.get(pk=self.pk)
        copy.id = None
        copy.public = False
        copy.state = 'created'
        copy.name = 'Copy of ' + copy.name

        # empty the fks
        fk_field_names = [f.name for f in self._meta.model._meta.get_fields() if isinstance(f, (models.ForeignKey))]
        for field_name in fk_field_names:
            setattr(copy, field_name, None)
        try:
            copy.uuid = uuid.uuid4()
        except AttributeError:
            pass
        return copy

    def notify_administrators_of_submission(self, ev):
        # TODO
        pass

    def notify_submitter_of_approval(self, ev):
        # TODO
        pass

    def notify_submitter_of_rejection(self, ev):
        # TODO
        pass

    def notify_administrators_of_retraction(self, ev):
        # TODO
        pass

    def notify_administrators_of_activation(self, ev):
        # TODO
        pass

    def notify_administrators_of_pause(self, ev):
        # TODO
        pass

    def notify_administrators_of_deactivation(self, ev):
        # TODO
        pass

    # Runs for every transition to log action
    def _log_action(self, ev):
        StudyLog.objects.create(
            action=ev.state.name,
            study=ev.model,
            user=ev.kwargs.get('user')
        )

    # Runs for every transition to save state and log action
    def _finalize_state_change(self, ev):
        ev.model.save()
        self._log_action(ev)

# TODO Need a post_save hook for edit that pulls studies out of approved state
# TODO or disallows editing in pre_save if they are approved


@receiver(post_save, sender=Study)
def add_study_created_log(sender, instance, created, **kwargs):
    if created:
        StudyLog.objects.create(
            action='created',
            study=instance,
            user=instance.creator
        )


@receiver(post_save, sender=Study)
def study_post_save(sender, **kwargs):
    '''
    Add study permissions to organization groups and
    create groups for all newly created Study instances. We only
    run on study creation to avoid having to check for existence
    on each call to Study.save.
    '''
    study, created = kwargs['instance'], kwargs['created']
    if created:
        from django.contrib.auth.models import Group

        organization_groups = Group.objects.filter(
            name__startswith=f'{slugify(study.organization.name)}_ORG_'.upper()
        )
        # assign study permissions to organization groups
        for group in organization_groups:
            for perm, _ in Study._meta.permissions:
                if 'ADMIN' in group.name:
                    assign_perm(perm, group, obj=study)
                elif 'READ' in group.name and 'view' in perm:
                    assign_perm(perm, group, obj=study)

        # create study groups and assign permissions
        for group in ['read', 'admin']:
            study_group_instance = Group.objects.create(
                name=build_study_group_name(study.organization.name, study.name, study.pk, group)
            )
            for perm, _ in Study._meta.permissions:
                # add only view permissions to non-admin
                if group == 'read' and perm != 'can_view_study':
                    continue
                if 'approve' not in perm:
                    assign_perm(perm, study_group_instance, obj=study)


class Response(models.Model):
    study = models.ForeignKey(
        Study, on_delete=models.DO_NOTHING,
        related_name='responses'
    )
    completed = models.BooleanField(default=False)
    exp_data = DateTimeAwareJSONField(default=dict)
    conditions = DateTimeAwareJSONField(default=dict)
    sequence = ArrayField(models.CharField(max_length=128), blank=True, default=list)
    global_event_timings = DateTimeAwareJSONField(default=dict)
    child = models.ForeignKey(Child, on_delete=models.DO_NOTHING)
    demographic_snapshot = models.ForeignKey(
        DemographicData,
        on_delete=models.DO_NOTHING
    )

    def __str__(self):
        return f'<Response: {self.study} {self.child.user.get_short_name}>'

    class Meta:
        permissions = (
            ('view_response', 'View Response'),
        )


class Log(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f'<{self.__class__.name}: {self.action} @ {self.created_at:%c}>'

    class Meta:
        abstract = True


class StudyLog(Log):
    action = models.CharField(max_length=128, db_index=True)
    study = models.ForeignKey(
        Study,
        on_delete=models.DO_NOTHING,
        related_name='logs',
        related_query_name='logs'
    )

    def __str__(self):
        return f'<StudyLog: {self.action} on {self.study.name} at {self.created_at} by {self.user.username}'  # noqa

    class Meta:
        index_together = (
            ('study', 'action')
        )


class ResponseLog(Log):
    action = models.CharField(max_length=128, db_index=True)
    response = models.ForeignKey(Response, on_delete=models.DO_NOTHING)

    class Meta:
        index_together = (
            ('response', 'action')
        )

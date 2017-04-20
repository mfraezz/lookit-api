from django import forms

from accounts.models import User
from guardian.shortcuts import assign_perm, get_objects_for_user, remove_perm
from studies.models import Study


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = ('password', )


class UserStudiesForm(forms.Form):
    template = 'accounts/collaborator_form.html'
    user = forms.ModelChoiceField(User.objects.all(), required=True, label='Collaborator')
    studies = forms.ModelMultipleChoiceField(Study.objects.all(), required=True, label='Assigned Studies')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('instance')
        super(UserStudiesForm, self).__init__(*args, **kwargs)

    def is_valid(self):
        valid = super(UserStudiesForm, self).is_valid()
        if valid and len(self.data['studies']) > 0:
            return True

    def save(self):
        permissions = ['studies.view_study', 'studies.edit_study']
        current_permitted_objects = get_objects_for_user(self.cleaned_data['user'], permissions)
        disallowed_studies = current_permitted_objects.exclude(id__in=[x.id for x in self.cleaned_data['studies']])

        for perm in permissions:
            for study in self.cleaned_data['studies']:
                assign_perm(perm, self.cleaned_data['user'], study)
            for study in disallowed_studies:
                remove_perm(perm, self.cleaned_data['user'], study)
        return self.cleaned_data['user']
{% extends 'exp/base.html' %}

{% block title %}{{ study.name }}{% endblock %}
{% block content %}
    <h1>{{ user.username }}</h1>
    <table>
      <tbody>
        <tr>
          <th>
            Given Name
          </th>
          <td>
            {{ user.given_name }}
          </td>
        </tr>
        <tr>
          <th>
            Middle Name
          </th>
          <td>
            {{ user.middle_name }}
          </td>
        </tr>
        <tr>
          <th>
            Family Name
          </th>
          <td>
            {{ user.family_name }}
          </td>
        </tr>
        <tr>
          <th>
            Studies
          </th>
          <td>
            {% for study in user.studies %}
              {{ study.name }},
            {% endfor %}
          </td>
        </tr>
      </tbody>
    </table>
    <form action="" method="POST">{% csrf_token %}
      {% if user.is_active %}
        <input type="hidden" name="disable" />
        <input type="submit" value="Disable User" onclick="return confirm('Are you sure?');"/>
      {% else %}
        <input type="hidden" name="enable" />
        <input type="submit" value="Enable User" onclick="return confirm('Are you sure?');"/>
      {% endif %}
    </form>
{% endblock %}

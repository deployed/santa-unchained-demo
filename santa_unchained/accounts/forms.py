from django import forms
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from santa_unchained.constants import Role


class GroupAdminForm(forms.ModelForm):
    name = forms.ChoiceField(choices=Role.choices, label=_("Name"))

    class Meta:
        model = Group
        exclude = ()

from django import forms
from django.contrib.auth.models import Group, User

from justchat.models import Chat

class OtherModelsForm(forms.ModelForm):
    user_groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.none(),
        widget=forms.CheckboxSelectMultiple(),
        required=False
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(OtherModelsForm, self).__init__(*args, **kwargs)
        if user is not None:
            self.fields['user_groups'].queryset = Group.objects.filter(user=user)

        if self.instance.pk:
            self.fields['user_groups'].initial = self.instance.usergroup.all()

    class Meta:
        model = Chat
        fields = ['user_groups']

    LANGUAGES = (
        ('Finnish', 'Suomi'),
        ('Swedish', 'Ruotsi'),
        ('English', 'Englanti'),
        ('German', 'Saksa'),
        ('Estonia', 'Viro'),
        ('Hungary', 'Unkari'),
        ('Norwegian', 'Norja'),
        ('Polish', 'Puola'),
    )
    translatelanguage = forms.ChoiceField(
        choices=LANGUAGES,
        widget=forms.Select(
            attrs={"style": "width: 8em;"}
        ),
    )

from django import forms

from main_app.models import ProfileCard, Card


class CardUpdateForm(forms.ModelForm):
    """Card form update"""

    class Meta:
        model = ProfileCard
        fields = ('first_name', 'last_name', 'email', 'phone',)


class CardCreateForm(forms.ModelForm):
    """Card create form"""

    class Meta:
        model = Card
        fields = ('series', 'end_activity')

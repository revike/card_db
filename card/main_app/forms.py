from django import forms
from django.core.validators import RegexValidator

from main_app.models import ProfileCard, Card


class CardUpdateForm(forms.ModelForm):
    """Card form update"""

    class Meta:
        model = ProfileCard
        fields = ('first_name', 'last_name', 'email', 'phone',)


class CardCreateForm(forms.ModelForm):
    """Card create form"""

    # series_valid = RegexValidator(regex='^\d{4}$')
    score = forms.IntegerField(min_value=1)
    # series = forms.IntegerField(
    #     validators=[series_valid], error_messages={
    #         "invalid": 'Серия состоит из 4х цифр и начинается с 1000'
    #     })

    class Meta:
        model = Card
        fields = ('term', 'score',)

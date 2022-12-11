from django import forms

from main_app.models import ProfileCard, Card


class CardUpdateForm(forms.ModelForm):
    """Card form update"""

    class Meta:
        model = ProfileCard
        fields = ('first_name', 'last_name', 'email', 'phone',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
            field.label = ''
        self.fields['first_name'].widget.attrs['placeholder'] = 'Имя'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Фамилия'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['phone'].widget.attrs['placeholder'] = 'Телефон'


class CardCreateForm(forms.ModelForm):
    """Card create form"""
    score = forms.IntegerField(min_value=1)

    class Meta:
        model = Card
        fields = ('term', 'score',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
            field.label = ''
        self.fields['score'].widget.attrs['placeholder'] = 'Количество'

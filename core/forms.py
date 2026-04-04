from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].label = 'Логін'
        self.fields['email'].label = 'Електронна пошта'
        self.fields['password1'].label = 'Пароль'
        self.fields['password2'].label = 'Підтвердження пароля'

        self.fields['username'].widget.attrs.update({
            'placeholder': 'Введіть логін'
        })
        self.fields['email'].widget.attrs.update({
            'placeholder': 'Введіть email'
        })
        self.fields['password1'].widget.attrs.update({
            'placeholder': 'Введіть пароль'
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Повторіть пароль'
        })

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('Користувач з такою поштою вже існує.')

        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email'].strip().lower()

        if commit:
            user.save()

        return user
from django import forms
from django.forms import ModelForm
from django.contrib.auth import get_user_model
from django.forms.widgets import PasswordInput, EmailInput

User = get_user_model()

class UserForm(ModelForm):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=PasswordInput)
    confirm_password=forms.CharField(widget=PasswordInput, label="Confirm Password")
    email = forms.CharField(widget=EmailInput)
    first_name = forms.CharField(max_length=100, label="First Name")
    last_name = forms.CharField(max_length=100, label="Last Name")

    class Meta:
        model = User
        fields = ["username", "password", "confirm_password", "first_name", "last_name", "email"]

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "Passwords do not match!"
            )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
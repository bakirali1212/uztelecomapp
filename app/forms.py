# users/forms.py
from django import forms
from .models import User

class UserCreationForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("username", "phone", "email")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])  # parol hash qilinadi
        if commit:
            user.save()
        return user

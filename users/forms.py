from django import forms
from users.models import CustomUser

class RegistrationForm(forms.ModelForm):

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class':'form-control'})
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class':'form-control'})
    )

    class Meta:
        model = CustomUser
        fields = ['username','email','password','confirm_password']

        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.EmailInput(attrs={'class':'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        pw = cleaned_data.get('password')
        cpw = cleaned_data.get('confirm_password')

        if pw != cpw:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data


class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            "class": "form-input",
            "placeholder": "Enter your email"
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "form-input",
            "placeholder": "Enter your password"
        })
    )
from django import forms
from django.forms.fields import EmailField
from . import models


class LoginForm(forms.Form):  # Form에는 save method가 없다.

    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Email"}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "password"})
    )  # widget은 부가적인 형식들을

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        try:
            user = models.User.objects.get(email=email)
            if user.check_password(
                password
            ):  # Returns True if the given raw string is the correct password for the user. (This takes care of the password hashing in making the comparison.)
                return self.cleaned_data
            else:
                self.add_error("password", forms.ValidationError("Password is wrong"))
        except models.User.DoesNotExist:
            self.add_error("email", forms.ValidationError("user does not exist"))
            # add_error는 특정 필드의 form 형태에 에러를 나타나게하는 함수


class SignUpForm(forms.ModelForm):  # ModelForm은 save method가 있다.
    class Meta:
        model = models.User
        fields = ("first_name", "last_name", "email")
        widgets = {
            "first_name": forms.TextInput(attrs={"placeholder": "First name"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Last name"}),
            "email": forms.EmailInput(attrs={"placeholder": "Email"}),
        }

    # user가 password는 갖고 있지 않으므로, 아래처럼 password 부분은 만들어놓는다.
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Password"})
    )
    confirm_pw = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password"})
    )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            if models.User.objects.get(email=email):
                raise forms.ValidationError("That email is already taken", code="user")
        except models.User.DoesNotExist:
            return email

    def clean_confirm_pw(self):
        password = self.cleaned_data.get("password")
        confirm_pw = self.cleaned_data.get("confirm_pw")
        if password != confirm_pw:
            raise forms.ValidationError("password not matched")
        else:
            return password

    # make for username and password
    def save(self):
        user = super().save(commit=False)
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        user.username = email
        user.set_password(password)
        user.save()

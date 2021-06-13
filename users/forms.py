from django import forms
from django.forms.fields import EmailField
from . import models


class LoginForm(forms.Form):  # Form에는 save method가 없다.

    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        try:
            user = models.User.objects.get(email=email)
            if user.check_password(password):
                return self.cleaned_data
            else:
                self.add_error("password", forms.ValidationError("Password is wrong"))
        except models.User.DoesNotExist:
            self.add_error("email", forms.ValidationError("user does not exist"))


# add_error는 특정 필드에 에러를 넣는 함수


class SignUpForm(forms.ModelForm):  # ModelForm은 save method가 있다.
    class Meta:
        model = models.User
        fields = ("first_name", "last_name", "email")

    # user가 password는 갖고 있지 않으므로, 아래처럼 password 부분은 만들어놓는다.
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_pw = forms.CharField(widget=forms.PasswordInput, label="Confirm password")

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

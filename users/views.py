from django.views.generic.edit import UpdateView
from users import models
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.views.generic import FormView, DetailView
from . import forms

# Create your views here.


class LoginView(FormView):

    template_name = "users/login.html"
    form_class = forms.LoginForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)


def log_out(request):
    logout(request)
    return redirect(reverse("core:home"))


class SignUpView(FormView):
    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)

    # form_valid 를 쓰기 전에 일련의 과정들이 override 되어서
    # super().form_valid 해주는거


class UserProfileView(DetailView):
    model = models.User
    context_object_name = "user_obj"


class UserUpdateView(UpdateView):
    model = models.User
    template_name = "users/update-profile.html"
    fields = (
        "first_name",
        "last_name",
        "avatar",
        "gender",
        "bio",
        "birthday",
        "language",
        "currency",
    )

    def get_object(self, queryset=None):
        return self.request.user


"""     def form_valid(self, form):
        email = self.cleaned_data.get("email")
        self.object.username = email
        self.object.save()
        return super().form_valid(form) """


class UpdatePasswordView(PasswordChangeView):

    template_name = "users/update-password.html"
    success_url = reverse_lazy("users:update")

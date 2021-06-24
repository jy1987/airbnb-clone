from django.shortcuts import redirect
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy


class LoggedOutOnlyView(UserPassesTestMixin):

    permission_denied_message = "page not found"

    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        messages.error(self.request, "Can not go there")
        return redirect("core:home")


class LoggedInOnlyView(LoginRequiredMixin):
    login_url = reverse_lazy("users:login")

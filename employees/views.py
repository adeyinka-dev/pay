from django.contrib import messages
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.shortcuts import redirect

from .forms import EmployeeSignUpForm


class SignUpView(CreateView):
    form_class = EmployeeSignUpForm
    template_name = "registration/signup.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Thank You")
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy("home")

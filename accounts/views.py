from django.shortcuts import redirect, render
from django.urls.base import reverse_lazy
from django.views.generic import ListView, CreateView
from django.contrib.auth.models import User
from accounts.forms import UserForm
# Create your views here.
class CreateUser(CreateView):
    model = User
    form_class = UserForm
    template_name = 'register.html'
    success_url = reverse_lazy('home')
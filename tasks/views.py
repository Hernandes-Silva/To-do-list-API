from tasks.serializers import TaskSerializer
from tasks.forms import TaskForm
from tasks.models import Task
from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls.base import reverse, reverse_lazy
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
class ListTaskView(LoginRequiredMixin,ListView):
    model = Task
    template_name = 'task_list.html'
    context_object_name = "tasks"
class CreateTaskView(LoginRequiredMixin,CreateView):
    model = Task
    template_name = 'task_create.html'
    form_class = TaskForm
    success_url = reverse_lazy('task_list')
class UpdateTaskView(LoginRequiredMixin,UpdateView):
    model = Task
    template_name = 'task_update.html'
    form_class = TaskForm
    success_url = reverse_lazy('task_list')
class DeleteTaskView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'task_delete.html'
    success_url = reverse_lazy('task_list')
class ListTaskAPIView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Task.objects.all()
    serializer_class =  TaskSerializer
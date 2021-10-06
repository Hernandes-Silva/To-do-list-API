from tasks.serializers import TaskSerializer
from tasks.forms import TaskForm
from tasks.models import Task
from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls.base import reverse, reverse_lazy
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import Http404
# Create your views here.
class ListTaskView(LoginRequiredMixin,ListView):
    model = Task
    template_name = 'task_list.html'
    context_object_name = "tasks"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['classe']=self.object
        return context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user = self.request.user)
        return context
class CreateTaskView(LoginRequiredMixin,CreateView):
    model = Task
    template_name = 'task_create.html'
    form_class = TaskForm
    success_url = reverse_lazy('task_list')
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreateTaskView, self).form_valid(form)
class UpdateTaskView(LoginRequiredMixin,UpdateView):
    model = Task
    template_name = 'task_update.html'
    form_class = TaskForm
    success_url = reverse_lazy('task_list')
    def form_valid(self, form):
        if form.instance.user != self.request.user: #verify user post
            raise Http404
        form.instance.user = self.request.user
        return super(UpdateTaskView, self).form_valid(form)
class DeleteTaskView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'task_delete.html'
    success_url = reverse_lazy('task_list')
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if(self.object.user != self.request.user):
            raise Http404
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if(self.object.user != self.request.user):
            raise Http404
        return self.delete(request, *args, **kwargs)

#API
class ListTaskAPIView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Task.objects.all()
    serializer_class =  TaskSerializer
    def get_queryset(self):
        user = self.request.user
        return user.tasks.all()
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
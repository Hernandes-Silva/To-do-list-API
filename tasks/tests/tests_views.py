from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from tasks.models import Task
from tasks.tests.tests_models import create_deafault_task
class TestView(TestCase):
    def setUp(self):
        self.password = '123' 
        user = User.objects.create_superuser('test', 'test@email.com', self.password)
        self.user2 = User.objects.create_superuser('test2', 'test@email.com', self.password)
        create_deafault_task(self.user2)
        self.client.login(username=user.username, password=self.password)
    
    def test_get_listTaskView(self):
        response = self.client.get(reverse('task_list'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'task_list.html')
        #testing user task
        self.assertEquals(len(response.context['tasks']), 0)
        self.client.login(username=self.user2.username, password=self.password)
        response = self.client.get(reverse('task_list'))
        self.assertEquals(len(response.context['tasks']), 1)
    def test_post_CreateTaskView(self):
        response = self.client.post(reverse('task_create'), {'name':'testing2','status':'TOD'})
        self.assertEquals(response.status_code, 302)
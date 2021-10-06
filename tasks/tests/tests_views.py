from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from tasks.models import Task
from tasks.tests.tests_models import create_deafault_task
class TestView(TestCase):
    def setUp(self):
        self.password = '123' 
        self.user = User.objects.create_superuser('test', 'test@email.com', self.password)
        self.user2 = User.objects.create_superuser('test2', 'test@email.com', self.password)
        self.client.login(username=self.user.username, password=self.password)
        self.task = create_deafault_task(self.user2)
        token = Token.objects.get(user__username=self.user2.username)
        self.api = APIClient()
        self.api.credentials(HTTP_AUTHORIZATION='Token '+ token.key)
    
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
    def test_post_UpdateTaskView(self):
        # a user cannot change another user's task
        self.client.login(username=self.user.username, password=self.password)
        response = self.client.post(reverse('task_update', kwargs={'slug':self.task.slug}),{
            'name': 'newTask',
            'status': 'TOD',
        })
        self.assertEquals(response.status_code, 404)

        self.client.login(username=self.user2.username, password=self.password)
        response = self.client.post(reverse('task_update', kwargs={'slug':self.task.slug}),{
            'name': 'newTask',
            'status': 'TOD',
        })
        self.assertEquals(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertEquals(self.task.name, 'newTask')
    def test_get_DeleteTaskView(self):
        self.client.login(username=self.user2.username, password=self.password)
        response = self.client.get(reverse('task_delete', kwargs={'slug':self.task.slug}))
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, 'Are you sure you want to delete')
        self.assertTemplateUsed(response, 'task_delete.html')
        #other User
        self.client.login(username=self.user.username, password=self.password)
        response = self.client.get(reverse('task_delete', kwargs={'slug':self.task.slug}))
        self.assertEquals(response.status_code, 404)
    def test_post_DeleteTaskView(self):
        self.client.login(username=self.user2.username, password=self.password)
        response = self.client.post(reverse('task_delete', args=(self.task.slug,)), follow=True )
        self.assertRedirects(response, reverse('task_list'), status_code=302)

    #                    #           API 

    def test_get_ListTaskAPIView(self):
        response = self.api.get('/api/tasks/', format='api')
        self.assertEquals(response.status, 200)


        
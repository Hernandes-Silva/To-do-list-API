from django.test import TestCase
from django.contrib.auth.models import User

from tasks.models import Task
def create_deafault_task(user, name="testing"):
    task =Task.objects.create(name=name, status= 'TOD', user=user)
    return task
class TestTask(TestCase):
    def setUp(self):
        password = 'teste'
        self.user = User.objects.create_superuser('test', 'Test@gmail.com', password)
        self.task_name = 'testing'
        self.task = Task.objects.create(name=self.task_name, status= 'TOD', user=self.user)
        return super().setUp()
    def test_str(self):
        task = Task.objects.get(name=self.task_name)
        self.assertEquals(task.__str__(), self.task_name)
    def test_slug(self):
        self.assertEquals(self.task.slug, self.task_name)
        task = Task.objects.create(name=self.task_name, status= 'TOD', user=self.user)
        self.assertNotEquals(task.slug, self.task.slug)
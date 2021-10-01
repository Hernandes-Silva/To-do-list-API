from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from tasks.generator_slug import unique_slug_generator
# Create your models here.
class Task(models.Model):
    status_choice = [('COM', 'Complete'), ('INP', "In progress"), ('TOD', 'Todo')]
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length = 250, null = True, blank = True, unique=True)
    status = models.CharField(max_length=3, choices=status_choice)

    def __str__(self):
       return self.name

@receiver(pre_save, sender=Task)
def pre_save_receiver(sender, instance, *args, **kwargs):
   if not instance.slug:
       instance.slug = unique_slug_generator(instance)
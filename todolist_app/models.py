from django.db import models
from django.contrib.auth.models import User

class TaskList(models.Model):
    id = models.AutoField(primary_key=True)
    manage = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='tasklist', null=True, blank=True , help_text='The user who manages this task list.')
    title = models.CharField(max_length=200)
    task = models.CharField(max_length=300)
    done = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
        ordering = ['-id']
    
    def __str__(self):
        return self.task + ' - ' + str(self.done) + ' - ' + self.title
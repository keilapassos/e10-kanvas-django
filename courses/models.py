from uuid import uuid4
from django.db import models

# Create your models here.

class Course(models.Model):
  uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
  name = models.CharField(max_length=255)
  demo_time = models.TimeField()
  created_at = models.DateTimeField()
  link_repo = models.TextField()

  instructor = models.OneToOneField('users.User', on_delete=models.CASCADE, related_name='course', null=True)
  students = models.ManyToManyField('users.User', related_name='courses')

  
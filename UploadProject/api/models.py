from django.db import models
import uuid
# Create your models here.
class UsersTable(models.Model):
    id = models.UUIDField(primary_key=True,null=False,unique=True,default=uuid.uuid4())
    name = models.CharField(max_length=256,null=True)
    email = models.CharField(max_length=2056,null=True)
    password = models.CharField(max_length=256,null=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)

 
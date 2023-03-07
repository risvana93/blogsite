from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    popic=models.ImageField(upload_to='profile_picture',null=True)
    options=(
        ('male','male'),
        ('female','female'),
        ('others','others')
    )
    gender=models.CharField(max_length=12,choices=options)
    phone=models.IntegerField()
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='users')
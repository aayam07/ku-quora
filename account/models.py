from django.db import models
from django.contrib.auth import get_user_model
import uuid
from django.db.models.signals import post_save
# Create your models here.

User = get_user_model()


class Profile(models.Model):
    image = models.ImageField(default='default.png',null=True,blank=True)
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    token = models.CharField(max_length = 200,unique=True,null=False,blank=False)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.token
    
    def save_profile(sender,instance,*args,**kwargs):
        try:
            profile = Profile(user = instance,token = str(uuid.uuid1()) )
            profile.save()
            print('saved profile')
        except Exception as e:
            print('error = ',e)
        

post_save.connect(Profile.save_profile,sender=User)

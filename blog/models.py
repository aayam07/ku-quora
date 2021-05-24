from django.db import models
from django.contrib.auth.models import User
import uuid
from django.db.models.signals import post_save
from django.utils.text import slugify
from django.urls import reverse
from ckeditor.fields import RichTextField


class Tag(models.Model):
    title = models.CharField(max_length=100,verbose_name='Tag')
    slug = models.SlugField(null=False,unique=True)

    class Meta:
        verbose_name_plural = 'Tags'
    
    def get_absolute_url(self):
        return reverse('tags',args=[self.slug])
    
    def __str__(self):
        return self.title
    
    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args,**kwargs)


class Post(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    title = models.CharField(max_length = 100,verbose_name='Title')
    body = RichTextField(blank=True, null=True)
    # body = models.TextField(verbose_name='Body')
    posted_on = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag,related_name='tags')
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    def get_absolute_url(self):
        return reverse('post_detail',args=[str(self.id)])
    
    def __str__(self):
        return self.title


class Follow(models.Model):
    follower = models.ForeignKey(User,on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey(User,on_delete=models.CASCADE , related_name='following')


class Stream(models.Model):
    following = models.ForeignKey(User,on_delete=models.CASCADE,related_name='stream_following')
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    date = models.DateTimeField()

    def add_post_to_stream_for_followers(sender,instance,*args,**kwargs):
        # recently created post
        post = instance
        # user who recently created above post
        user = post.user
        followers = Follow.objects.all().filter(following=user)
        for follower in followers:
            stream = Stream(post=post,user=follower.follower,date=post.posted_on,following=user)
            stream.save()

class Likes(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_like')
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='post_liked')


class Dislikes(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE , related_name='user_dislike')
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='post_disliked')


post_save.connect(Stream.add_post_to_stream_for_followers,sender=Post)




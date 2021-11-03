from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class contact(models.Model):
    sno=models.AutoField(primary_key=True)
    name=models.CharField(max_length=200)
    email=models.CharField(max_length=200)
    address=models.CharField(max_length=200)



class post(models.Model):
    sno=models.AutoField(primary_key=True)
    title=models.CharField(max_length=100)
    content=models.TextField()
    timeslap=models.TimeField(blank=True)
    author=models.CharField(max_length=100)
    slug=models.SlugField(max_length=200)
    Image= models.ImageField(blank= True, null=True)

    def __str__(self):
        return f" post by {self.author} {self.title}"

class Comment(models.Model):
    sno = models.AutoField(primary_key=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(post,on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    email = models.EmailField()
    comment = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self',on_delete=models.CASCADE,null=True,blank=True,related_name='+')
    active = models.BooleanField(default=False)


    class Meta:
        ordering = ['created_on']

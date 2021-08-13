from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User



# Create your models here.

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.deletion.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    likes = models.ManyToManyField(User, related_name='blog_post')
    create_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)


    def total_likes(self):
        return self.likes.count()

    def who_liked(self):
        return ", ".join([str(p) for p in self.likes.all()])

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def approve_comments(self):
        return self.comments.filter(approved_comment=True)

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey('blog_app.Post', related_name='comments', on_delete=models.deletion.CASCADE)
    author = models.CharField(max_length=200)
    text = models.TextField()
    likes = models.IntegerField(default=0)
    create_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def give_like(self):
        return self.likes + 1

    def get_absolute_url(self):
        return reverse('post_list')

    def __str__(self):
        return self.text


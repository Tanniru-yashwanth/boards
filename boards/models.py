import math

from django.db import models
from django.contrib.auth.models import User
from markdown import markdown
from django.utils.html import mark_safe


class Board(models.Model):
    """
    Class to create board model.
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=200)

    def __str__(self):
        """
        Function to display the name of object created.
        """
        return f"{self.name}"

    def get_posts_count(self):
        return Post.objects.filter(topic__board=self).count()

    def get_last_post(self):
        return Post.objects.filter(topic__board=self).order_by('-created_at').first()


class Topic(models.Model):
    """
    Class to create topic model.
    """
    subject = models.CharField(max_length=255)
    last_updated = models.DateTimeField(auto_now_add=True)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='topics')
    starter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='topics')
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        """
        Function to display the object name.
        """
        return f"{self.subject}"

    def get_page_count(self):
        count = self.posts.count()
        pages = count / 3
        return math.ceil(pages)

    def has_many_pages(self, count=None):
        if count is None:
            count = self.get_page_count()
        return count > 6

    def get_page_range(self):
        count = self.get_page_count()
        if self.has_many_pages(count):
            return range(1, 5)
        return range(1, count + 1)

    def get_last_ten_posts(self):
        return self.posts.order_by('created_at')[:10]


class Post(models.Model):
    """
    Class to create post model.
    """
    message = models.TextField()
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    updated_by = models.ForeignKey(User, null=True, related_name='+', on_delete=models.CASCADE)

    def __str__(self):
        """
        Function to display the message.
        """
        return f"{self.message}"

    def get_message_as_markdown(self):
        return mark_safe(markdown(self.message, safe_mode='escape'))

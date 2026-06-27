from django.db import models
from django.utils import timezone
from datetime import timedelta
from users.models import User


class Story(models.Model):
    MEDIA_TYPES = [('image', 'Image'), ('video', 'Video')]

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stories')
    media = models.FileField(upload_to='stories/')
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPES, default='image')
    caption = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Story by {self.author.username} at {self.created_at:%Y-%m-%d %H:%M}"

    @property
    def is_active(self):
        return timezone.now() < self.created_at + timedelta(hours=24)

    @property
    def expires_at(self):
        return self.created_at + timedelta(hours=24)

    @property
    def view_count(self):
        return self.views.count()


class StoryView(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='views')
    viewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='story_views')
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('story', 'viewer')

    def __str__(self):
        return f"{self.viewer.username} viewed story #{self.story_id}"

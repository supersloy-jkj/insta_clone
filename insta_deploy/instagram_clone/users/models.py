from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class User(AbstractUser):
    bio = models.TextField(blank=True, max_length=500)
    profile_picture = models.ImageField(
        upload_to='profile_pics/',
        blank=True,
        null=True,
    )
    website = models.URLField(blank=True)
    is_private = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:profile', kwargs={'username': self.username})

    @property
    def follower_count(self):
        return self.followers.count()

    @property
    def following_count(self):
        return self.following.count()

    @property
    def post_count(self):
        return self.posts.count()

    def get_profile_picture_url(self):
        if self.profile_picture:
            return self.profile_picture.url
        # Generate a clean gradient avatar with initials via ui-avatars
        initials = self.username[:2].upper()
        # Consistent color from username hash
        colors = ['4f5bd5', 'd62976', 'fa7e1e', '962fbf', '0095f6', '00b894', 'e17055', '6c5ce7']
        color = colors[sum(ord(c) for c in self.username) % len(colors)]
        return f'https://ui-avatars.com/api/?name={initials}&background={color}&color=fff&size=150&bold=true&font-size=0.45'

    @property
    def initials(self):
        return self.username[:2].upper()


class Follow(models.Model):
    follower = models.ForeignKey(
        User, related_name='following', on_delete=models.CASCADE
    )
    followed = models.ForeignKey(
        User, related_name='followers', on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'followed')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.follower} → {self.followed}"

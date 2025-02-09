from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.auth.models import User

class Stream(models.Model):
    title = models.CharField(max_length=255)
    cover_image = models.ImageField(upload_to = 'covers/', validators = [FileExtensionValidator(allowed_extensions = ['jpeg', 'jpg', 'png'])])
    video_file = models.FileField(upload_to = 'files/', validators = [FileExtensionValidator(allowed_extensions = ['mp4', 'mkv'])])
    trailer_link = models.URLField(max_length=200)
    genre = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.CharField(max_length=14)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title + ' on ' + self.created_at.strftime('%Y-%m-%d')

class Comment(models.Model):
    video = models.ForeignKey(Stream, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.video.title}"

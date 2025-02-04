from django.core.validators import FileExtensionValidator
from django.db import models

# Create your models here.
class Stream(models.Model):
    title = models.CharField(max_length=255)
    cover_image = models.ImageField(upload_to = 'covers/', validators = [FileExtensionValidator(allowed_extensions = ['jpeg', 'jpg', 'png'])])
    video_file = models.FileField(upload_to = 'files/', validators = [FileExtensionValidator(allowed_extensions = ['mp4', 'mkv'])])
    trailer_link = models.URLField(max_length=200)
    genre = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    uploaded_by =models.CharField(max_length=14)

    class Meta:
        verbose_name_plural = "Streams"

    def __str__(self):
        return self.title + ' on ' + self.created_at.strftime('%Y-%m-%d')
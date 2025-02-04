from django.db import models
from django.core.validators import FileExtensionValidator

# Create your models here.
class Stream(models.Model):
    title = models.CharField(max_length=255)
    cover_image = models.ImageField(upload_to = 'media/covers/', validators = [FileExtensionValidator(allowed_extensions = ['jpeg', 'jpg', 'png'])])
    video_file = models.FileField(upload_to = 'media/files', validators = [FileExtensionValidator(allowed_extensions = ['mp4', 'mkv'])])
    trailer_link = models.URLField(max_length=200)
    genre = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Streams" # Changes the name of the table in the admin panel

    def __str__(self):
        return self.title + ' on ' + self.created_at.strftime('%Y-%m-%d')
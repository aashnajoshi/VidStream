from django.db import models
from django.utils import timezone

# Create your models here.
class ContactUs(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    file_path = models.FileField(upload_to='attachments/')
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return 'Message from ' + self.name + ' - ' + self.email + ' on ' + self.date_added.strftime('%Y-%m-%d')
from django.db import models

# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    file_path = models.FileField(upload_to='attachments/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Message from ' + self.name + ' - ' + self.email + ' on ' + self.created_at.strftime('%Y-%m-%d')
from django.db import models
from django.contrib.auth.models import User
import uuid

class UploadedFile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # associate with user
    file = models.FileField(upload_to='uploads/')
    display_name = models.CharField(max_length=255, blank=True)   # new field
    description = models.TextField(blank=True)   
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.display_name or self.file.name

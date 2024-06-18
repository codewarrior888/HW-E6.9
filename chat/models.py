from django.db import models
from django.contrib.auth.models import User
from PIL import Image
import uuid


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='defaultavatar.png', upload_to='avatars', null=True, blank=True)
    user_uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    def __str__(self):
        return f'{self.user.username} Account'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.avatar:
            try:
                img = Image.open(self.avatar.path)
                max_size = (300, 300)
                if img.height > max_size[1] or img.width > max_size[0]:
                    img.thumbnail(max_size)
                    img.save(self.avatar.path)
                    
            except:
                self.avatar = 'defaultavatar.png'
                self.save(update_fields=['avatar'])


class Room(models.Model):
    room_name = models.CharField(max_length=128, unique=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.room_name


class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(max_length=280)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.room} - {self.user}'

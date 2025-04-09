from django.db import models
from django.conf import settings


class Announcement(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=True)
    workshop = models.ForeignKey('workshops.Workshop', on_delete=models.CASCADE, null=True, blank=True,
                                 related_name='announcements')

    def __str__(self):
        return self.title


class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_messages')
    subject = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.subject} - From: {self.sender.get_full_name()} To: {self.recipient.get_full_name()}"

    @property
    def is_read(self):
        return self.read_at is not None


class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('payment', 'Payment Reminder'),
        ('workshop', 'Workshop Update'),
        ('announcement', 'New Announcement'),
        ('message', 'New Message'),
        ('system', 'System Notification'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)
    related_link = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.notification_type}: {self.title} for {self.user.get_full_name()}"

    @property
    def is_read(self):
        return self.read_at is not None
from django.db import models
from django.conf import settings


class WorkshopCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Workshop Categories"


class Workshop(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(WorkshopCategory, on_delete=models.SET_NULL, null=True, related_name="workshops")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.CharField(max_length=200)
    max_participants = models.PositiveIntegerField(default=10)
    instructor = models.CharField(max_length=100)
    materials_needed = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    @property
    def available_slots(self):
        return self.max_participants - self.registrations.count()

    @property
    def is_full(self):
        return self.available_slots <= 0


class Registration(models.Model):
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE, related_name="registrations")
    parent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                               related_name="workshop_registrations")
    child_name = models.CharField(max_length=100)
    child_age = models.PositiveIntegerField()
    registration_date = models.DateTimeField(auto_now_add=True)
    attended = models.BooleanField(default=False)
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ['workshop', 'parent', 'child_name']

    def __str__(self):
        return f"{self.child_name} - {self.workshop.title}"
from django.db import models
from django.db.models import Q, Manager
from django.utils import timezone

from task.managers import ToDoManager, InProgressManager, DoneManager, ArchiveManager, SoftDeleteManager
from task.validators import datetime_checker


# Manager

# Create your models here.
class Todo(models.Model):
    class Status(models.TextChoices):
        TODO = "todo", "To Do"
        IN_PROGRESS = 'in_progress', "IN Progress"
        DONE = "done", "Done"
        ARCHIVE = "archive", "Archive"

    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=Status, default=Status.TODO)
    priority = models.PositiveSmallIntegerField(default=3)
    due_date = models.DateTimeField(default=timezone.now, validators=[datetime_checker])
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    delete_at = models.DateTimeField(null=True, blank=True)

    # Standart Manager doim saqlanib qolishi kerak.
    objects = Manager()  # default

    # Managers
    todo = ToDoManager()  # custom manager
    in_progress = InProgressManager()  # custom manager
    done = DoneManager()  # custom manager
    archive = ArchiveManager()  # custom manager
    soft_del = SoftDeleteManager()  # custom manager

    class Meta:
        indexes = [
            models.Index(fields=['title', 'create_at']),
            models.Index(fields=['delete_at']),
        ]

        constraints = [
            models.CheckConstraint(check=Q(priority__gte=1) and Q(priority__lte=5), name="priority__range_1_5")
        ]

    def soft_delete(self):
        if not self.delete_at:
            self.delete_at = timezone.now()
            self.save(update_fields=["delete_at"])

    def __str__(self):
        return f"{self.title}: {self.status}"

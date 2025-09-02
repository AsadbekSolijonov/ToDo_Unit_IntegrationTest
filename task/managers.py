from django.db.models import Manager


# Managers
# Todo.objects.all() -- Barcha todo obyektlari
# Todo.todo.all() -- Bajarilishi kerak bo'lganlar.
# Todo.done.all() -- Bajarib bo'linganlar.
# Todo.archive.all() -- Arxivdagilar.

class ToDoManager(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='todo', delete_at__isnull=True)


class InProgressManager(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='in_progress', delete_at__isnull=True)


class DoneManager(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='done')


class ArchiveManager(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='archive', delete_at__isnull=True)


class SoftDeleteManager(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(delete_at__isnull=False)

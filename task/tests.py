from datetime import timedelta

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from task.models import Todo


class TestTodoModels(TestCase):
    def setUp(self):
        self.todo = Todo.objects.create(
            title="To Do 1",
            status=Todo.Status.TODO
        )

    # ------ UNIT test ----
    def test_str_todo_model(self):
        self.assertEqual(str(self.todo), f"{self.todo.title}: {self.todo.status}")

    def test_due_date_validator(self):
        with self.assertRaises(ValidationError):
            todo = Todo.objects.create(
                title="To Do 2",
                status=Todo.Status.TODO,
                due_date=timezone.now() - timedelta(seconds=1)
            )
            todo.full_clean()

    def test_todo_manager(self):
        self.todo.soft_delete()
        Todo.objects.create(
            title="To Do 2",
            status=Todo.Status.TODO,
            due_date=timezone.now() + timedelta(seconds=1)
        )
        todos_count = Todo.todo.all().count()
        self.assertEqual(todos_count, 1)

    def test_soft_delete(self):
        self.assertIsNone(self.todo.delete_at)
        self.todo.soft_delete()
        self.assertIsNotNone(self.todo.delete_at)
        # rollback

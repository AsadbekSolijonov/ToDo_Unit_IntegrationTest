from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone
from rest_framework.reverse import reverse
from datetime import timedelta

from task.models import Todo
from rest_framework.test import APITestCase
from rest_framework import status


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


class TodoAPITest(APITestCase):

    def setUp(self):
        self.url = reverse('todo-list')
        self.data = {
            "title": "To Do",
            "description": "Desc",
            "due_date": (timezone.now() + timedelta(days=1)).isoformat().replace('+00:00', 'Z'),
            "status": "todo"
        }
        res = self.client.post(self.url, data=self.data, format='json')
        self.todo_id = res.data["id"]  # <-- MUHIM: 'id' ni oling

    def test_todo_list_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Todo.objects.count(), 1)

    def test_todo_create_201(self):
        url = reverse('todo-list')
        data = {
            **self.data,
            "title": "Second",
            "due_date": (timezone.now() + timedelta(days=2)).isoformat().replace('+00:00', 'Z'),
        }
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Todo.objects.count(), 2)
        self.assertEqual(response.data.get('title'), 'Second')

    def test_todo_create_400(self):
        data = {
            **self.data,
            "due_date": (timezone.now() - timedelta(days=2)).isoformat().replace('+00:00', 'Z'),
        }
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Todo.objects.count(), 1)

    def test_todo_detail_200(self):
        url = reverse('todo-detail', kwargs={"pk": self.todo_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('title'), 'To Do')

    def test_todo_update_200(self):
        url = reverse('todo-detail', kwargs={"pk": self.todo_id})
        new_data = {
            **self.data,
            "title": 'Second'
        }
        res = self.client.put(url, data=new_data, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data.get('title'), 'Second')

    def test_todo_partial_update_200(self):
        detail_url = reverse('todo-detail', kwargs={"pk": self.todo_id})
        res = self.client.patch(detail_url, data={"title": "Partial Title"}, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data.get('title'), "Partial Title")
        self.assertIn('due_date', res.data)

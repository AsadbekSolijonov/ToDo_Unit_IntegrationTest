from datetime import timedelta

import model_bakery.baker
from django.contrib.auth.models import User
from django.test import override_settings
from django.utils import timezone
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from task.models import Todo


@override_settings(PASSWORD_HASHERS=["django.contrib.auth.hashers.MD5PasswordHasher"])
class TodoAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='u', password='p')
        self.other = User.objects.create_user(username='uo', password='po')
        self.superuser = User.objects.create_superuser(username='su', password='psu')
        self.admin = User.objects.create_user(username='au', password='pau', is_staff=True)
        self.payload = {
            "title": "To Do",
            "description": "Desc",
            "due_date": timezone.now() + timedelta(days=1),
            "status": "todo"
        }
        res = Todo.objects.create(**self.payload)
        self.todo_id = res.id
        self.list_url = reverse('task-list')
        self.client.force_authenticate(user=self.user)

    def test_todo_list_200(self):  # happy
        res = self.client.get(self.list_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_todo_create_201(self):  # happy
        res = self.client.post(self.list_url, data=self.payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data.get('title'), 'To Do')
        self.assertIn('due_date', res.data)
        self.assertIn('create_at', res.data)
        self.assertNotIn('delete_at', res.data)

    def test_todo_create_400(self):  # unhappy
        from datetime import timedelta
        bad_payload = {
            **self.payload,
            "due_date": timezone.now() - timedelta(days=1),
        }
        res = self.client.post(self.list_url, data=bad_payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_todo_partial_status_200(self):  # unhappy

        url = reverse('task-detail', kwargs={"pk": self.todo_id})
        payload = {
            **self.payload,
            "status": "done",
        }
        res = self.client.patch(url, data=payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data.get('status'), 'done')

    def test_todo_delete_204(self):
        url = reverse('task-detail', kwargs={"pk": self.todo_id})
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_todo_mark_done_action(self):
        url = reverse('task-mark-done', kwargs={"pk": self.todo_id})
        res = self.client.post(url)
        todo = Todo.objects.get()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(todo.status, 'done')

    def test_todos_mark_bulk_done_action(self):
        objs = model_bakery.baker.make(Todo, _quantity=4, status='todo')

        url = reverse('task-mark-bulk-done')
        res = self.client.post(url, data={"ids": [objs[1].id, objs[2].id]}, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        objs[1].refresh_from_db()
        objs[2].refresh_from_db()

        self.assertEqual(objs[1].status, "done")
        self.assertEqual(objs[2].status, "done")

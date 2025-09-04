from rest_framework import generics
from rest_framework.viewsets import ModelViewSet

from task.models import Todo
from task.serializers import TodoSerializer


class TodoListCreateAPIView(ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

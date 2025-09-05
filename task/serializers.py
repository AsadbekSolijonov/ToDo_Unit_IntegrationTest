from task.models import Todo
from rest_framework import serializers


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ['id', 'title', 'description', 'due_date', 'status', 'create_at', 'update_at']
        read_only_fields = ('id', 'create_at', 'update_at')

from rest_framework import serializers

from task.models import Todo


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ['id', 'title', 'description', 'due_date', 'status', 'create_at', 'update_at']
        read_only_fields = ('id', 'create_at', 'update_at')

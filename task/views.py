from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import generics

from rest_framework.viewsets import ModelViewSet

from task.models import Todo
from task.serializers import TodoSerializer


class TodoViewSet(ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

    @action(detail=True, methods=['post'], url_name='mark-done')
    def mark_done(self, request, pk=None):
        obj = self.get_object()
        obj.status = "done"
        obj.save()
        return Response({"detail": "Success"})

    @action(detail=False, methods=['post'], url_name='mark-bulk-done')
    def mark_bluk_done(self, request):
        ids = self.request.data.get('ids')
        if ids is None or not isinstance(ids, list):
            return Response({"errors": {"ids fields list[1,2,3] bo'lishi kerak."}}, status=status.HTTP_400_BAD_REQUEST)

        updated_count = self.get_queryset().filter(id__in=ids).update(status="done")
        return Response({"message": "Successfully updated", "update_count": updated_count})

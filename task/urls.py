from django.urls import path
from rest_framework.routers import DefaultRouter
from task.views import TodoListCreateAPIView

router = DefaultRouter()
router.register('todo', TodoListCreateAPIView)
urlpatterns = [
    # path('tasks', TodoListCreateAPIView.as_view(), name='task-list')
]

urlpatterns += router.urls


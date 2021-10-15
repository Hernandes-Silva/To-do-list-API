
from django.urls import path
from tasks import views
urlpatterns = [
    path('', views.ListTaskView.as_view(), name="home"),
    path('tasks/', views.ListTaskView.as_view(), name="task_list"),
    path('tasks/create', views.CreateTaskView.as_view(), name="task_create"),
    path('tasks/<str:slug>/update', views.UpdateTaskView.as_view(), name="task_update"),
    path('tasks/<str:slug>/delete', views.DeleteTaskView.as_view(), name="task_delete"),
    path("api/", views.api_urls, name="api"),
    path("api/tasks/", views.ListTaskAPIView.as_view(), name="api_task"),
    path('api/tasks/<int:pk>/detail/', views.UpdateDeleteTaskAPIView.as_view(), name="api_task_detail"),

]
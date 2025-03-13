from django.urls import path
from tasks.views import index, savetask, savesubtask, subtasks_view, ajax_rm_task, ajax_rm_subtask, calendar_view

urlpatterns = [
    path('', index, name='index'),
    path("save-task/", savetask, name="save_task"),
    path("save-subtask/", savesubtask, name="save-subtask"),    
    path('subtasks/<int:task_id>/', subtasks_view, name='subtasks_view'),
    path('task/<int:task_id>/rm/', ajax_rm_task, name='rm_task'),
    path('subtask/<int:subtask_id>/rm/', ajax_rm_subtask, name='rm_subtask'),
    path('calendar/', calendar_view, name='calendar'),
]

from django.urls import path
<<<<<<< HEAD
from tasks.views import index, savetask, subtasks_view, ajax_rm_task, ajax_rm_subtask
=======
from tasks.views import index, savetask, savesubtask, subtasks_view, ajax_rm_task, ajax_rm_subtask
>>>>>>> ae7b4020dca5f57d49b1ec01f8a8036af73594f6

urlpatterns = [
    path('', index, name='index'),
    path("save-task/", savetask, name="save_task"),
<<<<<<< HEAD
=======
    path("save-subtask/", savesubtask, name="save-subtask"),    
>>>>>>> ae7b4020dca5f57d49b1ec01f8a8036af73594f6
    path('subtasks/<int:task_id>/', subtasks_view, name='subtasks_view'),
    path('task/<int:task_id>/rm/', ajax_rm_task, name='rm_task'),
    path('subtask/<int:subtask_id>/rm/', ajax_rm_subtask, name='rm_subtask'),
]

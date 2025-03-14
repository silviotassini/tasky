from django.urls import path
from tasks.views import index, savetask, savesubtask, subtasks_view, ajax_rm_task, ajax_rm_subtask, calendar_view
from tasks.views import task_list, task_detail, update_task, add_subtask, update_subtask, delete_subtask, get_subtask_data

urlpatterns = [
    path('', index, name='index'),
    path("save-task/", savetask, name="save_task"),
    path("save-subtask/", savesubtask, name="save-subtask"),    
    path('subtasks/<int:task_id>/', subtasks_view, name='subtasks_view'),
    path('task/<int:task_id>/rm/', ajax_rm_task, name='rm_task'),
    path('subtask/<int:subtask_id>/rm/', ajax_rm_subtask, name='rm_subtask'),
    path('calendar/', calendar_view, name='calendar'),

    path('tasks/', task_list, name='task_list'),
    path('task/<int:task_id>/', task_detail, name='task_detail'),
    path('task/<int:task_id>/update/', update_task, name='update_task'),
    path('task/<int:task_id>/add_subtask/', add_subtask, name='add_subtask'),
    path('subtask/<int:subtask_id>/update/', update_subtask, name='update_subtask'),
    path('subtask/<int:subtask_id>/delete/', delete_subtask, name='delete_subtask'),
    path('subtask/<int:subtask_id>/data/', get_subtask_data, name='get_subtask_data'),    
]

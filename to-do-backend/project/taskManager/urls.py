from django.urls import path
from . import api

urlpatterns = [
    path("tasks/all/", api.all_task_list, name="all-task-list"),
    path("tasks/pending/", api.pending_task_list, name="pending-task-list"),
    path("tasks/complete/", api.completed_task_list, name="completed-task-list"),
    path("tasks/today/", api.todays_task_list, name="todays-task-list"),
    path("tasks/create", api.create_task, name="task-create"),
    path("tasks/delete/<uuid:id>", api.delete_task, name="task-delete"),
    path("tasks/update/<uuid:id>", api.update_task, name="task-update"),
    path("tasks/mark-complete/<uuid:id>", api.mark_task_complete, name="mark-task-complete"),
    path("tasks/mark-pending/<uuid:id>", api.mark_task_pending, name="mark-task-pending"),
    path("groups/all/", api.group_list, name="group-list"),
    path("groups/update/<uuid:id>", api.update_group, name="group-update"),
    path("groups/delete/<uuid:id>", api.delete_group, name="group-delete"),
    path("groups/create", api.create_group, name="group-create"),
]

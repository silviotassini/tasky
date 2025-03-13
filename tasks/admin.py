from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.db.models import Count, Sum

from .models import Task, SubTask, TaskComment, TaskHistory


class SubTaskInline(admin.TabularInline):
    """Inline para exibir subtarefas dentro de uma tarefa"""
    model = SubTask
    extra = 1
    fields = ('title', 'status', 'assigned_to', 'start_date',
              'estimated_end_date', 'estimated_hours', 'actual_hours')


class TaskCommentInline(admin.TabularInline):
    """Inline para exibir comentários dentro de uma tarefa"""
    model = TaskComment
    extra = 0
    readonly_fields = ('author', 'created_at')
    fields = ('author', 'content', 'created_at')

    def has_add_permission(self, request, obj=None):
        # Permite adicionar, mas não editar comentários existentes
        return True

    def has_change_permission(self, request, obj=None):
        return False

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """Admin para o model Task"""
    list_display = ('title', 'status', 'assigned_to', 'start_date', 'estimated_end_date',
                    'estimated_hours', 'actual_hours', 'is_overdue_display', 'progress_bar')
    list_filter = ('status','assigned_to',
                   'start_date', 'estimated_end_date')
    search_fields = ('title', 'description', 'assigned_to__username')
    readonly_fields = ('created_at', 'updated_at', 'progress_percentage')
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('title', 'description', 'status', 'priority', 'order')
        }),
        ('Datas e Tempo', {
            'fields': ('start_date', 'estimated_end_date', 'actual_end_date', 'estimated_hours', 'actual_hours')
        }),
        ('Atribuição', {
            'fields': ('assigned_to', 'created_by')
        }),
        ('Metadados', {
            'fields': ('created_at', 'updated_at', 'progress_percentage'),
            'classes': ('collapse',)
        }),
    )
    inlines = [SubTaskInline, TaskCommentInline]
    actions = ['mark_as_todo', 'mark_as_in_progress', 'mark_as_done']

    def is_overdue_display(self, obj):
        if obj.is_overdue():
            return format_html('<span style="color: red;">Atrasada</span>')
        return format_html('<span style="color: green;">No prazo</span>')
    is_overdue_display.short_description = 'Prazo'

    def progress_bar(self, obj):
        progress = obj.progress_percentage()
        color = 'green'
        if progress < 30:
            color = 'red'
        elif progress < 70:
            color = 'orange'
        return format_html(
            '<div style="width:100px; height:10px; background-color:#ddd;">'
            '<div style="height:10px; width:{}px; background-color:{}"></div></div>'
            '<span>{}</span>',
            progress, color, f"{progress}%"
        )
    progress_bar.short_description = 'Progresso'

    def mark_as_todo(self, request, queryset):
        queryset.update(status='todo')
    mark_as_todo.short_description = "Marcar selecionados como 'A Fazer'"

    def mark_as_in_progress(self, request, queryset):
        queryset.update(status='in_progress')
    mark_as_in_progress.short_description = "Marcar selecionados como 'Em Progresso'"

    def mark_as_done(self, request, queryset):
        queryset.update(status='done')
    mark_as_done.short_description = "Marcar selecionados como 'Concluída'"


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    """Admin para o model SubTask"""
    list_display = ('title', 'status', 'parent_task_link', 'assigned_to',
                    'start_date', 'estimated_end_date', 'estimated_hours', 'actual_hours')
    list_filter = ('status', 'assigned_to')
    search_fields = ('title', 'description', 'parent_task__title')
    readonly_fields = ('created_at', 'updated_at')

    def parent_task_link(self, obj):
        url = reverse('admin:core_task_change', args=[obj.parent_task_id])
        return format_html('<a href="{}">{}</a>', url, obj.parent_task)
    parent_task_link.short_description = 'Tarefa Principal'


@admin.register(TaskComment)
class TaskCommentAdmin(admin.ModelAdmin):
    """Admin para o model TaskComment"""
    list_display = ('task', 'author', 'content_preview', 'created_at')
    search_fields = ('task__title', 'author__username', 'content')
    readonly_fields = ('created_at',)
    list_filter = ('author', 'created_at')

    def content_preview(self, obj):
        if len(obj.content) > 50:
            return obj.content[:50] + '...'
        return obj.content
    content_preview.short_description = 'Conteúdo'

    def has_change_permission(self, request, obj=None):
        # Comentários não podem ser editados depois de criados
        return False


@admin.register(TaskHistory)
class TaskHistoryAdmin(admin.ModelAdmin):
    """Admin para o model TaskHistory"""
    list_display = ('task', 'action', 'user', 'timestamp')
    list_filter = ('action', 'user', 'timestamp')
    search_fields = ('task__title', 'user__username', 'action', 'details')
    readonly_fields = ('task', 'user', 'action', 'details', 'timestamp')

    def has_add_permission(self, request):
        # Histórico não pode ser adicionado manualmente
        return False

    def has_change_permission(self, request, obj=None):
        # Histórico não pode ser editado
        return False

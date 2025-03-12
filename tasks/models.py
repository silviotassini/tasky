from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class TaskStatus(models.TextChoices):
    """Choices para status de tarefas"""
    TO_DO = 'todo', 'A Fazer'
    IN_PROGRESS = 'in_progress', 'Em Progresso'
    DONE = 'done', 'Concluída'

class Task(models.Model):
    """Model para representar uma tarefa principal"""
    title = models.CharField(max_length=200, verbose_name="Título")
    description = models.TextField(blank=True, null=True, verbose_name="Descrição")
    status = models.CharField(
        max_length=20,
        choices=TaskStatus.choices,
        default=TaskStatus.TO_DO,
        verbose_name="Status"
    )
    
    # Datas e tempos
    start_date = models.DateField(default=timezone.now, verbose_name="Data de Início")
    estimated_end_date = models.DateField(verbose_name="Previsão de Término")
    actual_end_date = models.DateField(blank=True, null=True, verbose_name="Data de Término Real")
    estimated_hours = models.DecimalField(
        max_digits=6, 
        decimal_places=2, 
        verbose_name="Tempo Estimado (horas)"
    )
    actual_hours = models.DecimalField(
        max_digits=6, 
        decimal_places=2, 
        default=0, 
        verbose_name="Tempo Gasto (horas)"
    )
    
    # Atribuições
    assigned_to = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name="assigned_tasks",
        verbose_name="Responsável"
    )
    created_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name="created_tasks",
        verbose_name="Criado por"
    )
    
    # Controle de timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")
    
    # Campos adicionais
    priority = models.PositiveIntegerField(default=0, verbose_name="Prioridade")
    order = models.PositiveIntegerField(default=0, verbose_name="Ordem no Quadro")
    
    def __str__(self):
        return self.title
    
    def is_overdue(self):
        """Verifica se a tarefa está atrasada"""
        if self.status != TaskStatus.DONE and self.estimated_end_date < timezone.now().date():
            return True
        return False
    
    def progress_percentage(self):
        """Calcula o percentual de progresso baseado nas subtarefas"""
        subtasks = self.subtasks.all()
        if not subtasks:
            return 0
        
        completed = subtasks.filter(status=TaskStatus.DONE).count()
        return int((completed / subtasks.count()) * 100)
    
    class Meta:
        verbose_name = "Tarefa"
        verbose_name_plural = "Tarefas"
        ordering = ['status', 'order', 'priority']

class SubTask(models.Model):
    """Model para representar uma subtarefa"""
    title = models.CharField(max_length=200, verbose_name="Título")
    description = models.TextField(blank=True, null=True, verbose_name="Descrição")
    status = models.CharField(
        max_length=20,
        choices=TaskStatus.choices,
        default=TaskStatus.TO_DO,
        verbose_name="Status"
    )
    parent_task = models.ForeignKey(
        Task, 
        on_delete=models.CASCADE, 
        related_name="subtasks",
        verbose_name="Tarefa Principal"
    )
    
    # Datas e tempos
    start_date = models.DateField(blank=True, null=True, verbose_name="Data de Início")
    estimated_end_date = models.DateField(blank=True, null=True, verbose_name="Previsão de Término")
    actual_end_date = models.DateField(blank=True, null=True, verbose_name="Data de Término Real")
    estimated_hours = models.DecimalField(
        max_digits=6, 
        decimal_places=2, 
        blank=True, 
        null=True,
        verbose_name="Tempo Estimado (horas)"
    )
    actual_hours = models.DecimalField(
        max_digits=6, 
        decimal_places=2, 
        default=0, 
        verbose_name="Tempo Gasto (horas)"
    )
    
    # Atribuições
    assigned_to = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name="assigned_subtasks",
        verbose_name="Responsável"
    )
    
    # Controle de timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")
    
    # Ordem
    order = models.PositiveIntegerField(default=0, verbose_name="Ordem")
    
    def __str__(self):
        return self.title
    
    def is_overdue(self):
        """Verifica se a subtarefa está atrasada"""
        if self.status != TaskStatus.DONE and self.estimated_end_date and self.estimated_end_date < timezone.now().date():
            return True
        return False
    
    class Meta:
        verbose_name = "Subtarefa"
        verbose_name_plural = "Subtarefas"
        ordering = ['order', 'created_at']

class TaskComment(models.Model):
    """Model para comentários em tarefas"""
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="comments", verbose_name="Tarefa")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Autor")
    content = models.TextField(verbose_name="Conteúdo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    
    def __str__(self):
        return f"Comentário de {self.author} em {self.task}"
    
    class Meta:
        verbose_name = "Comentário"
        verbose_name_plural = "Comentários"
        ordering = ['-created_at']

class TaskHistory(models.Model):
    """Model para histórico de alterações em tarefas"""
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="history", verbose_name="Tarefa")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Usuário")
    action = models.CharField(max_length=100, verbose_name="Ação")
    details = models.TextField(blank=True, null=True, verbose_name="Detalhes")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Data/Hora")
    
    def __str__(self):
        return f"{self.action} em {self.task} por {self.user}"
    
    class Meta:
        verbose_name = "Histórico"
        verbose_name_plural = "Históricos"
        ordering = ['-timestamp']

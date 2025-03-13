
from django.shortcuts import render, redirect, get_object_or_404
from .models import Task, SubTask, TaskStatus
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

@login_required
def index(request):
    # Substitua isso por dados reais do seu modelo
    to_do_tasks = Task.objects.filter(status=TaskStatus.TO_DO)
    in_progress_tasks = Task.objects.filter(status=TaskStatus.IN_PROGRESS)
    done_tasks = Task.objects.filter(status=TaskStatus.DONE)
    users = User.objects.all()
    context = {
        'to_do_tasks': to_do_tasks,
        'in_progress_tasks': in_progress_tasks,
        'done_tasks': done_tasks,
        'to_do_count': to_do_tasks.count(),
        'in_progress_count': in_progress_tasks.count(),
        'done_count': done_tasks.count(),
        'users': users,
    }

    return render(request, 'tasks/index.html', context)

@login_required
def subtasks_view(request, task_id):
    # Obter a tarefa correspondente ao ID
    task = get_object_or_404(Task, id=task_id)
    
    # Filtrar subtarefas relacionadas à tarefa
    to_do_subtasks = SubTask.objects.filter(parent_task=task, status=TaskStatus.TO_DO)
    in_progress_tasks = SubTask.objects.filter(parent_task=task, status=TaskStatus.IN_PROGRESS)
    done_tasks = SubTask.objects.filter(parent_task=task, status=TaskStatus.DONE)
    
    # Contexto para o template
    context = {
        'task': task,  # Passa a tarefa pai
        'to_do_subtasks': to_do_subtasks,
        'in_progress_tasks': in_progress_tasks,
        'done_tasks': done_tasks,
        'to_do_count': to_do_subtasks.count(),
        'in_progress_count': in_progress_tasks.count(),
        'done_count': done_tasks.count(),
    }
    return render(request, 'tasks/subtask.html', context)

def ajax_rm_task(request, task_id):
    """
    View para apagar uma tarefa via AJAX.
    Útil para apagar sem sair da página.
    """
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        task = get_object_or_404(Task, id=task_id)
        
        # Opcional: permissões de verificação
        
        # Apaga a subtarefa
        task.delete()
        
        # Retorna resposta JSON
        return JsonResponse({
            'success': True,
            'message': 'Tarefa apagada com sucesso.'
        })
    
    # Se não for uma requisição AJAX POST, retorna erro
    return JsonResponse({
        'success': False,
        'message': 'Método não permitido'
    }, status=405)

def ajax_rm_subtask(request, subtask_id):
    """
    View para apagar uma subtarefa via AJAX.
    Útil para apagar sem sair da página.
    """
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        subtask = get_object_or_404(SubTask, id=subtask_id)
        
        # Opcional: permissões de verificação
        
        # Apaga a subtarefa
        subtask.delete()
        
        # Retorna resposta JSON
        return JsonResponse({
            'success': True,
            'message': 'Subtarefa apagada com sucesso.'
        })
    
    # Se não for uma requisição AJAX POST, retorna erro
    return JsonResponse({
        'success': False,
        'message': 'Método não permitido'
    }, status=405)

def savetask(request):
    if request.method == "POST":
        # Obtém os dados do formulário
        title = request.POST.get("title")
        description = request.POST.get("description")
        deadline = request.POST.get("deadline")
        assigned_to_id = request.POST.get("assigned_to")
        estimated_hours = request.POST.get("estimated_hours")
        # Cria a nova tarefa
        Task.objects.create(
            title=title,
            description=description,
            estimated_end_date=deadline,
            assigned_to_id=assigned_to_id,
            estimated_hours = estimated_hours,
            created_by=request.user
        )

    return redirect("index")

def savesubtask(request):
    if request.method == "POST":
        task = get_object_or_404(Task, id=request.POST.get("task_id"))
        # Obtém os dados do formulário
        title = request.POST.get("title")
        description = request.POST.get("description")
        deadline = request.POST.get("deadline")
        assigned_to_id = task.assigned_to.pk
        estimated_hours = request.POST.get("estimated_hours")
        # Cria a nova tarefa        

        SubTask.objects.create(
            title=title,
            description=description,
            estimated_end_date=deadline,
            assigned_to_id=assigned_to_id,
            estimated_hours = estimated_hours,
            parent_task = task
        )

    return redirect(f"/subtasks/{task.id}/")

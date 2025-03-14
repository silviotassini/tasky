from django.utils import timezone
from datetime import date, timedelta
import calendar
from calendar import monthrange
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from tasks.forms.forms import SubTaskForm, TaskForm
from .models import Task, SubTask, TaskStatus
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from django.views.decorators.http import require_POST

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

def calendar_view(request):
    # Obtém o mês e ano da query string ou usa o mês atual
    today = timezone.now().date()
    year = int(request.GET.get('year', today.year))
    month = int(request.GET.get('month', today.month))
    
    # Cria um objeto de calendário
    cal = calendar.monthcalendar(year, month)
    
    # Obtém o primeiro e último dia do mês
    try:
        first_day = date(year, month, 1)
        days_in_month = monthrange(year, month)[1]
        last_day = date(year, month, days_in_month)
    except ValueError:
        # Garante que não haverá erro em caso de datas inválidas
        first_day = today.replace(day=1)
        last_day = first_day + timedelta(days=monthrange(first_day.year, first_day.month)[1] - 1)
    
    # Calcula o mês anterior e o próximo mês
    prev_month = month - 1 if month > 1 else 12
    prev_year = year if month > 1 else year - 1
    next_month = month + 1 if month < 12 else 1
    next_year = year if month < 12 else year + 1
    
    # Lista de nomes dos meses em português
    month_names = [
        'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
        'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
    ]
    
    # Obtém todas as tarefas do mês
    start_date = first_day - timedelta(days=7)  # Uma semana antes
    end_date = last_day + timedelta(days=7)     # Uma semana depois
    
    tasks = Task.objects.filter(
        Q(start_date__lte=end_date) & Q(estimated_end_date__gte=start_date)
    ).order_by('start_date', 'priority')
    
    # Organiza as tarefas por data
    task_dict = {}
    for task in tasks:
        current_date = task.start_date
        while current_date <= task.estimated_end_date:
            if current_date not in task_dict:
                task_dict[current_date] = []
            task_dict[current_date].append(task)
            current_date += timedelta(days=1)
    
    # Prepara os dados do calendário para o template
    calendar_weeks = []
    for week in cal:
        week_data = []
        for day in week:
            if day == 0:  # Dias fora do mês
                week_data.append((None, []))
            else:
                current_day = date(year, month, day)
                week_data.append((current_day, task_dict.get(current_day, [])))
        calendar_weeks.append(week_data)
    
    context = {
        'calendar_weeks': calendar_weeks,
        'month': month,
        'year': year,
        'month_name': month_names[month - 1],
        'prev_month': prev_month,
        'prev_year': prev_year,
        'next_month': next_month,
        'next_year': next_year,
        'today': today,
    }
    
    return render(request, 'tasks/calendar.html', context)

def task_detail(request, task_id):
    """
    View que exibe os detalhes de uma tarefa específica e suas subtarefas.
    """
    # Busca a tarefa no banco de dados
    task = get_object_or_404(Task, id=task_id)
    
    # Busca todas as subtarefas relacionadas
    subtasks = task.subtasks.all()
    
    # Formulários para edição e criação
    task_form = TaskForm(instance=task)
    subtask_form = SubTaskForm()
    
    context = {
        'task': task,
        'subtasks': subtasks,
        'task_form': task_form,
        'subtask_form': subtask_form,
    }
    
    return render(request, 'tasks/task_detail.html', context)

@require_POST
def update_task(request, task_id):
    """
    View para processar a atualização de uma tarefa existente.
    """
    task = get_object_or_404(Task, id=task_id)
    form = TaskForm(request.POST, instance=task)
    
    if form.is_valid():
        form.save()
        messages.success(request, 'Tarefa atualizada com sucesso!')
    else:
        messages.error(request, 'Erro ao atualizar tarefa. Verifique os dados informados.')
    
    return redirect('task_detail', task_id=task_id)

@require_POST
def add_subtask(request, task_id):
    """
    View para adicionar uma nova subtarefa a uma tarefa existente.
    """
    task = get_object_or_404(Task, id=task_id)
    form = SubTaskForm(request.POST)
    
    if form.is_valid():
        subtask = form.save(commit=False)
        subtask.task = task
        subtask.save()
        messages.success(request, 'Subtarefa adicionada com sucesso!')
    else:
        messages.error(request, 'Erro ao adicionar subtarefa. Verifique os dados informados.')
    
    return redirect('task_detail', task_id=task_id)

@require_POST
def update_subtask(request, subtask_id):
    """
    View para atualizar uma subtarefa existente.
    """
    subtask = get_object_or_404(SubTask, id=subtask_id)
    task_id = subtask.task.id
    form = SubtaskForm(request.POST, instance=subtask)
    
    if form.is_valid():
        form.save()
        messages.success(request, 'Subtarefa atualizada com sucesso!')
    else:
        messages.error(request, 'Erro ao atualizar subtarefa. Verifique os dados informados.')
    
    return redirect('task_detail', task_id=task_id)

@require_POST
def delete_subtask(request, subtask_id):
    """
    View para excluir uma subtarefa.
    """
    subtask = get_object_or_404(SubTask, id=subtask_id)
    task_id = subtask.task.id
    
    subtask.delete()
    messages.success(request, 'Subtarefa excluída com sucesso!')
    
    return redirect('task_detail', task_id=task_id)

def task_list(request):
    """
    View para listar todas as tarefas.
    """
    tasks = Task.objects.all()
    return render(request, 'tasks/task_list.html', {'tasks': tasks})

def get_subtask_data(request, subtask_id):
    """
    View para obter os dados de uma subtarefa via AJAX.
    """
    subtask = get_object_or_404(SubTask, id=subtask_id)
    
    data = {
        'id': subtask.id,
        'title': subtask.title,
        'description': subtask.description,
        'due_date': subtask.due_date.strftime('%Y-%m-%d') if subtask.due_date else '',
        'status': subtask.status,
    }
    
    return JsonResponse(data)
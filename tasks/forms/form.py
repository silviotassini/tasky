<form id = "new-task-form" method = "POST" action = "{% url 'save_task' %}" >
    {% csrf_token % }
    <input type = "hidden" id = "destination-card" name = "board_id" value = "{{ board_id }}" / >
    <div class = "form-group" >
      <label for = "task-title" > Título: < /label >
       <input type = "text" id = "task-title" name = "title" required / >
    </div >
    <div class = "form-group" >
      <label for = "task-description" > Descrição: < /label >
       <textarea id = "task-description" name = "description" required > </textarea >
    </div >
    <div class = "form-group" >
      <label for = "task-deadline" > Prazo: < /label >
       <input type = "date" id = "task-deadline" name = "deadline" required / >
    </div >
    <div class = "form-group" >
      <label for = "task-assigned" > Responsável: < /label >
       <select id = "task-assigned" name = "assigned_to" required >
            {% for user in users % }
                <option value = "{{ user.id }}" > {{user.username}} < /option >
            {% endfor % }
        </select >
    </div >
    <button type = "submit" > Salvar < /button >
</form >

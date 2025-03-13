function deleteTask(taskId, url, buttonElement) {
    // Confirmar antes de excluir
    updateTaskCounters()
    if (confirm('Tem certeza que deseja excluir esta tarefa?')) {
        // Obter o token CSRF
        const csrftoken = getCookie('csrftoken')

        // Fazer a requisição AJAX
        fetch(url, {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': csrftoken
            }
        })
            .then((response) => response.json())
            .then((data) => {
                if (data.success) {
                    // Se a exclusão foi bem-sucedida, remover o elemento da tarefa do DOM
                    const taskElement = buttonElement.closest('.task')
                    taskElement.style.opacity = '0'
                    setTimeout(() => {
                        taskElement.remove()

                        // Opcional: mostrar mensagem de sucesso
                        showMessage(data.message, 'success')

                        // Opcional: atualizar contadores ou outras informações da página
                        updateTaskCounters()
                    }, 300) // Tempo para a animação de fade-out
                } else {
                    // Se houve um erro, mostrar mensagem
                    showMessage(data.message || 'Erro ao excluir tarefa', 'error')
                }
            })
            .catch((error) => {
                console.error('Erro:', error)
                showMessage('Erro ao processar a solicitação', 'error')
            })
    }
}

function getCookie(name) {
    let cookieValue = null
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';')
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim()
            if (cookie.substring(0, name.length + 1) === name + '=') {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
                break
            }
        }
    }
    return cookieValue
}

function showMessage(message, type) {
    // Verificar se já existe um container de mensagens
    let messageContainer = document.getElementById('message-container')

    // Se não existir, criar um
    if (!messageContainer) {
        messageContainer = document.createElement('div')
        messageContainer.id = 'message-container'
        messageContainer.style.position = 'fixed'
        messageContainer.style.top = '20px'
        messageContainer.style.right = '20px'
        messageContainer.style.zIndex = '1000'
        document.body.appendChild(messageContainer)
    }

    // Criar o elemento da mensagem
    const messageElement = document.createElement('div')
    messageElement.className = `alert alert-${type}`
    messageElement.style.padding = '10px 15px'
    messageElement.style.marginBottom = '10px'
    messageElement.style.borderRadius = '4px'
    messageElement.style.boxShadow = '0 2px 5px rgba(0,0,0,0.2)'

    // Estilizar com base no tipo
    if (type === 'success') {
        messageElement.style.backgroundColor = '#d4edda'
        messageElement.style.color = '#155724'
        messageElement.style.borderColor = '#c3e6cb'
    } else if (type === 'error') {
        messageElement.style.backgroundColor = '#f8d7da'
        messageElement.style.color = '#721c24'
        messageElement.style.borderColor = '#f5c6cb'
    }

    messageElement.textContent = message

    // Adicionar botão de fechar
    const closeButton = document.createElement('button')
    closeButton.innerHTML = '&times;'
    closeButton.style.marginLeft = '10px'
    closeButton.style.border = 'none'
    closeButton.style.background = 'none'
    closeButton.style.fontSize = '18px'
    closeButton.style.fontWeight = 'bold'
    closeButton.style.cursor = 'pointer'
    closeButton.onclick = function () {
        messageContainer.removeChild(messageElement)
    }

    messageElement.appendChild(closeButton)
    messageContainer.appendChild(messageElement)

    // Remover a mensagem após 5 segundos
    setTimeout(() => {
        if (messageElement.parentNode === messageContainer) {
            messageContainer.removeChild(messageElement)
        }
    }, 5000)
}

function updateTaskCounters() {
    // Atualizar o contador de tarefas "A Fazer"
    const todoCardBody = document.getElementById('todo-card')
    if (todoCardBody) {
        // Contar as tarefas no card "A Fazer"
        const todoTaskCount = todoCardBody.querySelectorAll('.task').length

        // Encontrar o cabeçalho do card "A Fazer"
        const todoCardHeader = todoCardBody.previousElementSibling
        if (todoCardHeader && todoCardHeader.classList.contains('card-header')) {
            // Encontrar o badge dentro do cabeçalho
            const badge = todoCardHeader.querySelector('.badge')
            if (badge) {
                // Atualizar o texto do badge
                badge.textContent = todoTaskCount
            }
        }
    }

    // Você pode fazer o mesmo para os outros cards também
    updateCardCounter('progress-card', 'in-progress')
    updateCardCounter('done-card', 'done')
}

// Função auxiliar para atualizar o contador de qualquer card
function updateCardCounter(cardId, headerClass) {
    const cardBody = document.getElementById(cardId)
    if (cardBody) {
        const taskCount = cardBody.querySelectorAll('.task').length

        const cardHeader = cardBody.previousElementSibling
        if (cardHeader && cardHeader.classList.contains('card-header')) {
            const badge = cardHeader.querySelector('.badge')
            if (badge) {
                badge.textContent = taskCount
            }
        }
    }
}
// Funções para adicionar nova tarefa
function showTaskForm(cardId) {
    document.getElementById('task-modal').style.display = 'block'
}

function closeTaskForm() {
    document.getElementById('task-modal').style.display = 'none'
}

// Função para salvar a nova tarefa no backend (simulada)
function saveNewTask(taskId, cardId, title, description, deadline, assigned) {
    console.log(`Nova tarefa criada: ${title}`)
    // Aqui você adicionaria uma chamada AJAX para salvar a tarefa no backend
}

// Fechar o modal se o usuário clicar fora dele
window.onclick = function (event) {
    const modal = document.getElementById('task-modal')
    if (event.target === modal) {
        closeTaskForm()
    }
}

document.addEventListener('DOMContentLoaded', function () {
    // Obtém a data atual
    const today = new Date()

    // Formata a data no formato YYYY-MM-DD que é o formato aceito pelo input type="date"
    const year = today.getFullYear()
    const month = String(today.getMonth() + 1).padStart(2, '0') // O mês começa em 0
    const day = String(today.getDate()).padStart(2, '0')

    const formattedDate = `${day}-${month}-${year}`

    // Define o valor do campo deadline como a data de hoje
    document.getElementById('task-deadline').value = formattedDate
})
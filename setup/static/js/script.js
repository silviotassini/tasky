document.addEventListener('DOMContentLoaded', function () {
    const toggleBtn = document.getElementById('toggleBtn')
    const sidebar = document.getElementById('sidebar')
    const body = document.body

    toggleBtn.addEventListener('click', function () {
        sidebar.classList.toggle('collapsed')
        body.classList.toggle('collapsed-sidebar')
    })

    // Ajusta o comportamento em telas pequenas
    function checkScreenSize() {
        if (window.innerWidth <= 768) {
            sidebar.classList.add('collapsed')
            body.classList.remove('collapsed-sidebar')

            // Inverte o comportamento do botão em telas pequenas
            toggleBtn.addEventListener('click', function () {
                if (sidebar.classList.contains('collapsed')) {
                    sidebar.style.transform = 'translateX(0)'
                } else {
                    sidebar.style.transform = 'translateX(-100%)'
                }
            })
        } else {
            sidebar.style.transform = 'translateX(0)'
        }
    }

    // Verifica o tamanho da tela ao carregar
    checkScreenSize()

    // Verifica ao redimensionar
    window.addEventListener('resize', checkScreenSize)
})
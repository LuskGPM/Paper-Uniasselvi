const form_senha = document.getElementById('form-senha')
const alter_senha = document.getElementById('alter-senha')

alter_senha.onclick = () => {
    if (form_senha.style.display == 'none'){
        form_senha.style.display = 'grid'
        alter_senha.value = 'Cancelar'
    }
    else {
        form_senha.style.display = 'none'
        alter_senha.value = 'Alterar Senha'
    }
}
const form_senha = document.getElementById('form_senha');
const btn = document.getElementById('alter-senha');
function aparecer_formulario_de_senha() {
    form_senha.classList.toggle('display-form-senha');
    btn.classList.toggle('active-btn-senha')
}
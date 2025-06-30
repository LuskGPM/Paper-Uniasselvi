const btnEdit = document.getElementById('edit')
const btnReset = document.getElementById('reset')
const btnSave = document.getElementById('save')
const inputs = document.querySelectorAll('input')

btnEdit.onclick = () => {
    if (btnEdit.value === 'Editar') {
        for (i = 1; i < inputs.length; i++) {
            inputs[i].disabled = false
        }
        btnEdit.value = 'Cancelar'
        btnReset.classList.toggle('ativo')
        btnSave.classList.toggle('ativo')
    } else {
        btnEdit.value = 'Editar'
        for (i = 1; i < inputs.length; i++) {
            inputs[i].disabled = true
        }
        btnEdit.disabled = false
        btnReset.classList.toggle('ativo')
        btnSave.classList.toggle('ativo')
    }
}
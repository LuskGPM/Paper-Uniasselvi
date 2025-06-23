const btnEdit = document.querySelector('#edit')
const btnSalvar = document.querySelector('#save')
const btnReset = document.querySelector('#reset')
const inputs = document.querySelectorAll('input')
const txtarea = document.querySelector('textarea')

btnEdit.onclick = () => {
    if (btnEdit.value === 'Editar') {
        btnEdit.value = 'Cancelar'
        for (i = 1; i<inputs.length; i++) {
            inputs[i].disabled = false
        }
        txtarea.disabled = false
        
    } else {
        btnEdit.value = 'Editar'
        btnSalvar.disabled = true
        for (i = 1; i<inputs.length; i++) {
            inputs[i].disabled = true
        }
        txtarea.disabled = true
        btnEdit.disabled = false
    }
    btnSalvar.classList.toggle('ativo')
    btnReset.classList.toggle('ativo')
    btnSalvar.disabled = false
}
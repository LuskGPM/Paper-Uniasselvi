var btnE = document.querySelector('#edit')
var btnS = document.querySelector('.save')
const inputs = document.querySelectorAll('input')
const textArea = document.querySelector('textarea')

btnE.onclick = () => {
    if (btnE.classList.contains('blue')) {
        btnE.classList.remove('blue')
        btnE.classList.add('red')
    } else {
        btnE.classList.remove('red')
        btnE.classList.add('blue')
    }
    if (btnS.disabled) {
        btnS.disabled = false
    } else {
        btnS.disabled = true
    }
    if (inputs[0].disabled) {
        for (i=0; i<inputs.length; i++) {
        inputs[i].disabled = false
        }
        textArea.disabled = false
    } else {
        for (i=0; i<inputs.length; i++) {
        inputs[i].disabled = true
        }
        textArea.disabled = true
    }
}
const sanduiche = document.querySelector('#sanduiche')
const colapseNav = document.querySelector("#colapse")

sanduiche.onclick = () => {
    colapseNav.classList.toggle('aberto')
    if (colapseNav.classList.contains('aberto')) {
        sanduiche.innerHTML = 'close'
    } else {
        sanduiche.innerHTML = 'menu'
    }
}
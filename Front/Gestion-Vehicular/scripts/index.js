let menu = document.querySelector('.navbar');
let menuIcon = document.querySelector('#menu-icon');

document.querySelector('#menu-icon').onclick = () => {
    menu.classList.toggle('active');
}

window.onscroll = () => {
    menu.classList.remove('active');
}

document.addEventListener('click', (event) => {
    if (!menu.contains(event.target) && !menuIcon.contains(event.target)) {
        menu.classList.remove('active');
    }
});
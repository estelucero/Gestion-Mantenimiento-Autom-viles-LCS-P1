let button = document.getElementById("read");
let eliminar1 = document.getElementById("delete1");
let eliminar2 = document.getElementById("delete2");
button.addEventListener('click', () => {
    document.querySelectorAll('.single-box').forEach(e => {
        e.classList.add('delete');

    })
    document.querySelectorAll('.dot').forEach(e => {
        console.log(e.classList)
        e.classList.remove('dot');

    })
    document.getElementById('num').innerText = '0'

    
})

eliminar1.addEventListener('click',()=>{
    document.querySelectorAll('#single-box1').forEach(e => {
        
        e.classList.add('delete');

    })
})
eliminar2.addEventListener('click',()=>{
    document.querySelectorAll('#single-box2').forEach(e => {
        
        e.classList.add('delete');

    })
})
document.addEventListener('DOMContentLoaded',function(){
    document.getElementById('registro').addEventListener('click',function(){
        window.location.href='/registro';
    })
})

function iniciarSesion() {
    window.location.href='/ingreso';
}

function mostrarBarraBusqueda() {
    var barraBusqueda = document.getElementById('barra-busqueda');
    barraBusqueda.style.display = 'block';
}

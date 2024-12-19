const ball = document.querySelector(".toggle-ball");
const items = document.querySelectorAll(".container,.films-list-title,.navbar-container,.sidebar,.left-menu-icon,.toggle");

ball.addEventListener("click", ()=>{
    items.forEach(items=>{
        items.classList.toggle("active")
    })
    ball.classList.toggle("active")
})
let burger=document.getElementsByClassName('burger')[0]
let links=document.getElementsByClassName('links')[0]

burger.addEventListener('click',()=>
{
    links.classList.toggle('active_link')
})

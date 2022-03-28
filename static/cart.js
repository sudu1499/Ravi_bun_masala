let b=document.getElementsByClassName('burger')[0]
let link=document.getElementsByClassName('links')[0]


//for burger
b.addEventListener('click',()=>
{
    link.classList.toggle('active_link')
})

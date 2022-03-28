let b=document.getElementsByClassName('burger')[0]
let link=document.getElementsByClassName('links')[0]
let dishes=document.getElementsByClassName("dishes")
let db=document.getElementsByClassName('db')
// let db1=document.getElementsByClassName('db1')[0]
// let db2=document.getElementsByClassName('db2')[0]


const ds_k={
    0:'bun',
    1:'nippattu',
    2:'3rd',
    4:'4'
};
//for burger
b.addEventListener('click',()=>
{
    link.classList.toggle('active_link')
})
//till here

for (let i=0;i<dishes.length;i++){
dishes[i].addEventListener('mouseenter',()=>
{ 
    db[i].classList.toggle('a_db')
})
dishes[i].addEventListener('mouseleave',()=>
{
    db[i].classList.toggle('a_db')
})

}
// dishes[0].addEventListener('mouseenter',()=>{db1.classList.toggle('a_db1')})
// dishes[0].addEventListener('mouseleave',()=>{db1.classList.toggle('a_db1')})

// dishes[1].addEventListener('mouseenter',()=>{db2.classList.toggle('a_db2')})
// dishes[1].addEventListener('mouseleave',()=>{db2.classList.toggle('a_db2')})

///////change same button name for button 
var form = document.getElementsByClassName('reply-box');
let btnShow= document.querySelectorAll('#show')
let hideForm=document.querySelectorAll('#cancel-reply')

btnShow.forEach((ele,i)=>{
    ele.addEventListener("click",  ()=> {     
        // form[i].style.height="60px"
        form[i].style.display="block"
        btnShow[i].style.display="none"
        hideForm[i].style.display="block"
    })
})
hideForm.forEach((ele,i)=>{
    ele.addEventListener("click",  ()=> {     
        form[i].style.display="none"
        btnShow[i].style.display="block"
        hideForm[i].style.display="none"
    })
})


  
    // ,


    // function hide_reply_box() {
    //     document.getElementsByClassName('reply-box')[i].style.height="0px"
    //     document.getElementsByClassName('reply-box')[i].style.display="none"
    //     document.getElementById('show').style.display="block";
    // }
    


// console.log(btn)

// var btn = document.getElementsByClassName('reply-box');

// console.log(btn);
// for (var i = 0; i < btn.length; i++) {
//     console.log(btn[i]).style["height"]="20px";
// }




// function show_reply_box() {
//     document.getElementsByClassName('reply-box')[0].style.height="60px"
//     document.getElementsByClassName('reply-box')[0].style.display="block"
//     document.getElementById('show').style.display="none";
// }


// function hide_reply_box() {
//     document.getElementsByClassName('reply-box')[0].style.height="0px"
//     document.getElementsByClassName('reply-box')[0].style.display="none"
//     document.getElementById('show').style.display="block";
// }
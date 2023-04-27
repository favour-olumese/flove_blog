// Hide and Unhide Article Reply Box

var form = document.getElementsByClassName('reply-box');
let btnShow = document.querySelectorAll('#show-reply-box')
let hideForm = document.querySelectorAll('#cancel-reply')

btnShow.forEach((ele,i)=>{
    ele.addEventListener("click",  ()=> {     
        // form[i].style.height="60px"
        form[i].style.display="block"
        btnShow[i].style.display="none"
        hideForm[i].style.display="inline"
    })
})
hideForm.forEach((ele,i)=>{
    ele.addEventListener("click",  ()=> {     
        form[i].style.display="none"
        btnShow[i].style.display="block"
        hideForm[i].style.display="none"
    })
})

// Show and Hide Comments

function show_comments() {
    document.getElementById('comment-area').style.display="block";
    document.getElementById('hide-comments').style.display="block";
    document.getElementById('show-comments').style.display="none";
}

function hide_comments() {
    document.getElementById('comment-area').style.display="none";
    document.getElementById('show-comments').style.display="block";
    document.getElementById('hide-comments').style.display="none";
}
  
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
function show_reply_box() {
    document.getElementsByClassName('reply-box').style.height="60px"
    document.getElementsByClassName('reply-box').style.display="block"
    document.getElementById('show').style.display="none";
}

function hide_reply_box() {
    document.getElementsByClassName('reply-box').style.height="0px"
    document.getElementsByClassName('reply-box').style.display="none"
}
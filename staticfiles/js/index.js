// Display and hide the menu bar
$('.user-picture').on("click", function(event) {
    if ($('#menu-bar').css("display") == 'none'){
        $('#menu-bar').css("display", "block")
    }
    else {
        $('#menu-bar').css("display", "none")
    }
});

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


// Confirms if user is logged in.
const userAuthenticated = $('#check-authenticaton').data('check_authentication')

// Redirect forms to login page if user is not authenticated
var loginPageRedirect = $('#login-page-redirect').data('login_page_redirect')

// Forms action urls
var likeFormUrl = $('#like-form-url').data('like_form_url')
var saveFormUrl = $('#save-form-url').data('save_form_url')


// Article like button 
$(document).on('submit', '#like-form', function(event){
    /*
     * Update the number of likes when the like form is submitted
     */
    event.preventDefault();

    $.ajax({

        beforeSend: function() {
        /*
         * Users are redirected to login page if there are not logged in. 
         */

            if (userAuthenticated == false) {
                window.location.href = loginPageRedirect
            }
        },

        url: likeFormUrl,
        method: "POST",

        data: {
            article_id: $('.article_id').val(),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },

        success: function(response) {
            /*
             * Changes the number of likes asynchrously.
             * @param {JSON} response - Response from the server.
             */

            if(response.status == 200) {
                function plural(word, count) {
                    /*
                     * Pluralizes the number of counts
                     * @param {string} word - Text to be pluralized.
                     * @param {integer} count - Number which determines pluralization of word. 
                     */

                    if (count === 1){
                        var likes = count + ' ' + word
                    } else {
                        var likes = count + ' ' + word + 's'
                    }
                    return likes
                }

                var likesNum = response.article_likes
                
                var likesText = plural("Like", likesNum)
                $('#likes-num').text(likesText)
                $('#like-button').val(response.button_value)
                $('#like-button').prop('title', response.title_value)
            }  else if (response.status == 302){
                window.location.href = response.writer_profile_page
            }
        },
    });
});


// For Asynchronous Saving and Unsaving of Articles
$(document).on('submit', '.save-form', function(event){
    /*
     * Bookmarks an article logged in user clicks on the form.
     */
    event.preventDefault();

    $.ajax({

        beforeSend: function() {
            /*
             * Users are redirected to login page if there are not logged in. 
             */

            if (userAuthenticated == false) {
                window.location.href = loginPageRedirect
                }
        },

        url: saveFormUrl,
        method: "POST",

        data: {
            article_id: $('.article_id').val(),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },

        success: function(response) {
                /*
                 * Changes the save button button value to save/unsave.
                 * @param {JSON} response - Response from the server.
                 */

            if(response.status == 200) {
                $('#save-button').val(response.button_value)
                $('#save-button').prop('title', response.title_value)
            } else if (response.status == 302){
                window.location.href = response.writer_profile_page
            }
        },
    });
});

// Cancel the deletion of an article
$('.delete-cancel-button').on("click", function(event) {
    /*
    * Cancels the deletion of an article and redirects to the article page.
    */

    var articlePageUrl = $('#cancel-delete-redirect-to-article').data('cancel_delete_redirect_to_article');
    window.location = articlePageUrl;
    return false;
});


// HANDLE ARTICLE PAGINATION
// Pagination of Articles in ArticleListView

var page = 1;  // Initial page number
var pagesNum = $('#article-pages-num').data('article_pages_num')
var articleUrl = $('#article-url').data('article_url')

$("#load-more-button").click(function() {
    $.ajax({
        url: articleUrl,
        data: { page: page + 1 },  // Send the next page number
        dataType: "html",  // Expecting HTML response
        success: function(data) {
            if (data) {
                var articles = ($(data).find(".article-card-cover"))

                $("#content-container").append(articles);
                page++;  // Increment the page counter
            } 
            
            if (page == pagesNum ){
                $("#load-more-button").hide();  // No more items to load
            }
        }
    });
});

// Change clipboard icon when clicked and change it back after 3 seconds.

let copyArticleLink = document.getElementById("clipboard")

copyArticleLink.addEventListener("click", function(){
    copyArticleLink.classList.remove("fa-clipboard")
    copyArticleLink.classList.remove("fa-regular")
    copyArticleLink.classList.add("fa")
    copyArticleLink.classList.add("fa-check")
    setTimeout(()=> {
        copyArticleLink.classList.remove("fa")
        copyArticleLink.classList.remove("fa-check")
        copyArticleLink.classList.add("fa-regular")
        copyArticleLink.classList.add("fa-clipboard")
    }, 3000);
});
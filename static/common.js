likeBtns = document.querySelectorAll('.blog-post .footer .buttons .like')
likeBtns.forEach(btn => {
    btn.addEventListener('click',()=>{
        likesDisplayArea = event.target.nextElementSibling;
        dislikeDisplayArea = event.target.parentNode.nextElementSibling.children[1];
        event.target.classList.toggle('liked')
        dislikeBtn = event.target.parentNode.nextElementSibling.children[0];
        if(dislikeBtn.classList.contains('disliked')){
            dislikeBtn.classList.remove('disliked');
        }
        xhr = new XMLHttpRequest()
        csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
        console.log(csrfToken)
        xhr.open('POST',event.target.getAttribute('data-url'),true)
        xhr.setRequestHeader('X-CSRFToken',csrfToken)
        xhr.setResponseType = 'json'
        xhr.onload = function(){
            console.log(this.response)
            data = JSON.parse(this.response)
            likesDisplayArea.innerHTML = data.current_likes;
            dislikeDisplayArea.innerHTML = data.current_dislikes;
        }
        data = {
            'post_id':event.target.dataset.post_id
        }

        xhr.send(JSON.stringify(data))
    })

});



dislikeBtns = document.querySelectorAll('.blog-post .footer .buttons .dislike')
dislikeBtns.forEach(btn => {
    btn.addEventListener('click',()=>{
        dislikeDisplayArea  = event.target.nextElementSibling;
        console.log(dislikeDisplayArea)
        likesDisplayArea = event.target.parentNode.previousElementSibling.children[2];
        event.target.classList.toggle('disliked');

        likeBtn = event.target.parentNode.previousElementSibling.children[1];
        if(likeBtn.classList.contains('liked')){
            likeBtn.classList.remove('liked');
        }

        xhr = new XMLHttpRequest();
        csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
        console.log(csrfToken);
        xhr.open('POST',event.target.getAttribute('data-url'),true);
        xhr.setRequestHeader('X-CSRFToken',csrfToken);
        xhr.setResponseType = 'json';
        xhr.onload = function(){
            console.log(this.response);
            data = JSON.parse(this.response);
            likesDisplayArea.innerHTML = data.current_likes;
            dislikeDisplayArea.innerHTML = data.current_dislikes;
        }
        
        data = {
            'post_id':event.target.dataset.post_id
        }

        xhr.send(JSON.stringify(data));
    })

});
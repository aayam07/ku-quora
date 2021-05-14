try{
    cancelOverlay = document.querySelector('.add-question .overlay button')
    askQuestionTriggerer = document.querySelector('.add-question .visible-part')
    askQuestionTriggerer.addEventListener('click',()=>{
        overlay = document.querySelector('.add-question .overlay')
        overlay.classList.toggle('block')
    })
    cancelOverlay.addEventListener('click',()=>{
        event.preventDefault()
        overlay = document.querySelector('.add-question .overlay')
        overlay.classList.toggle('block')
    })
    
}catch(err){
    console.log(err)
}




// profile follow functionality
try{
    followBtn = document.querySelector('.button button')
    followBtn.addEventListener('click',()=>{
        console.log(event.target.value);
        event.target.classList.toggle('followed')
        if(event.target.classList.contains('followed')){
            event.target.innerHTML='Following';
        }else{
            event.target.innerHTML='Follow';
        }
        csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
        const xhr = new XMLHttpRequest();
        xhr.open('POST',event.target.dataset.url,true);
        xhr.setRequestHeader('X-CSRFToken',csrfToken)
        xhr.onload = function(){
            data = JSON.parse(this.response)
            following = document.querySelector('.following span.count')
            follower = document.querySelector('.follower span.count')
            following.innerHTML = data.followings
            follower.innerHTML = data.followers
            console.log(this.response)

        }
        
        data = {
            'followingId':event.target.value,
        }

        xhr.send(JSON.stringify(data));

    })
}catch(err){
    console.log(err)
}








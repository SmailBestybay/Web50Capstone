export function make_post() {
    document.querySelector('form').submit();
}

export function edit_post(event) {
    const post_div = event.target.parentElement;
    const content = post_div.querySelector('#content');
    const text_area = document.createElement('textarea');
    text_area.innerHTML = content.innerHTML;
    content.innerHTML = '';
    content.append(text_area);

    const save_button = document.createElement('button');
    save_button.setAttribute('class' , 'btn btn-outline-primary mb-2')
    save_button.innerHTML = 'Save';
    const edit_button = event.target;

    save_button.addEventListener('click', (event) => {

        if (!text_area.value) {
            alert('Post must not be empty')
        } else {
            const csrftoken = getCookie('csrftoken'); // get token
            content.innerHTML = text_area.value;
            text_area.remove();
            save_button.replaceWith(edit_button);
            fetch(`/update_post/${post_div.id}`, {
                method: 'PUT',
                headers: {'X-CSRFToken': csrftoken}, // token
                mode: 'same-origin', // request mode
                body: JSON.stringify({
                    content: text_area.value
                })
            });
        }
    });

    event.target.replaceWith(save_button);
}
// get cookie from django docs
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}



export function like_unlike(event) {
    const liked = event.target.dataset.liked
    event.target.classList.toggle("fa-thumbs-down");

    // get span.innerHtml after icon element
    const count_element = event.target.nextElementSibling;
    let count = Number(count_element.innerHTML);

    // get post id from 3 parent elements up.
    const post_div = event.target.closest('.post-div')
    
    if (liked === 'true') {
        // unlike here
        event.target.dataset.liked = false;
        count_element.innerHTML = --count;

        // fetch a delete request to like_unlike view based on post id
        fetch('/like_unlike', {
            method: 'DELETE',
            body: JSON.stringify({
                id: post_div.getAttribute('id')
            })
        })
    } 
    else if (liked === 'false') {
        // like here
        event.target.dataset.liked = true;
        count_element.innerHTML = ++count;

        // fetch a post request for like based on post id
        fetch('/like_unlike', {
            method: 'POST',
            body: JSON.stringify({
                id: post_div.getAttribute('id')
            })
        })
    }
}
const forms = document.querySelectorAll('.remove form');
forms.forEach(element => element.addEventListener('submit', handleRemoveChannel));


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

async function postFormDataAsJson({url, formData}) {
    const plainFormData = Object.fromEntries(formData.entries());
    const formDataJsonString = JSON.stringify(plainFormData);
    const csrftoken = getCookie('csrftoken');
    const fetchOptions = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        mode: 'same-origin',
        body: formDataJsonString,
    };

    const response = await fetch(url, fetchOptions);
    if(!response.ok) {
        const errorMessage = await response.text();
        throw new Error(errorMessage);
    }
    return response.json();
}

async function handleRemoveChannel(event) {
    event.preventDefault();
    const form = event.currentTarget;
    const url = form.action;
    console.log(form.closest('.channel'));
    try {
        const formData = new FormData(form);
        const responseData = await postFormDataAsJson({url, formData});
        console.log({responseData});
        form.closest('.channel').remove();
        document.getElementById('add-status-message').innerHTML = responseData.message;
    } catch (error) {
        console.error(error);
        document.getElementById('add-status-message').innerHTML = responseData.message;
    }
};
window.addEventListener('DOMContentLoaded', () => {
    const forms = document.querySelectorAll('.result__dropdown form');
    forms.forEach(element => element.addEventListener('submit', handleAddChannels));
});

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
    // feels like csrf is not needed in each form because cookie csrf is used instead.
    // delete plainFormData.csrfmiddlewaretoken
    const feeds = formData.getAll('feeds');
    plainFormData.feeds = feeds;
    const formDataJsonString = JSON.stringify(plainFormData);
    const csrftoken = getCookie('csrftoken');
    const fetchOptions = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            Accept: "application/json",
            'X-CSRFToken': csrftoken,
        },
        mode: 'same-origin',
        body: formDataJsonString,
    }

    const response = await fetch(url, fetchOptions);
    if(!response.ok) {
        const errorMessage = await response.text();
        throw new Error(errorMessage);
    }
    return response.json();
}

async function handleAddChannels(event) {
    /**
     * 
     * @see https://simonplend.com/how-to-use-fetch-to-post-form-data-as-json-to-your-api/
     */
    event.preventDefault();
    // this and currentTarget are the same
    const form = event.currentTarget;
    const url = form.action;
    try {
        const formData = new FormData(form);
        const resonseData = await postFormDataAsJson({url, formData});

        console.log({ resonseData });
    } catch (error) {
        console.error(error);
    }

    // console.log([...formData.entries()]);
    // console.log([...formData.keys()]);
    // console.log(formData.getAll('feeds'));
}; 
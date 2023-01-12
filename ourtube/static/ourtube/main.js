window.addEventListener('DOMContentLoaded', (event) => {
    document.getElementById('add_feed').addEventListener('click', () => {
        document.getElementById('add_choices').classList.toggle('add_choices--show');
    });

    document.getElementById('create_form_button').addEventListener('click', () => {
        document.getElementById('create_form').classList.toggle('create_form--show');
    });

    document.getElementById('join_form_button').addEventListener('click', () => {
        console.log("join")
        document.getElementById('join_form').classList.toggle('join_form--show');
    });

});
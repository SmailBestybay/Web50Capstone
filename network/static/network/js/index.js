import {make_post, edit_post, like_unlike} from './funcs.js';

document.addEventListener('DOMContentLoaded', () => {
    
    // new post button and enter key listeners
    document.querySelector('#post-button').addEventListener('click', make_post);
    document.querySelector('#new-content').onkeypress = (event) => {
        if (!event.shiftKey) {
            if (event.code === 'Enter') {
                make_post()
            }
        }
    };

    // edit post feature
    const edit_buttons = document.querySelectorAll('#edit_post');
    edit_buttons.forEach(button => button.addEventListener('click', edit_post));

    // like feature
    const like_action = document.querySelectorAll('#like');
    like_action.forEach(button => button.addEventListener('click', like_unlike));
});
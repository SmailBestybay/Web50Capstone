import {edit_post, like_unlike} from './funcs.js';

document.addEventListener('DOMContentLoaded', () => {

    // edit post feature
    const edit_buttons = document.querySelectorAll('#edit_post');
    edit_buttons.forEach(button => button.addEventListener('click', edit_post));

    // like feature
    const like_action = document.querySelectorAll('#like');
    like_action.forEach(button => button.addEventListener('click', like_unlike));
});
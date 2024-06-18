document.addEventListener('DOMContentLoaded', () => {
    const commonInputs = [
        { id: 'id_username', placeholder: 'username' },
        { id: 'id_password', placeholder: 'password' },
        { id: 'id_password1', placeholder: 'password' },
        { id: 'id_password2', placeholder: 'retry password' }
    ];

    commonInputs.forEach(input => {
        const element = document.getElementById(input.id);
        if (element) {
            element.placeholder = input.placeholder;
            element.classList.add('textInput');
            const label = document.querySelector(`label[for='${input.id}']`);
            if (label) label.remove();
        }
    });

    const helpTexts = [
        'id_username_helptext',
        'id_password2_helptext'
    ];
    
    helpTexts.forEach(id => {
        const element = document.getElementById(id);
        if (element) element.remove();
    });
});

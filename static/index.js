document.addEventListener('DOMContentLoaded', () => {
    const roomNameInput = document.querySelector('#room-name-input');
    const roomNameSubmit = document.querySelector('#room-name-submit');
    const regex = /[\\\/^\\\/]/;

    roomNameInput.focus();

    roomNameInput.addEventListener('keyup', (e) => {
        if (e.key === 'Enter') roomNameSubmit.click();
    });

    roomNameInput.addEventListener('input', () => {
        roomNameInput.value = roomNameInput.value.replace(regex, '');
    });

    roomNameSubmit.addEventListener('click', () => {
        const roomName = roomNameInput.value;
        window.location.pathname = `/chat/${roomName}/`;
    });
});

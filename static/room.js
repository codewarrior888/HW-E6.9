document.addEventListener('DOMContentLoaded', () => {
    const chatLog = document.getElementById('chat-log');
    const roomName = JSON.parse(document.getElementById('room_name').textContent);
    const userId = JSON.parse(document.getElementById('user_id').textContent);

    function scrollToBottom() {
        chatLog.scrollTop = chatLog.scrollHeight;
    }

    scrollToBottom();

    if (chatLog.childNodes.length <= 1) {
        const emptyText = document.createElement('h3');
        emptyText.id = 'emptyText';
        emptyText.innerText = 'No Messages';
        emptyText.className = 'emptyText';
        chatLog.appendChild(emptyText);
    }

    const chatSocket = new WebSocket(`ws://${window.location.host}/ws/chat/${roomName}/`);

    chatSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        const messageElement = document.createElement('div');
        messageElement.innerHTML = `${data.user_name}: ${data.message}`;
        messageElement.classList.add('message', data.user_id === userId ? 'sender' : 'receiver');
        chatLog.appendChild(messageElement);

        const emptyText = document.getElementById('emptyText');
        if (emptyText) emptyText.remove();

        scrollToBottom();
    };

    chatSocket.onclose = () => {
        console.error('Chat socket closed unexpectedly');
    };

    const messageInput = document.getElementById('chat-message-input');
    const messageSubmit = document.getElementById('chat-message-submit');

    messageInput.focus();

    messageInput.addEventListener('keyup', (e) => {
        if (e.key === 'Enter') messageSubmit.click();
    });

    messageSubmit.addEventListener('click', () => {
        const message = messageInput.value;
        chatSocket.send(JSON.stringify({ 'message': message }));
        messageInput.value = '';
    });
});

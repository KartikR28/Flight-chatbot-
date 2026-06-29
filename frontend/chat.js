const SESSION_ID = crypto.randomUUID();
const API_URL = 'http://localhost:8000/chat';

const chatMessages = document.getElementById('chatMessages');
const chatForm = document.getElementById('chatForm');
const messageInput = document.getElementById('messageInput');
const typingIndicator = document.getElementById('typingIndicator');
const sendBtn = document.getElementById('sendBtn');

function appendMessage(content, role) {
    const wrapper = document.createElement('div');
    wrapper.className = `message ${role}`;

    const bubble = document.createElement('div');
    bubble.className = 'bubble';
    bubble.textContent = content;

    wrapper.appendChild(bubble);
    chatMessages.appendChild(wrapper);
    scrollToBottom();
}

function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function setLoading(loading) {
    sendBtn.disabled = loading;
    messageInput.disabled = loading;
    typingIndicator.style.display = loading ? 'block' : 'none';
    if (loading) scrollToBottom();
}

chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const message = messageInput.value.trim();
    if (!message) return;

    appendMessage(message, 'user');
    messageInput.value = '';
    setLoading(true);

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ session_id: SESSION_ID, message }),
        });

        if (!response.ok) {
            const err = await response.json().catch(() => ({}));
            throw new Error(err.detail || `Server error ${response.status}`);
        }

        const data = await response.json();
        appendMessage(data.reply, 'ai');
    } catch (err) {
        appendMessage(`Error: ${err.message}. Please try again.`, 'error');
    } finally {
        setLoading(false);
        messageInput.focus();
    }
});

// Allow Enter to send (Shift+Enter for newline not needed in single-line input)
messageInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        chatForm.requestSubmit();
    }
});

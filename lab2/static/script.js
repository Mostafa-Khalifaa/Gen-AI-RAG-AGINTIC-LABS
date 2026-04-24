document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    const messageInput = document.getElementById('message-input');
    const chatBox = document.getElementById('chat-box');
    const imageUpload = document.getElementById('image-upload');
    const imagePreviewContainer = document.getElementById('image-preview-container');
    const imagePreview = document.getElementById('image-preview');
    const removeImageBtn = document.getElementById('remove-image');

    let currentImageBase64 = null;

    // Handle image selection
    imageUpload.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (e) => {
                currentImageBase64 = e.target.result;
                imagePreview.src = currentImageBase64;
                imagePreviewContainer.style.display = 'inline-block';
            };
            reader.readAsDataURL(file);
        }
    });

    // Handle image removal
    removeImageBtn.addEventListener('click', () => {
        currentImageBase64 = null;
        imagePreview.src = '';
        imagePreviewContainer.style.display = 'none';
        imageUpload.value = '';
    });

    // Helper functions for chat UI
    function addUserMessage(text, imageBase64) {
        const msgDiv = document.createElement('div');
        msgDiv.className = 'message user-message';
        
        let contentHtml = '';
        if (text) {
            contentHtml += `<div>${escapeHtml(text)}</div>`;
        }
        if (imageBase64) {
            contentHtml += `<img src="${imageBase64}" class="image-attachment" alt="User upload">`;
        }
        
        msgDiv.innerHTML = `
            <div class="avatar"><i class="fa-solid fa-user"></i></div>
            <div class="content">${contentHtml}</div>
        `;
        chatBox.appendChild(msgDiv);
        scrollToBottom();
    }

    function addAiMessage(text) {
        const msgDiv = document.createElement('div');
        msgDiv.className = 'message ai-message';
        msgDiv.innerHTML = `
            <div class="avatar"><i class="fa-solid fa-stethoscope"></i></div>
            <div class="content">${escapeHtml(text).replace(/\n/g, '<br>')}</div>
        `;
        chatBox.appendChild(msgDiv);
        scrollToBottom();
    }

    function showTyping() {
        const msgDiv = document.createElement('div');
        msgDiv.className = 'message ai-message typing-indicator-container';
        msgDiv.id = 'typing';
        msgDiv.innerHTML = `
            <div class="avatar"><i class="fa-solid fa-stethoscope"></i></div>
            <div class="typing-indicator">
                <span></span><span></span><span></span>
            </div>
        `;
        chatBox.appendChild(msgDiv);
        scrollToBottom();
    }

    function removeTyping() {
        const typingIndicator = document.getElementById('typing');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }

    function scrollToBottom() {
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    function escapeHtml(unsafe) {
        return unsafe
             .replace(/&/g, "&amp;")
             .replace(/</g, "&lt;")
             .replace(/>/g, "&gt;")
             .replace(/"/g, "&quot;")
             .replace(/'/g, "&#039;");
    }

    // Main send logic
    async function sendMessage(text, imageBase64) {
        if (!text && !imageBase64) return;
        
        addUserMessage(text, imageBase64);
        
        // Reset inputs
        messageInput.value = '';
        removeImageBtn.click();
        
        showTyping();

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    text: text,
                    image: imageBase64
                })
            });

            const data = await response.json();
            removeTyping();
            
            if (response.ok) {
                addAiMessage(data.reply);
            } else {
                addAiMessage("Error: " + data.reply);
            }
        } catch (error) {
            removeTyping();
            addAiMessage("A network error occurred. Is the server running?");
            console.error(error);
        }
    }

    // Form submission
    chatForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const text = messageInput.value.trim();
        sendMessage(text, currentImageBase64);
    });
});

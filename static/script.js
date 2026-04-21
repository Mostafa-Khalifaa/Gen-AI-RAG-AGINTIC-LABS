async function sendMessage() {
    let my_input = document.getElementById('user-input');
    let img_input = document.getElementById('my-img');
    let box = document.getElementById('chat-box');
    let c_val = document.getElementById('creativity').value;
    let l_val = document.getElementById('length').value;
    
    let msg = my_input.value.trim();
    let file = img_input.files[0];
    
    if (!msg && !file) return;
    let display_msg = msg ? msg : "[Image attached]";
    const userMessageHTML = `
        <div class="message user-message">
            <div class="message-content">
                <div class="message-text">${escapeHtml(display_msg)}</div>
            </div>
        </div>
    `;
    box.innerHTML += userMessageHTML;
    
    // Clear inputs
    my_input.value = '';
    img_input.value = '';
    box.scrollTop = box.scrollHeight;

    // Prepare request
    let my_form = new FormData();
    my_form.append('text', msg);
    my_form.append('creativity', c_val);
    my_form.append('length', l_val);
    if (file) {
        my_form.append('image', file);
    }

    // Show loading indicator
    const loadingHTML = `
        <div class="message chef-message">
            <div class="message-avatar"></div>
            <div class="message-content">
                <div class="message-text" style="opacity: 0.6;">Chef is thinking...</div>
            </div>
        </div>
    `;
    box.innerHTML += loadingHTML;
    box.scrollTop = box.scrollHeight;

    try {
        let res = await fetch('/chat', {
            method: 'POST',
            body: my_form
        });

        let out = await res.json();
        
        // Remove loading message and add actual response
        let lastMessage = box.lastChild;
        if (lastMessage) lastMessage.remove();
        
        const chefMessageHTML = `
            <div class="message chef-message">
                <div class="message-avatar"></div>
                <div class="message-content">
                    <div class="message-text">${out.answer}</div>
                </div>
            </div>
        `;
        box.innerHTML += chefMessageHTML;
        box.scrollTop = box.scrollHeight;
    } catch (error) {
        console.error('Error:', error);
        let lastMessage = box.lastChild;
        if (lastMessage) lastMessage.remove();
        
        const errorHTML = `
            <div class="message chef-message">
                <div class="message-avatar"></div>
                <div class="message-content">
                    <div class="message-text" style="color: #d32f2f;">Sorry, something went wrong. Please try again.</div>
                </div>
            </div>
        `;
        box.innerHTML += errorHTML;
        box.scrollTop = box.scrollHeight;
    }
}

// Utility function to escape HTML
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('user-input').addEventListener('keypress', function(event) {
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault();
            sendMessage();
        }
    });
});
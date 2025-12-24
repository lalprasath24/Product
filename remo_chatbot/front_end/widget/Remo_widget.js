/*
 *Remo_widget.js
 * Logic for the modular Remo Chatbot widget.
 */

document.addEventListener('DOMContentLoaded', () => {
    
    // --- Configuration ---
    const API_URL = "http://localhost:8000";
    
    // --- DOM Elements ---
    const floatingIcon = document.getElementById('floating-icon');
    const chatWindow = document.getElementById('chat-window');
    const closeBtn = document.getElementById('close-btn');
    const configBtn = document.getElementById('config-btn');
    const configModal = document.getElementById('config-modal');
    const closeModalBtn = document.getElementById('close-modal-btn');
    const dbConfigForm = document.getElementById('db-config-form');
    const configStatus = document.getElementById('config-status');
    const chatBox = document.getElementById('chat-box');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');

    let isConnected = false;
    let typingIndicator = null;

    // --- A. WIDGET INTERACTION ---

    floatingIcon.addEventListener('click', () => {
        chatWindow.classList.toggle('active');
    });
    closeBtn.addEventListener('click', () => {
        chatWindow.classList.remove('active');
    });

    // Open/Close Configuration Modal
    configBtn.addEventListener('click', () => {
        chatWindow.classList.remove('active'); 
        configModal.style.display = 'flex';
    });
    closeModalBtn.addEventListener('click', () => {
        configModal.style.display = 'none';
    });
    // Close modal on outside click
    configModal.addEventListener('click', (e) => {
        if (e.target === configModal) {
            configModal.style.display = 'none';
        }
    });

    // --- B. HELPER FUNCTIONS ---

    function addMessage(sender, text) {
        if (typingIndicator) {
            chatBox.removeChild(typingIndicator);
            typingIndicator = null;
        }
        const msgDiv = document.createElement('div');
        msgDiv.className = sender;
        msgDiv.textContent = text;
        chatBox.appendChild(msgDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    function showTypingIndicator() {
        if (!typingIndicator) {
            typingIndicator = document.createElement('div');
            typingIndicator.className = 'bot typing';
            typingIndicator.textContent = 'Remo is typing...';
            chatBox.appendChild(typingIndicator);
            chatBox.scrollTop = chatBox.scrollHeight;
        }
    }

    function setChatState(enabled, message) {
        isConnected = enabled;
        userInput.disabled = !enabled;
        sendBtn.disabled = !enabled;
        if (message) {
             addMessage('bot', message);
        }
    }
    
    // --- C. DATABASE CONFIGURATION LOGIC ---
    
    dbConfigForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        configStatus.textContent = 'Connecting...';
        configStatus.style.color = 'blue';

        const config = {
            db_type: document.getElementById('db-type').value,
            host: document.getElementById('db-host').value,
            port: parseInt(document.getElementById('db-port').value) || (document.getElementById('db-type').value === 'postgres' ? 5432 : 3306),
            dbname: document.getElementById('db-name').value,
            user: document.getElementById('db-user').value,
            password: document.getElementById('db-pass').value
        };

        // Save config to Local Storage
        localStorage.setItem('RemoDbConfig', JSON.stringify(config));

        try {
            const response = await fetch(`${API_URL}/configure-db`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(config)
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Connection failed');
            }

            const data = await response.json();
            configStatus.textContent = data.message;
            configStatus.style.color = 'green';
            configModal.style.display = 'none'; 
            setChatState(true, `✅ ${data.message} You can now ask questions.`);

        } catch (error) {
            configStatus.textContent = `Error: ${error.message}`;
            configStatus.style.color = 'red';
            setChatState(false, 'Connection failed. Please check credentials and try again.');
        }
    });

    // Load and attempt to auto-reconnect with saved config on startup
    (function loadAndReconnect() {
        const savedConfig = localStorage.getItem('RemoDbConfig');
        if (savedConfig) {
            const config = JSON.parse(savedConfig);
            // Pre-fill form fields
            document.getElementById('db-type').value = config.db_type || 'postgres';
            document.getElementById('db-host').value = config.host || '';
            document.getElementById('db-port').value = config.port || '';
            document.getElementById('db-name').value = config.dbname || '';
            document.getElementById('db-user').value = config.user || '';
            document.getElementById('db-pass').value = config.password || ''; 
            
            // Attempt auto-reconnect
            // Note: In a real app, this should probably happen quietly
            // For now, let's keep it manual to avoid silent failures on demo startup.
        }
    })();


    // --- D. CHAT MESSAGE SENDING LOGIC ---

    sendBtn.addEventListener('click', sendMessage);
    userInput.addEventListener('keyup', (e) => {
        if (e.key === 'Enter') sendMessage();
    });

    async function sendMessage() {
        const question = userInput.value.trim();
        if (!question || !isConnected) return;

        addMessage('user', question);
        userInput.value = '';
        showTypingIndicator(); 

        try {
            const response = await fetch(`${API_URL}/chat`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ question: question })
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Failed to get answer');
            }

            const data = await response.json();
            addMessage('bot', data.answer);

        } catch (error) {
            addMessage('bot', `🚨 Error: ${error.message}`);
        } finally {
            // Ensure typing indicator is removed after response/error
            if (typingIndicator && chatBox.contains(typingIndicator)) {
                chatBox.removeChild(typingIndicator);
                typingIndicator = null;
            }
        }
    }
});
class OrbitXChatbot {
    constructor() {
        this.conversationId = this.getOrCreateConversationId();
        this.isOpen = false;
        this.isTyping = false;
        this.userInfo = this.getUserInfo();
        this.init();
    }

    getOrCreateConversationId() {
        let conversationId = localStorage.getItem('orbitx_conversation_id');
        if (!conversationId) {
            conversationId = 'conv_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
            localStorage.setItem('orbitx_conversation_id', conversationId);
        }
        return conversationId;
    }

    getUserInfo() {
        return {
            name: localStorage.getItem('orbitx_user_name') || null,
            email: localStorage.getItem('orbitx_user_email') || null,
            phone: localStorage.getItem('orbitx_user_phone') || null,
            session_id: this.conversationId
        };
    }

    saveUserInfo(info) {
        if (info.name) {
            localStorage.setItem('orbitx_user_name', info.name);
            this.userInfo.name = info.name;
        }
        if (info.email) {
            localStorage.setItem('orbitx_user_email', info.email);
            this.userInfo.email = info.email;
        }
        if (info.phone) {
            localStorage.setItem('orbitx_user_phone', info.phone);
            this.userInfo.phone = info.phone;
        }
    }

    init() {
        this.createChatWidget();
        this.attachEventListeners();
        this.loadConversationHistory();
    }

    createChatWidget() {
        const chatHTML = `
            <div id="orbitx-chatbot" class="orbitx-chatbot">
                <!-- Chat Toggle Button -->
                <button id="chat-toggle" class="chat-toggle" title="Chat with OrbitX AI">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M20 2H4C2.9 2 2 2.9 2 4V22L6 18H20C21.1 18 22 17.1 22 16V4C22 2.9 21.1 2 20 2ZM20 16H5.17L4 17.17V4H20V16Z" fill="currentColor"/>
                        <circle cx="12" cy="10" r="1.5" fill="currentColor"/>
                        <circle cx="8" cy="10" r="1.5" fill="currentColor"/>
                        <circle cx="16" cy="10" r="1.5" fill="currentColor"/>
                    </svg>
                    <span class="chat-notification" id="chat-notification">1</span>
                </button>

                <!-- Chat Window -->
                <div id="chat-window" class="chat-window">
                    <div class="chat-header">
                        <div class="chat-header-info">
                            <div class="chat-avatar">
                                <div class="avatar-icon">AI</div>
                                <div class="status-indicator"></div>
                            </div>
                            <div class="chat-title">
                                <h4>OrbitX AI Assistant</h4>
                                <span class="chat-status">Online • Ready to help</span>
                            </div>
                        </div>
                        <button id="chat-close" class="chat-close">
                            <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                                <path d="M15 5L5 15M5 5L15 15" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                            </svg>
                        </button>
                    </div>

                    <div class="chat-messages" id="chat-messages">
                        <!-- Welcome Message -->
                        <div class="message bot-message">
                            <div class="message-avatar">
                                <div class="avatar-icon">AI</div>
                            </div>
                            <div class="message-content">
                                <div class="message-bubble">
                                    <p>👋 Hi there! I'm your OrbitX AI Assistant.</p>
                                    <p>I can help you:</p>
                                    <ul>
                                        <li>🎨 Start a design project</li>
                                        <li>💰 Get instant quotes</li>
                                        <li>📁 View our portfolio</li>
                                        <li>📞 Connect with our team</li>
                                    </ul>
                                    <p>What can I help you with today?</p>
                                </div>
                                <div class="message-time">${this.formatTime(new Date())}</div>
                            </div>
                        </div>
                    </div>

                    <div class="chat-input-section">
                        <!-- Quick Actions -->
                        <div class="quick-actions" id="quick-actions">
                            <button class="quick-action" data-message="I need a logo design">
                                🎨 Logo Design
                            </button>
                            <button class="quick-action" data-message="How much for a website?">
                                💰 Get Quote
                            </button>
                            <button class="quick-action" data-message="Show me your portfolio">
                                📁 Portfolio
                            </button>
                            <button class="quick-action" data-message="What services do you offer?">
                                📋 Services
                            </button>
                        </div>

                        <!-- Typing Indicator -->
                        <div class="typing-indicator" id="typing-indicator" style="display: none;">
                            <div class="typing-dots">
                                <span></span>
                                <span></span>
                                <span></span>
                            </div>
                            <span class="typing-text">OrbitX AI is typing...</span>
                        </div>

                        <!-- Input Area -->
                        <div class="chat-input-container">
                            <div class="chat-input-wrapper">
                                <input
                                    type="text"
                                    id="chat-input"
                                    class="chat-input"
                                    placeholder="Type your message..."
                                    maxlength="500"
                                />
                                <button id="chat-send" class="chat-send" title="Send message">
                                    <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                                        <path d="M18 2L1 9L7 11L9 17L18 2Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                                    </svg>
                                </button>
                            </div>
                            <div class="chat-input-footer">
                                <small>Press Enter to send • Powered by OrbitX AI</small>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;

        // Insert chatbot HTML
        document.body.insertAdjacentHTML('beforeend', chatHTML);

        // Add CSS
        this.addChatbotStyles();
    }

    addChatbotStyles() {
        const styles = `
            <style>
                .orbitx-chatbot {
                    position: fixed;
                    bottom: 20px;
                    right: 20px;
                    z-index: 9999;
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                }

                .chat-toggle {
                    width: 60px;
                    height: 60px;
                    border-radius: 50%;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    border: none;
                    color: white;
                    cursor: pointer;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    box-shadow: 0 4px 20px rgba(102, 126, 234, 0.4);
                    transition: all 0.3s ease;
                    position: relative;
                }

                .chat-toggle:hover {
                    transform: scale(1.1);
                    box-shadow: 0 6px 25px rgba(102, 126, 234, 0.6);
                }

                .chat-notification {
                    position: absolute;
                    top: -5px;
                    right: -5px;
                    background: #ff4757;
                    color: white;
                    border-radius: 50%;
                    width: 24px;
                    height: 24px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 12px;
                    font-weight: bold;
                    animation: pulse 2s infinite;
                }

                @keyframes pulse {
                    0% { transform: scale(1); }
                    50% { transform: scale(1.1); }
                    100% { transform: scale(1); }
                }

                .chat-window {
                    position: fixed;
                    bottom: 80px;
                    right: 20px;
                    width: 380px;
                    height: calc(100vh - 160px);
                    max-height: 700px;
                    background: white;
                    border-radius: 20px;
                    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
                    display: none;
                    flex-direction: column;
                    overflow: hidden;
                    transform: scale(0.8) translateY(20px);
                    opacity: 0;
                    transition: all 0.3s ease;
                    z-index: 9998;
                }

                .chat-window.open {
                    display: flex;
                    transform: scale(1) translateY(0);
                    opacity: 1;
                }

                .chat-header {
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 20px;
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                }

                .chat-header-info {
                    display: flex;
                    align-items: center;
                }

                .chat-avatar {
                    position: relative;
                    margin-right: 12px;
                }

                .avatar-icon {
                    width: 40px;
                    height: 40px;
                    background: rgba(255, 255, 255, 0.2);
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-weight: bold;
                    font-size: 14px;
                }

                .status-indicator {
                    position: absolute;
                    bottom: 2px;
                    right: 2px;
                    width: 12px;
                    height: 12px;
                    background: #2ed573;
                    border: 2px solid white;
                    border-radius: 50%;
                }

                .chat-title h4 {
                    margin: 0;
                    font-size: 16px;
                    font-weight: 600;
                }

                .chat-status {
                    font-size: 12px;
                    opacity: 0.9;
                }

                .chat-close {
                    background: none;
                    border: none;
                    color: white;
                    cursor: pointer;
                    padding: 8px;
                    border-radius: 50%;
                    transition: background 0.2s;
                }

                .chat-close:hover {
                    background: rgba(255, 255, 255, 0.1);
                }

                .chat-messages {
                    flex: 1;
                    overflow-y: auto;
                    padding: 20px;
                    background: #f8f9fa;
                }

                .message {
                    display: flex;
                    margin-bottom: 20px;
                    animation: messageSlideIn 0.3s ease;
                }

                @keyframes messageSlideIn {
                    from {
                        opacity: 0;
                        transform: translateY(10px);
                    }
                    to {
                        opacity: 1;
                        transform: translateY(0);
                    }
                }

                .user-message {
                    justify-content: flex-end;
                }

                .user-message .message-content {
                    order: -1;
                }

                .message-avatar {
                    margin: 0 8px;
                }

                .message-avatar .avatar-icon {
                    width: 32px;
                    height: 32px;
                    font-size: 12px;
                    background: #667eea;
                    color: white;
                }

                .user-message .message-avatar .avatar-icon {
                    background: #2f3542;
                }

                .message-content {
                    max-width: 70%;
                }

                .message-bubble {
                    background: white;
                    padding: 12px 16px;
                    border-radius: 18px;
                    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
                    word-wrap: break-word;
                }

                .user-message .message-bubble {
                    background: #667eea;
                    color: white;
                }

                .message-bubble p {
                    margin: 0 0 8px 0;
                }

                .message-bubble p:last-child {
                    margin-bottom: 0;
                }

                .message-bubble ul {
                    margin: 8px 0;
                    padding-left: 20px;
                }

                .message-bubble li {
                    margin: 4px 0;
                }

                .message-time {
                    font-size: 11px;
                    color: #8e9297;
                    margin-top: 4px;
                    text-align: center;
                }

                .quick-actions {
                    display: flex;
                    flex-wrap: wrap;
                    gap: 8px;
                    padding: 16px 20px 8px;
                    background: white;
                }

                .quick-action {
                    background: #f1f3f4;
                    border: 1px solid #e1e4e6;
                    border-radius: 20px;
                    padding: 8px 12px;
                    font-size: 12px;
                    cursor: pointer;
                    transition: all 0.2s;
                    color: #5f6368;
                }

                .quick-action:hover {
                    background: #667eea;
                    color: white;
                    border-color: #667eea;
                }

                .typing-indicator {
                    background: white;
                    padding: 12px 20px;
                    display: flex;
                    align-items: center;
                    gap: 8px;
                }

                .typing-dots {
                    display: flex;
                    gap: 4px;
                }

                .typing-dots span {
                    width: 8px;
                    height: 8px;
                    background: #667eea;
                    border-radius: 50%;
                    animation: typingBounce 1.4s infinite ease-in-out;
                }

                .typing-dots span:nth-child(1) { animation-delay: -0.32s; }
                .typing-dots span:nth-child(2) { animation-delay: -0.16s; }

                @keyframes typingBounce {
                    0%, 80%, 100% {
                        transform: scale(0.8);
                        opacity: 0.5;
                    }
                    40% {
                        transform: scale(1);
                        opacity: 1;
                    }
                }

                .typing-text {
                    font-size: 12px;
                    color: #8e9297;
                }

                .chat-input-container {
                    background: white;
                    border-top: 1px solid #e1e4e6;
                }

                .chat-input-wrapper {
                    display: flex;
                    align-items: center;
                    padding: 16px 20px;
                    gap: 12px;
                }

                .chat-input {
                    flex: 1;
                    border: 1px solid #e1e4e6;
                    border-radius: 20px;
                    padding: 10px 16px;
                    font-size: 14px;
                    outline: none;
                    transition: border-color 0.2s;
                }

                .chat-input:focus {
                    border-color: #667eea;
                }

                .chat-send {
                    background: #667eea;
                    border: none;
                    border-radius: 50%;
                    width: 40px;
                    height: 40px;
                    color: white;
                    cursor: pointer;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    transition: all 0.2s;
                }

                .chat-send:hover {
                    background: #5a67d8;
                    transform: scale(1.05);
                }

                .chat-send:disabled {
                    background: #ccc;
                    cursor: not-allowed;
                    transform: none;
                }

                .chat-input-footer {
                    padding: 8px 20px 16px;
                    text-align: center;
                }

                .chat-input-footer small {
                    color: #8e9297;
                    font-size: 11px;
                }

                /* Mobile Responsive */
                @media (max-width: 480px) {
                    .orbitx-chatbot {
                        bottom: 10px;
                        right: 10px;
                    }

                    .chat-window {
                        width: calc(100vw - 20px);
                        height: calc(100vh - 140px);
                        right: -10px;
                        bottom: 70px;
                        max-height: none;
                    }

                    .chat-toggle {
                        width: 50px;
                        height: 50px;
                    }
                }
            </style>
        `;

        document.head.insertAdjacentHTML('beforeend', styles);
    }

    attachEventListeners() {
        const toggleBtn = document.getElementById('chat-toggle');
        const closeBtn = document.getElementById('chat-close');
        const sendBtn = document.getElementById('chat-send');
        const input = document.getElementById('chat-input');
        const quickActions = document.getElementById('quick-actions');

        toggleBtn.addEventListener('click', () => this.toggleChat());
        closeBtn.addEventListener('click', () => this.closeChat());
        sendBtn.addEventListener('click', () => this.sendMessage());

        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });

        // Quick action buttons
        quickActions.addEventListener('click', (e) => {
            if (e.target.classList.contains('quick-action')) {
                const message = e.target.getAttribute('data-message');
                this.sendQuickMessage(message);
            }
        });

        // Hide notification when chat is opened
        toggleBtn.addEventListener('click', () => {
            document.getElementById('chat-notification').style.display = 'none';
        });
    }

    toggleChat() {
        const chatWindow = document.getElementById('chat-window');
        this.isOpen = !this.isOpen;

        if (this.isOpen) {
            chatWindow.classList.add('open');
            document.getElementById('chat-input').focus();
        } else {
            chatWindow.classList.remove('open');
        }
    }

    closeChat() {
        const chatWindow = document.getElementById('chat-window');
        chatWindow.classList.remove('open');
        this.isOpen = false;
    }

    async sendMessage() {
        const input = document.getElementById('chat-input');
        const message = input.value.trim();

        if (!message || this.isTyping) return;

        // Add user message to chat
        this.addMessage(message, 'user');
        input.value = '';

        // Show typing indicator
        this.showTyping();

        try {
            const response = await this.sendToAPI(message);
            this.hideTyping();

            if (response.success) {
                this.addMessage(response.bot_response, 'bot');

                // Handle quote creation
                if (response.quote_created) {
                    this.addMessage("🎉 Great! I've created a quote request for you. Our team will be in touch within 2 hours!", 'bot');
                }
            } else {
                this.addMessage(response.bot_response || "Sorry, I couldn't process your message. Please try again.", 'bot');
            }
        } catch (error) {
            this.hideTyping();
            this.addMessage("I'm having trouble connecting right now. Please try again in a moment.", 'bot');
            console.error('Chatbot error:', error);
        }
    }

    sendQuickMessage(message) {
        const input = document.getElementById('chat-input');
        input.value = message;
        this.sendMessage();
    }

    async sendToAPI(message) {
        const response = await fetch('/api/chatbot/message', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                conversation_id: this.conversationId,
                user_info: this.userInfo
            })
        });

        return await response.json();
    }

    addMessage(message, sender) {
        const messagesContainer = document.getElementById('chat-messages');
        const messageTime = this.formatTime(new Date());

        const messageHTML = `
            <div class="message ${sender}-message">
                <div class="message-avatar">
                    <div class="avatar-icon">${sender === 'bot' ? 'AI' : 'U'}</div>
                </div>
                <div class="message-content">
                    <div class="message-bubble">
                        ${this.formatMessage(message)}
                    </div>
                    <div class="message-time">${messageTime}</div>
                </div>
            </div>
        `;

        messagesContainer.insertAdjacentHTML('beforeend', messageHTML);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    formatMessage(message) {
        // Convert newlines to <br> and handle basic formatting
        return message
            .replace(/\n/g, '<br>')
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>');
    }

    formatTime(date) {
        return date.toLocaleTimeString('en-US', {
            hour: 'numeric',
            minute: '2-digit',
            hour12: true
        });
    }

    showTyping() {
        this.isTyping = true;
        document.getElementById('typing-indicator').style.display = 'flex';
        document.getElementById('chat-send').disabled = true;
    }

    hideTyping() {
        this.isTyping = false;
        document.getElementById('typing-indicator').style.display = 'none';
        document.getElementById('chat-send').disabled = false;
    }

    async loadConversationHistory() {
        try {
            const response = await fetch(`/api/chatbot/history/${this.conversationId}`);
            const data = await response.json();

            if (data.success && data.messages.length > 0) {
                const messagesContainer = document.getElementById('chat-messages');
                // Clear welcome message if we have history
                messagesContainer.innerHTML = '';

                data.messages.forEach(msg => {
                    this.addMessage(msg.message, msg.sender);
                });
            }
        } catch (error) {
            console.log('No previous conversation history');
        }
    }
}

// Initialize chatbot when page loads
document.addEventListener('DOMContentLoaded', function() {
    // Only initialize if not already initialized
    if (!window.orbitxChatbot) {
        window.orbitxChatbot = new OrbitXChatbot();
    }
});
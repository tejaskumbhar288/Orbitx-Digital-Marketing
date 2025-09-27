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
                    <div class="ai-orb">
                        <div class="orb-core">
                            <div class="orb-inner"></div>
                            <div class="orb-particles">
                                <div class="particle"></div>
                                <div class="particle"></div>
                                <div class="particle"></div>
                                <div class="particle"></div>
                            </div>
                        </div>
                        <div class="orb-glow"></div>
                    </div>
                    <span class="chat-notification" id="chat-notification">1</span>
                </button>

                <!-- Chat Window -->
                <div id="chat-window" class="chat-window">
                    <div class="chat-header">
                        <div class="chat-header-info">
                            <div class="chat-avatar">
                                <div class="ai-avatar-orb">
                                    <div class="avatar-core">
                                        <div class="avatar-inner"></div>
                                        <div class="avatar-sparkles">
                                            <div class="sparkle"></div>
                                            <div class="sparkle"></div>
                                            <div class="sparkle"></div>
                                        </div>
                                    </div>
                                </div>
                                <div class="status-indicator-pulse"></div>
                            </div>
                            <div class="chat-title">
                                <h4>OrbitX AI Assistant</h4>
                                <span class="chat-status">
                                    <span class="status-dot"></span>
                                    Online • Ready to help with your projects
                                </span>
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
                        <div class="message bot-message welcome-message">
                            <div class="message-avatar">
                                <div class="message-ai-orb">
                                    <div class="message-orb-core">
                                        <div class="message-orb-inner"></div>
                                    </div>
                                </div>
                            </div>
                            <div class="message-content">
                                <div class="message-bubble ai-bubble">
                                    <div class="bubble-glow"></div>
                                    <div class="bubble-content">
                                        <p class="greeting-text">✨ Hello! I'm your OrbitX AI Assistant</p>
                                        <p class="capabilities-intro">I'm here to help you with:</p>
                                        <div class="capability-grid">
                                            <div class="capability-item">
                                                <span class="capability-icon">🎨</span>
                                                <span>Design Projects</span>
                                            </div>
                                            <div class="capability-item">
                                                <span class="capability-icon">💰</span>
                                                <span>Instant Quotes</span>
                                            </div>
                                            <div class="capability-item">
                                                <span class="capability-icon">📁</span>
                                                <span>Portfolio Showcase</span>
                                            </div>
                                            <div class="capability-item">
                                                <span class="capability-icon">🚀</span>
                                                <span>Project Launch</span>
                                            </div>
                                        </div>
                                        <p class="cta-text">What creative project can I help you with today?</p>
                                    </div>
                                </div>
                                <div class="message-time">${this.formatTime(new Date())}</div>
                            </div>
                        </div>
                    </div>

                    <div class="chat-input-section">
                        <!-- Smart Quick Actions -->
                        <div class="smart-actions" id="quick-actions">
                            <div class="action-category">
                                <div class="action-buttons quick-action-grid">
                                    <button class="smart-action primary compact" data-message="I need a professional logo design for my business">
                                        <span class="action-icon">🎨</span>
                                        <span class="action-text">Logo</span>
                                    </button>
                                    <button class="smart-action secondary compact" data-message="How much would a modern website cost?">
                                        <span class="action-icon">💻</span>
                                        <span class="action-text">Website</span>
                                    </button>
                                    <button class="smart-action tertiary compact" data-message="Show me your best portfolio work">
                                        <span class="action-icon">✨</span>
                                        <span class="action-text">Portfolio</span>
                                    </button>
                                    <button class="smart-action quaternary compact" data-message="What digital marketing services do you offer?">
                                        <span class="action-icon">🚀</span>
                                        <span class="action-text">Services</span>
                                    </button>
                                </div>
                            </div>
                        </div>

                        <!-- AI Thinking Indicator -->
                        <div class="ai-thinking-indicator" id="typing-indicator" style="display: none;">
                            <div class="thinking-avatar">
                                <div class="thinking-orb">
                                    <div class="thinking-core"></div>
                                    <div class="thinking-pulse"></div>
                                </div>
                            </div>
                            <div class="thinking-content">
                                <div class="thinking-dots">
                                    <span class="dot"></span>
                                    <span class="dot"></span>
                                    <span class="dot"></span>
                                </div>
                                <span class="thinking-text">OrbitX AI is crafting your response...</span>
                            </div>
                        </div>

                        <!-- Input Area -->
                        <div class="chat-input-container">
                            <div class="modern-input-wrapper">
                                <div class="input-container">
                                    <input
                                        type="text"
                                        id="chat-input"
                                        class="modern-chat-input"
                                        placeholder="Ask me anything about your design needs..."
                                        maxlength="500"
                                    />
                                    <div class="input-actions">
                                        <button id="voice-input" class="voice-btn" title="Voice input (coming soon)" disabled>
                                            <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
                                                <path d="M12 1C10.34 1 9 2.34 9 4V12C9 13.66 10.34 15 12 15S15 13.66 15 12V4C15 2.34 13.66 1 12 1Z" fill="currentColor"/>
                                                <path d="M19 10V12C19 16.42 15.42 20 11 20H9V22H15C19.42 22 23 18.42 23 14V10H19Z" fill="currentColor"/>
                                                <path d="M5 10V12C5 16.42 8.58 20 13 20H15V22H9C4.58 22 1 18.42 1 14V10H5Z" fill="currentColor"/>
                                            </svg>
                                        </button>
                                        <button id="chat-send" class="modern-send-btn" title="Send message">
                                            <div class="send-icon">
                                                <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
                                                    <path d="M22 2L11 13" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                                                    <path d="M22 2L15 22L11 13L2 9L22 2Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                                                </svg>
                                            </div>
                                            <div class="send-glow"></div>
                                        </button>
                                    </div>
                                </div>
                                <div class="input-footer">
                                    <div class="footer-left">
                                        <span class="ai-status">
                                            <span class="status-indicator-mini"></span>
                                            AI Ready
                                        </span>
                                    </div>
                                    <div class="footer-right">
                                        <span class="powered-by">Powered by OrbitX AI ✨</span>
                                    </div>
                                </div>
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
                /* ===== MODERN AI CHATBOT STYLES ===== */
                :root {
                    --chatbot-primary: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    --chatbot-secondary: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                    --chatbot-ai-glow: #4facfe;
                    --chatbot-ai-core: #00f2fe;
                    --chatbot-dark: #1a1a2e;
                    --chatbot-dark-light: #16213e;
                    --chatbot-text: #ffffff;
                    --chatbot-text-muted: rgba(255, 255, 255, 0.7);
                    --chatbot-glass: rgba(255, 255, 255, 0.1);
                    --chatbot-border: rgba(255, 255, 255, 0.2);
                }

                .orbitx-chatbot {
                    position: fixed;
                    bottom: 20px;
                    right: 20px;
                    z-index: 9999;
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Inter', sans-serif;
                }

                /* ===== AI ORB TOGGLE BUTTON ===== */
                .chat-toggle {
                    width: 70px;
                    height: 70px;
                    border-radius: 50%;
                    background: var(--chatbot-dark);
                    border: 2px solid var(--chatbot-border);
                    cursor: pointer;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3), 0 0 0 1px rgba(255, 255, 255, 0.1);
                    transition: all 0.4s cubic-bezier(0.23, 1, 0.32, 1);
                    position: relative;
                    backdrop-filter: blur(20px);
                    overflow: hidden;
                }

                .ai-orb {
                    position: relative;
                    width: 100%;
                    height: 100%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                }

                .orb-core {
                    position: relative;
                    width: 32px;
                    height: 32px;
                    border-radius: 50%;
                    background: var(--chatbot-ai-glow);
                    background: linear-gradient(45deg, var(--chatbot-ai-glow), var(--chatbot-ai-core));
                    animation: orbPulse 2s ease-in-out infinite;
                }

                .orb-inner {
                    position: absolute;
                    top: 50%;
                    left: 50%;
                    transform: translate(-50%, -50%);
                    width: 16px;
                    height: 16px;
                    background: rgba(255, 255, 255, 0.9);
                    border-radius: 50%;
                    animation: innerGlow 3s ease-in-out infinite;
                }

                .orb-glow {
                    position: absolute;
                    top: -10px;
                    left: -10px;
                    right: -10px;
                    bottom: -10px;
                    background: radial-gradient(circle, var(--chatbot-ai-glow) 0%, transparent 70%);
                    border-radius: 50%;
                    opacity: 0.6;
                    animation: glowPulse 2s ease-in-out infinite;
                }

                .orb-particles {
                    position: absolute;
                    top: 0;
                    left: 0;
                    right: 0;
                    bottom: 0;
                }

                .particle {
                    position: absolute;
                    width: 3px;
                    height: 3px;
                    background: var(--chatbot-ai-core);
                    border-radius: 50%;
                    opacity: 0.8;
                }

                .particle:nth-child(1) {
                    top: 20%;
                    left: 20%;
                    animation: particleFloat 4s ease-in-out infinite;
                }

                .particle:nth-child(2) {
                    top: 30%;
                    right: 20%;
                    animation: particleFloat 4s ease-in-out infinite 1s;
                }

                .particle:nth-child(3) {
                    bottom: 20%;
                    left: 30%;
                    animation: particleFloat 4s ease-in-out infinite 2s;
                }

                .particle:nth-child(4) {
                    bottom: 30%;
                    right: 30%;
                    animation: particleFloat 4s ease-in-out infinite 3s;
                }

                .chat-toggle:hover {
                    transform: scale(1.05);
                    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4), 0 0 20px var(--chatbot-ai-glow);
                }

                .chat-toggle:hover .orb-core {
                    animation-duration: 1s;
                }

                .chat-toggle:hover .orb-glow {
                    opacity: 1;
                    animation-duration: 1s;
                }

                /* ===== KEYFRAME ANIMATIONS ===== */
                @keyframes orbPulse {
                    0%, 100% { transform: scale(1); }
                    50% { transform: scale(1.1); }
                }

                @keyframes innerGlow {
                    0%, 100% { opacity: 0.9; transform: translate(-50%, -50%) scale(1); }
                    50% { opacity: 1; transform: translate(-50%, -50%) scale(1.2); }
                }

                @keyframes glowPulse {
                    0%, 100% { opacity: 0.6; transform: scale(1); }
                    50% { opacity: 1; transform: scale(1.1); }
                }

                @keyframes particleFloat {
                    0%, 100% { transform: translateY(0px) scale(1); opacity: 0.8; }
                    25% { transform: translateY(-8px) scale(1.2); opacity: 1; }
                    50% { transform: translateY(-4px) scale(0.8); opacity: 0.6; }
                    75% { transform: translateY(-12px) scale(1.1); opacity: 0.9; }
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

                /* ===== MODERN CHAT WINDOW ===== */
                .chat-window {
                    position: fixed;
                    bottom: 100px;
                    right: 20px;
                    width: 400px;
                    height: calc(100vh - 160px);
                    max-height: 720px;
                    background: var(--chatbot-dark);
                    backdrop-filter: blur(20px);
                    border: 1px solid var(--chatbot-border);
                    border-radius: 24px;
                    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4), 0 0 0 1px rgba(255, 255, 255, 0.1);
                    display: none;
                    flex-direction: column;
                    overflow: hidden;
                    transform: scale(0.9) translateY(30px);
                    opacity: 0;
                    transition: all 0.4s cubic-bezier(0.23, 1, 0.32, 1);
                    z-index: 9998;
                }

                .chat-window.open {
                    display: flex;
                    transform: scale(1) translateY(0);
                    opacity: 1;
                }

                /* ===== CHAT HEADER WITH AI AVATAR ===== */
                .chat-header {
                    background: linear-gradient(135deg, var(--chatbot-dark-light) 0%, var(--chatbot-dark) 100%);
                    color: var(--chatbot-text);
                    padding: 24px;
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                    border-bottom: 1px solid var(--chatbot-border);
                    position: relative;
                }

                .chat-header::before {
                    content: '';
                    position: absolute;
                    top: 0;
                    left: 0;
                    right: 0;
                    height: 1px;
                    background: linear-gradient(90deg, transparent, var(--chatbot-ai-glow), transparent);
                }

                .chat-header-info {
                    display: flex;
                    align-items: center;
                }

                .chat-avatar {
                    position: relative;
                    margin-right: 16px;
                }

                .ai-avatar-orb {
                    position: relative;
                    width: 48px;
                    height: 48px;
                }

                .avatar-core {
                    width: 100%;
                    height: 100%;
                    background: linear-gradient(45deg, var(--chatbot-ai-glow), var(--chatbot-ai-core));
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    position: relative;
                    animation: avatarPulse 3s ease-in-out infinite;
                }

                .avatar-inner {
                    width: 24px;
                    height: 24px;
                    background: rgba(255, 255, 255, 0.9);
                    border-radius: 50%;
                    animation: avatarInnerGlow 2s ease-in-out infinite;
                }

                .avatar-sparkles {
                    position: absolute;
                    top: 0;
                    left: 0;
                    right: 0;
                    bottom: 0;
                }

                .sparkle {
                    position: absolute;
                    width: 4px;
                    height: 4px;
                    background: var(--chatbot-text);
                    border-radius: 50%;
                    opacity: 0.8;
                }

                .sparkle:nth-child(1) {
                    top: 10%;
                    left: 20%;
                    animation: sparkleFloat 3s ease-in-out infinite;
                }

                .sparkle:nth-child(2) {
                    top: 20%;
                    right: 15%;
                    animation: sparkleFloat 3s ease-in-out infinite 1s;
                }

                .sparkle:nth-child(3) {
                    bottom: 15%;
                    left: 25%;
                    animation: sparkleFloat 3s ease-in-out infinite 2s;
                }

                .status-indicator-pulse {
                    position: absolute;
                    bottom: 2px;
                    right: 2px;
                    width: 14px;
                    height: 14px;
                    background: #00ff88;
                    border: 2px solid var(--chatbot-dark);
                    border-radius: 50%;
                    animation: statusPulse 2s ease-in-out infinite;
                }

                @keyframes avatarPulse {
                    0%, 100% { transform: scale(1); }
                    50% { transform: scale(1.05); }
                }

                @keyframes avatarInnerGlow {
                    0%, 100% { opacity: 0.9; transform: scale(1); }
                    50% { opacity: 1; transform: scale(1.1); }
                }

                @keyframes sparkleFloat {
                    0%, 100% { transform: translateY(0px); opacity: 0.8; }
                    50% { transform: translateY(-6px); opacity: 1; }
                }

                @keyframes statusPulse {
                    0%, 100% { opacity: 1; transform: scale(1); }
                    50% { opacity: 0.7; transform: scale(1.2); }
                }

                .chat-title h4 {
                    margin: 0;
                    font-size: 18px;
                    font-weight: 700;
                    background: linear-gradient(135deg, var(--chatbot-text), var(--chatbot-ai-glow));
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    background-clip: text;
                }

                .chat-status {
                    font-size: 13px;
                    color: var(--chatbot-text-muted);
                    display: flex;
                    align-items: center;
                    gap: 6px;
                    margin-top: 4px;
                }

                .status-dot {
                    width: 8px;
                    height: 8px;
                    background: #00ff88;
                    border-radius: 50%;
                    animation: statusDotPulse 2s ease-in-out infinite;
                }

                @keyframes statusDotPulse {
                    0%, 100% { opacity: 1; }
                    50% { opacity: 0.5; }
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

                /* ===== MESSAGES AREA ===== */
                .chat-messages {
                    flex: 1;
                    overflow-y: auto;
                    padding: 24px;
                    background: linear-gradient(180deg, var(--chatbot-dark) 0%, var(--chatbot-dark-light) 100%);
                    position: relative;
                }

                .chat-messages::-webkit-scrollbar {
                    width: 6px;
                }

                .chat-messages::-webkit-scrollbar-track {
                    background: transparent;
                }

                .chat-messages::-webkit-scrollbar-thumb {
                    background: var(--chatbot-border);
                    border-radius: 3px;
                }

                .chat-messages::-webkit-scrollbar-thumb:hover {
                    background: var(--chatbot-ai-glow);
                }

                /* ===== MESSAGE STYLING ===== */
                .message {
                    display: flex;
                    margin-bottom: 24px;
                    animation: messageSlideIn 0.5s cubic-bezier(0.23, 1, 0.32, 1);
                }

                .welcome-message {
                    animation: welcomeSlideIn 0.8s cubic-bezier(0.23, 1, 0.32, 1);
                }

                @keyframes messageSlideIn {
                    from {
                        opacity: 0;
                        transform: translateY(20px) scale(0.95);
                    }
                    to {
                        opacity: 1;
                        transform: translateY(0) scale(1);
                    }
                }

                @keyframes welcomeSlideIn {
                    from {
                        opacity: 0;
                        transform: translateY(30px) scale(0.9);
                    }
                    to {
                        opacity: 1;
                        transform: translateY(0) scale(1);
                    }
                }

                .user-message {
                    justify-content: flex-end;
                }

                .user-message .message-content {
                    order: -1;
                }

                /* ===== MESSAGE AVATARS ===== */
                .message-avatar {
                    margin: 0 12px;
                    flex-shrink: 0;
                }

                .message-ai-orb {
                    width: 36px;
                    height: 36px;
                    position: relative;
                }

                .message-orb-core {
                    width: 100%;
                    height: 100%;
                    background: linear-gradient(45deg, var(--chatbot-ai-glow), var(--chatbot-ai-core));
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    animation: messageOrbPulse 2s ease-in-out infinite;
                }

                .message-orb-inner {
                    width: 18px;
                    height: 18px;
                    background: rgba(255, 255, 255, 0.9);
                    border-radius: 50%;
                    animation: messageOrbInner 3s ease-in-out infinite;
                }

                .user-avatar-circle {
                    width: 36px;
                    height: 36px;
                    background: linear-gradient(135deg, #ff6b6b, #ee5a24);
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    border: 2px solid var(--chatbot-border);
                }

                .user-initial {
                    font-size: 14px;
                    font-weight: 600;
                    color: white;
                }

                @keyframes messageOrbPulse {
                    0%, 100% { transform: scale(1); }
                    50% { transform: scale(1.05); }
                }

                @keyframes messageOrbInner {
                    0%, 100% { opacity: 0.9; }
                    50% { opacity: 1; }
                }

                .message-content {
                    max-width: 70%;
                }

                /* ===== MESSAGE BUBBLES ===== */
                .message-bubble {
                    position: relative;
                    padding: 16px 20px;
                    border-radius: 20px;
                    word-wrap: break-word;
                    backdrop-filter: blur(10px);
                    border: 1px solid var(--chatbot-border);
                }

                .ai-bubble, .ai-response-bubble {
                    background: var(--chatbot-glass);
                    color: var(--chatbot-text);
                    position: relative;
                    overflow: hidden;
                }

                .user-bubble {
                    background: linear-gradient(135deg, #667eea, #764ba2);
                    color: white;
                    margin-left: auto;
                }

                .bubble-glow {
                    position: absolute;
                    top: 0;
                    left: 0;
                    right: 0;
                    bottom: 0;
                    background: linear-gradient(135deg, var(--chatbot-ai-glow), transparent);
                    opacity: 0.1;
                    border-radius: 20px;
                }

                .bubble-content {
                    position: relative;
                    z-index: 1;
                }

                /* ===== WELCOME MESSAGE SPECIAL STYLING ===== */
                .greeting-text {
                    font-size: 16px;
                    font-weight: 600;
                    margin: 0 0 12px 0;
                    background: linear-gradient(135deg, var(--chatbot-text), var(--chatbot-ai-glow));
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    background-clip: text;
                }

                .capabilities-intro {
                    margin: 0 0 16px 0;
                    color: var(--chatbot-text-muted);
                    font-size: 14px;
                }

                .capability-grid {
                    display: grid;
                    grid-template-columns: 1fr 1fr;
                    gap: 12px;
                    margin: 16px 0;
                }

                .capability-item {
                    display: flex;
                    align-items: center;
                    gap: 8px;
                    padding: 8px 12px;
                    background: var(--chatbot-glass);
                    border: 1px solid var(--chatbot-border);
                    border-radius: 12px;
                    font-size: 13px;
                    transition: all 0.3s ease;
                }

                .capability-item:hover {
                    background: var(--chatbot-ai-glow);
                    color: var(--chatbot-dark);
                    transform: translateY(-2px);
                }

                .capability-icon {
                    font-size: 16px;
                }

                .cta-text {
                    margin: 16px 0 0 0;
                    font-size: 14px;
                    color: var(--chatbot-text-muted);
                    text-align: center;
                }

                /* ===== GENERAL MESSAGE TEXT ===== */
                .message-bubble p {
                    margin: 0 0 8px 0;
                    line-height: 1.5;
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
                    line-height: 1.4;
                }

                .message-time {
                    font-size: 11px;
                    color: #8e9297;
                    margin-top: 4px;
                    text-align: center;
                }

                /* ===== SMART ACTIONS ===== */\n\n                .quick-action-grid {\n                    grid-template-columns: 1fr 1fr 1fr 1fr;\n                    gap: 6px;\n                }\n\n                .smart-action.compact {\n                    padding: 8px 10px;\n                    flex-direction: column;\n                    text-align: center;\n                    gap: 4px;\n                }\n\n                .smart-action.compact .action-text {\n                    font-size: 11px;\n                }\n\n                .smart-action.compact .action-icon {\n                    font-size: 14px;\n                }
                .smart-actions {
                    padding: 20px 24px 16px;
                    background: var(--chatbot-dark);
                    border-top: 1px solid var(--chatbot-border);
                }

                .action-category {
                    margin-bottom: 16px;
                }

                .action-category:last-child {
                    margin-bottom: 0;
                }

                .category-label {
                    font-size: 12px;
                    color: var(--chatbot-text-muted);
                    margin-bottom: 8px;
                    font-weight: 500;
                    text-transform: uppercase;
                    letter-spacing: 0.5px;
                }

                .action-buttons {
                    display: grid;
                    grid-template-columns: 1fr 1fr;
                    gap: 12px;
                }

                .smart-action {
                    position: relative;
                    background: var(--chatbot-glass);
                    border: 1px solid var(--chatbot-border);
                    border-radius: 16px;
                    padding: 14px 16px;
                    cursor: pointer;
                    transition: all 0.3s cubic-bezier(0.23, 1, 0.32, 1);
                    color: var(--chatbot-text);
                    display: flex;
                    align-items: center;
                    gap: 10px;
                    overflow: hidden;
                    backdrop-filter: blur(10px);
                }

                .smart-action:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
                    border-color: var(--chatbot-ai-glow);
                }

                .smart-action.primary:hover {
                    background: linear-gradient(135deg, var(--chatbot-ai-glow), var(--chatbot-ai-core));
                    color: var(--chatbot-dark);
                }

                .smart-action.secondary:hover {
                    background: linear-gradient(135deg, #f093fb, #f5576c);
                }

                .smart-action.tertiary:hover {
                    background: linear-gradient(135deg, #4facfe, #00f2fe);
                }

                .smart-action.quaternary:hover {
                    background: linear-gradient(135deg, #43e97b, #38f9d7);
                }

                .action-icon {
                    font-size: 18px;
                    flex-shrink: 0;
                }

                .action-text {
                    font-size: 13px;
                    font-weight: 500;
                    flex: 1;
                }

                .action-accent {
                    position: absolute;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 2px;
                    background: linear-gradient(90deg, transparent, var(--chatbot-ai-glow), transparent);
                    opacity: 0;
                    transition: opacity 0.3s ease;
                }

                .smart-action:hover .action-accent {
                    opacity: 1;
                }

                /* ===== AI THINKING INDICATOR ===== */
                .ai-thinking-indicator {
                    background: var(--chatbot-dark);
                    padding: 16px 24px;
                    display: flex;
                    align-items: center;
                    gap: 12px;
                    border-top: 1px solid var(--chatbot-border);
                }

                .thinking-avatar {
                    position: relative;
                }

                .thinking-orb {
                    width: 32px;
                    height: 32px;
                    position: relative;
                }

                .thinking-core {
                    width: 100%;
                    height: 100%;
                    background: linear-gradient(45deg, var(--chatbot-ai-glow), var(--chatbot-ai-core));
                    border-radius: 50%;
                    animation: thinkingPulse 1.5s ease-in-out infinite;
                }

                .thinking-pulse {
                    position: absolute;
                    top: -4px;
                    left: -4px;
                    right: -4px;
                    bottom: -4px;
                    border: 2px solid var(--chatbot-ai-glow);
                    border-radius: 50%;
                    opacity: 0.6;
                    animation: thinkingRipple 2s ease-in-out infinite;
                }

                .thinking-content {
                    flex: 1;
                }

                .thinking-dots {
                    display: flex;
                    gap: 6px;
                    margin-bottom: 4px;
                }

                .thinking-dots .dot {
                    width: 8px;
                    height: 8px;
                    background: var(--chatbot-ai-glow);
                    border-radius: 50%;
                    animation: thinkingBounce 1.4s infinite ease-in-out;
                }

                .thinking-dots .dot:nth-child(1) { animation-delay: -0.32s; }
                .thinking-dots .dot:nth-child(2) { animation-delay: -0.16s; }
                .thinking-dots .dot:nth-child(3) { animation-delay: 0s; }

                .thinking-text {
                    font-size: 12px;
                    color: var(--chatbot-text-muted);
                    font-style: italic;
                }

                @keyframes thinkingPulse {
                    0%, 100% { transform: scale(1); opacity: 1; }
                    50% { transform: scale(1.1); opacity: 0.8; }
                }

                @keyframes thinkingRipple {
                    0% { transform: scale(1); opacity: 0.6; }
                    100% { transform: scale(1.4); opacity: 0; }
                }

                @keyframes thinkingBounce {
                    0%, 80%, 100% {
                        transform: scale(0.8);
                        opacity: 0.5;
                    }
                    40% {
                        transform: scale(1.2);
                        opacity: 1;
                    }
                }

                /* ===== MODERN INPUT SYSTEM ===== */
                .chat-input-container {
                    background: var(--chatbot-dark);
                    border-top: 1px solid var(--chatbot-border);
                }

                .modern-input-wrapper {
                    padding: 20px 24px;
                }

                .input-container {
                    display: flex;
                    align-items: center;
                    gap: 12px;
                    background: var(--chatbot-glass);
                    border: 1px solid var(--chatbot-border);
                    border-radius: 24px;
                    padding: 4px;
                    transition: all 0.3s ease;
                    backdrop-filter: blur(10px);
                }

                .input-container:focus-within {
                    border-color: var(--chatbot-ai-glow);
                    box-shadow: 0 0 0 3px rgba(79, 172, 254, 0.1);
                }

                .modern-chat-input {
                    flex: 1;
                    background: transparent;
                    border: none;
                    padding: 12px 16px;
                    font-size: 14px;
                    color: var(--chatbot-text);
                    outline: none;
                    font-family: inherit;
                }

                .modern-chat-input::placeholder {
                    color: var(--chatbot-text-muted);
                }

                .input-actions {
                    display: flex;
                    align-items: center;
                    gap: 8px;
                    padding-right: 4px;
                }

                .voice-btn {
                    background: var(--chatbot-glass);
                    border: 1px solid var(--chatbot-border);
                    border-radius: 50%;
                    width: 36px;
                    height: 36px;
                    color: var(--chatbot-text-muted);
                    cursor: not-allowed;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    transition: all 0.3s ease;
                    opacity: 0.5;
                }

                .modern-send-btn {
                    position: relative;
                    background: linear-gradient(135deg, var(--chatbot-ai-glow), var(--chatbot-ai-core));
                    border: none;
                    border-radius: 50%;
                    width: 40px;
                    height: 40px;
                    color: white;
                    cursor: pointer;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    transition: all 0.3s cubic-bezier(0.23, 1, 0.32, 1);
                    overflow: hidden;
                }

                .modern-send-btn:hover {
                    transform: scale(1.05);
                    box-shadow: 0 8px 25px rgba(79, 172, 254, 0.4);
                }

                .modern-send-btn:disabled {
                    background: var(--chatbot-border);
                    cursor: not-allowed;
                    transform: none;
                    box-shadow: none;
                }

                .send-icon {
                    position: relative;
                    z-index: 2;
                }

                .send-glow {
                    position: absolute;
                    top: 0;
                    left: 0;
                    right: 0;
                    bottom: 0;
                    background: radial-gradient(circle, rgba(255, 255, 255, 0.3), transparent);
                    opacity: 0;
                    transition: opacity 0.3s ease;
                }

                .modern-send-btn:hover .send-glow {
                    opacity: 1;
                }

                .input-footer {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-top: 12px;
                    font-size: 11px;
                }

                .ai-status {
                    display: flex;
                    align-items: center;
                    gap: 6px;
                    color: var(--chatbot-text-muted);
                }

                .status-indicator-mini {
                    width: 6px;
                    height: 6px;
                    background: #00ff88;
                    border-radius: 50%;
                    animation: miniStatusPulse 2s ease-in-out infinite;
                }

                .powered-by {
                    color: var(--chatbot-text-muted);
                }

                @keyframes miniStatusPulse {
                    0%, 100% { opacity: 1; }
                    50% { opacity: 0.5; }
                }

                /* ===== MOBILE RESPONSIVE DESIGN ===== */
                @media (max-width: 480px) {
                    .orbitx-chatbot {
                        bottom: 16px;
                        right: 16px;
                    }

                    .chat-toggle {
                        width: 60px;
                        height: 60px;
                    }

                    .chat-window {
                        width: calc(100vw - 32px);
                        height: calc(100vh - 120px);
                        right: 16px;
                        bottom: 84px;
                        max-height: none;
                        border-radius: 20px;
                    }

                    .chat-header {
                        padding: 20px;
                    }

                    .chat-messages {
                        padding: 20px;
                    }

                    .capability-grid {
                        grid-template-columns: 1fr;
                        gap: 8px;
                    }

                    .action-buttons {
                        grid-template-columns: 1fr;
                        gap: 8px;
                    }

                    .smart-action {
                        padding: 12px 14px;
                    }

                    .modern-input-wrapper {
                        padding: 16px 20px;
                    }

                    .input-container {
                        border-radius: 20px;
                    }

                    .modern-chat-input {
                        font-size: 16px; /* Prevents zoom on iOS */
                    }
                }

                @media (max-width: 360px) {
                    .chat-window {
                        width: calc(100vw - 16px);
                        right: 8px;
                        border-radius: 16px;
                    }

                    .chat-header {
                        padding: 16px;
                    }

                    .chat-messages {
                        padding: 16px;
                    }

                    .greeting-text {
                        font-size: 15px;
                    }

                    .smart-actions {
                        padding: 16px 20px 12px;
                    }

                    .modern-input-wrapper {
                        padding: 12px 16px;
                    }
                }

                /* ===== ACCESSIBILITY & ANIMATIONS ===== */
                @media (prefers-reduced-motion: reduce) {
                    * {
                        animation-duration: 0.01ms !important;
                        animation-iteration-count: 1 !important;
                        transition-duration: 0.01ms !important;
                    }
                }

                /* ===== DARK THEME SUPPORT ===== */
                @media (prefers-color-scheme: dark) {
                    :root {
                        --chatbot-dark: #0a0a0f;
                        --chatbot-dark-light: #12121a;
                        --chatbot-glass: rgba(255, 255, 255, 0.05);
                        --chatbot-border: rgba(255, 255, 255, 0.1);
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

        const avatarHTML = sender === 'bot' ?
            `<div class="message-ai-orb">
                <div class="message-orb-core">
                    <div class="message-orb-inner"></div>
                </div>
            </div>` :
            `<div class="user-avatar-circle">
                <div class="user-initial">U</div>
            </div>`;

        const messageHTML = `
            <div class="message ${sender}-message">
                <div class="message-avatar">
                    ${avatarHTML}
                </div>
                <div class="message-content">
                    <div class="message-bubble ${sender === 'bot' ? 'ai-response-bubble' : 'user-bubble'}">
                        ${sender === 'bot' ? '<div class="bubble-glow"></div>' : ''}
                        <div class="bubble-content">
                            ${this.formatMessage(message)}
                        </div>
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
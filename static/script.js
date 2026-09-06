// ==========================================================================
// KARTHIKEYAN AI – CLIENT CONTROLLER & NLP CHAT ENGINE
// ==========================================================================

const chatMessages = document.getElementById("chatMessages");
const userInput = document.getElementById("userInput");
const sendButton = document.getElementById("sendButton");
const themeToggle = document.getElementById("themeToggle");
const themeIcon = document.getElementById("themeIcon");
const themeLabel = document.getElementById("themeLabel");
const sidebar = document.getElementById("sidebar");
const sidebarBackdrop = document.getElementById("sidebarBackdrop");

let chatContext = {};
let isGenerating = false;
let isScrollScheduled = false;

// =====================================================
// MOBILE SIDEBAR TOGGLE HANDLER
// =====================================================

function toggleSidebar(open) {
    if (!sidebar || !sidebarBackdrop) return;

    if (open === undefined) {
        open = !sidebar.classList.contains("open");
    }

    if (open) {
        sidebar.classList.add("open");
        sidebarBackdrop.classList.add("active");
    } else {
        sidebar.classList.remove("open");
        sidebarBackdrop.classList.remove("active");
    }
}

// =====================================================
// GUARANTEED SCROLL TO BOTTOM CONTROLLER
// =====================================================

function appendChatMessage(element) {
    if (!chatMessages) return;
    const anchor = document.getElementById("chatBottomAnchor");
    if (anchor && anchor.parentNode === chatMessages) {
        chatMessages.insertBefore(element, anchor);
    } else {
        chatMessages.appendChild(element);
    }
}

function scrollToBottom(smooth = false) {
    if (!chatMessages) return;

    // 1. Direct scrollTop calculation
    chatMessages.scrollTop = chatMessages.scrollHeight;

    // 2. Target anchor or last element scrollIntoView
    const anchor = document.getElementById("chatBottomAnchor");
    const target = anchor || chatMessages.lastElementChild;
    if (target) {
        target.scrollIntoView({
            behavior: smooth ? "smooth" : "auto",
            block: "end",
            inline: "nearest"
        });
    }

    // 3. Scroll page/window if document height exceeds viewport
    if (document.documentElement.scrollHeight > window.innerHeight) {
        window.scrollTo({
            top: document.documentElement.scrollHeight,
            behavior: smooth ? "smooth" : "auto"
        });
    }
}

function scrollToBottomForce(smooth = false) {
    if (!chatMessages) return;
    scrollToBottom(smooth);
    requestAnimationFrame(() => {
        scrollToBottom(smooth);
    });
}

// =====================================================
// CONVERT URL / MARKDOWN LINKS TO CLICKABLE LINKS
// =====================================================

function convertLinks(text) {
    if (!text) return "";

    // 1. Markdown links: [Label](url)
    text = text.replace(
        /\[([^\]]+)\]\((https?:\/\/[^\s\)]+)\)/g,
        function(_, label, url) {
            return `<a href="${url}" target="_blank" rel="noopener noreferrer">${label}</a>`;
        }
    );

    // 2. Raw URLs that are not part of an existing <a> tag
    const urlRegex = /(?<!href=")(https?:\/\/[^\s<]+)/g;
    return text.replace(urlRegex, function(url) {
        let cleanUrl = url.replace(/[.,;)]+$/, "");
        return `<a href="${cleanUrl}" target="_blank" rel="noopener noreferrer">${cleanUrl}</a>`;
    });
}

// =====================================================
// TYPING INDICATOR HELPER
// =====================================================

let activeTypingIndicator = null;

function showTypingIndicator() {
    if (activeTypingIndicator) return;

    const messageDiv = document.createElement("div");
    messageDiv.classList.add("message", "bot-message");
    messageDiv.id = "activeTypingIndicator";
    messageDiv.innerHTML = `
        <div class="avatar">🤖</div>
        <div class="message-content">
            <div class="bot-name">
                <span>Karthikeyan AI</span>
                <span class="ai-badge">AI Assistant</span>
            </div>
            <div class="bubble typing-bubble">
                <div class="typing-indicator">
                    <span class="typing-dot"></span>
                    <span class="typing-dot"></span>
                    <span class="typing-dot"></span>
                </div>
            </div>
        </div>
    `;

    appendChatMessage(messageDiv);
    scrollToBottomForce();
    activeTypingIndicator = messageDiv;
}

function removeTypingIndicator() {
    if (activeTypingIndicator && activeTypingIndicator.parentNode) {
        activeTypingIndicator.parentNode.removeChild(activeTypingIndicator);
    }
    activeTypingIndicator = null;
}

// =====================================================
// SILKY SMOOTH LINE-BY-LINE STREAMING GENERATOR
// =====================================================

function generateLineByLine(text, onComplete) {
    isGenerating = true;
    if (sendButton) sendButton.disabled = true;

    const messageDiv = document.createElement("div");
    messageDiv.classList.add("message", "bot-message");

    const avatarDiv = document.createElement("div");
    avatarDiv.classList.add("avatar");
    avatarDiv.textContent = "🤖";

    const contentDiv = document.createElement("div");
    contentDiv.classList.add("message-content");

    const nameDiv = document.createElement("div");
    nameDiv.classList.add("bot-name");
    nameDiv.innerHTML = `
        <span>Karthikeyan AI</span>
        <span class="ai-badge">AI Assistant</span>
    `;

    const bubbleDiv = document.createElement("div");
    bubbleDiv.classList.add("bubble");

    contentDiv.appendChild(nameDiv);
    contentDiv.appendChild(bubbleDiv);
    messageDiv.appendChild(avatarDiv);
    messageDiv.appendChild(contentDiv);
    appendChatMessage(messageDiv);

    scrollToBottomForce();

    // Split text into lines
    const lines = (text || "").split("\n");
    let lineIndex = 0;

    // Fluid 22ms interval: quick, responsive, and buttery smooth
    const interval = setInterval(() => {
        if (lineIndex < lines.length) {
            const rawLine = lines[lineIndex];
            const lineElem = document.createElement("div");
            lineElem.classList.add("bubble-line");

            if (rawLine.trim() === "") {
                lineElem.classList.add("empty-line");
            } else {
                lineElem.innerHTML = convertLinks(rawLine);
            }

            bubbleDiv.appendChild(lineElem);
            scrollToBottomForce();
            lineIndex++;
        } else {
            clearInterval(interval);
            isGenerating = false;
            if (sendButton) sendButton.disabled = false;

            // Guaranteed scroll to bottom after answering finishes across layout & animation ticks
            scrollToBottomForce();
            setTimeout(() => scrollToBottomForce(), 50);
            setTimeout(() => scrollToBottomForce(), 150);
            setTimeout(() => scrollToBottomForce(), 300);

            if (userInput) {
                try {
                    userInput.focus({ preventScroll: true });
                } catch (e) {
                    userInput.focus();
                }
            }
            if (onComplete) onComplete();
        }
    }, 22);
}

// =====================================================
// ADD USER MESSAGE
// =====================================================

function addUserMessage(text) {
    const messageDiv = document.createElement("div");
    messageDiv.classList.add("message", "user-message");
    messageDiv.innerHTML = `
        <div class="bubble">
            ${text}
        </div>
    `;
    appendChatMessage(messageDiv);
    scrollToBottomForce();
}

// =====================================================
// CHECK GF QUESTION
// =====================================================

function isGirlfriendQuestion(message) {
    message = message.toLowerCase();
    return (
        message.includes("girlfriend") ||
        message.includes("gf name") ||
        message.includes("his gf")
    );
}

// =====================================================
// SEND MESSAGE
// =====================================================

async function sendMessage() {
    if (isGenerating) return;

    const message = userInput.value.trim();
    if (message === "") return;

    addUserMessage(message);
    userInput.value = "";

    let password = null;
    if (isGirlfriendQuestion(message)) {
        password = prompt("🔐 This information is protected. Enter password:");
    }

    showTypingIndicator();

    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                message: message,
                password: password,
                context: chatContext
            })
        });

        const data = await response.json();
        removeTypingIndicator();

        if (data.context) {
            chatContext = data.context;
        }

        generateLineByLine(data.response);
    } catch (error) {
        removeTypingIndicator();
        generateLineByLine("⚠️ Something went wrong. Please try again.");
        console.error(error);
    }
}

// =====================================================
// ENTER KEY HANDLER
// =====================================================

if (userInput) {
    userInput.addEventListener("keypress", function(event) {
        if (event.key === "Enter") {
            event.preventDefault();
            sendMessage();
        }
    });
}

// =====================================================
// QUICK QUESTION
// =====================================================

function quickQuestion(question) {
    if (isGenerating) return;
    toggleSidebar(false); // Auto-close drawer on mobile if open
    userInput.value = question;
    sendMessage();
}

// =====================================================
// NEW CHAT
// =====================================================

function newChat() {
    chatContext = {};
    toggleSidebar(false);

    chatMessages.innerHTML = `
        <div class="message bot-message welcome-message">
            <div class="avatar">🤖</div>

            <div class="message-content">
                <div class="bot-name">
                    <span>Karthikeyan AI</span>
                    <span class="ai-badge">AI Assistant</span>
                </div>

                <div class="bubble welcome-bubble">
                    <h3>👋 Welcome!</h3>
                    <p class="welcome-intro">
                        I am <strong>Karthikeyan's Personal AI Assistant</strong>, designed to assist you with comprehensive details about his background and work.
                    </p>
                    <p class="welcome-hint">Feel free to inquire about:</p>

                    <ul class="welcome-topics">
                        <li onclick="quickQuestion('What is his education?')">🎓 Education & Degree</li>
                        <li onclick="quickQuestion('What are his skills?')">💻 Skills & Tools</li>
                        <li onclick="quickQuestion('What projects has he done?')">🚀 Featured Projects</li>
                        <li onclick="quickQuestion('What is his CGPA?')">📊 Marks & CGPA</li>
                        <li onclick="quickQuestion('Who is Karthikeyan?')">👤 Career Journey</li>
                        <li onclick="quickQuestion('What are his hobbies?')">🎨 Hobbies & Passions</li>
                    </ul>
                </div>
            </div>
        </div>
        <div id="chatBottomAnchor" class="chat-bottom-anchor"></div>
    `;

    if (userInput) {
        try {
            userInput.focus({ preventScroll: true });
        } catch (e) {
            userInput.focus();
        }
    }
    scrollToBottomForce();
}

// =====================================================
// THEME TOGGLE (DARK IS DEFAULT)
// =====================================================

if (themeToggle) {
    themeToggle.addEventListener("click", function() {
        document.body.classList.toggle("light-mode");
        const isLight = document.body.classList.contains("light-mode");

        if (isLight) {
            if (themeIcon) themeIcon.textContent = "🌙";
            if (themeLabel) themeLabel.textContent = "Dark";
        } else {
            if (themeIcon) themeIcon.textContent = "☀️";
            if (themeLabel) themeLabel.textContent = "Light";
        }
    });
}
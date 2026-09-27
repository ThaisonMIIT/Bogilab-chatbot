/**
 * Bogilab Chat Widget
 * Dán đoạn này vào trước thẻ </body> của trang web, sau khi đổi API_URL bên dưới.
 *
 * <script src="bogilab-chat-widget.js"></script>
 */
(function () {
  const API_URL = "https://YOUR-BACKEND-DOMAIN.com/chat"; // <-- đổi thành domain backend đã deploy

  const STORAGE_KEY = "bogilab_session_id";
  let sessionId = localStorage.getItem(STORAGE_KEY) || null;

  // ---------- Styles ----------
  const style = document.createElement("style");
  style.textContent = `
    #bg-chat-bubble {
      position: fixed; bottom: 20px; right: 20px; width: 60px; height: 60px;
      border-radius: 50%; background: #1d4ed8; color: #fff; display: flex;
      align-items: center; justify-content: center; cursor: pointer;
      box-shadow: 0 4px 14px rgba(0,0,0,.25); z-index: 999999; font-size: 26px;
    }
    #bg-chat-window {
      position: fixed; bottom: 92px; right: 20px; width: 340px; max-width: 92vw;
      height: 460px; max-height: 70vh; background: #fff; border-radius: 14px;
      box-shadow: 0 10px 30px rgba(0,0,0,.25); display: none; flex-direction: column;
      overflow: hidden; z-index: 999999; font-family: system-ui, sans-serif;
    }
    #bg-chat-header {
      background: #1d4ed8; color: #fff; padding: 12px 16px; font-weight: 600;
      display: flex; justify-content: space-between; align-items: center;
    }
    #bg-chat-close { cursor: pointer; font-size: 18px; }
    #bg-chat-messages {
      flex: 1; padding: 12px; overflow-y: auto; background: #f5f7fb;
      display: flex; flex-direction: column; gap: 8px; font-size: 14px;
    }
    .bg-msg { max-width: 85%; padding: 8px 12px; border-radius: 12px; line-height: 1.4; white-space: pre-wrap; }
    .bg-msg.user { align-self: flex-end; background: #1d4ed8; color: #fff; border-bottom-right-radius: 2px; }
    .bg-msg.bot { align-self: flex-start; background: #e5e7eb; color: #111; border-bottom-left-radius: 2px; }
    #bg-chat-inputbar { display: flex; border-top: 1px solid #e5e7eb; }
    #bg-chat-input {
      flex: 1; border: none; padding: 10px 12px; font-size: 14px; outline: none;
    }
    #bg-chat-send {
      background: #1d4ed8; color: #fff; border: none; padding: 0 16px; cursor: pointer;
    }
    #bg-chat-send:disabled { opacity: .5; cursor: default; }
  `;
  document.head.appendChild(style);

  // ---------- DOM ----------
  const bubble = document.createElement("div");
  bubble.id = "bg-chat-bubble";
  bubble.textContent = "💬";

  const win = document.createElement("div");
  win.id = "bg-chat-window";
  win.innerHTML = `
    <div id="bg-chat-header">
      <span>Bogilab — hỗ trợ trực tuyến</span>
      <span id="bg-chat-close">✕</span>
    </div>
    <div id="bg-chat-messages"></div>
    <div id="bg-chat-inputbar">
      <input id="bg-chat-input" type="text" placeholder="Nhập câu hỏi..." />
      <button id="bg-chat-send">Gửi</button>
    </div>
  `;

  document.body.appendChild(bubble);
  document.body.appendChild(win);

  const messagesEl = win.querySelector("#bg-chat-messages");
  const inputEl = win.querySelector("#bg-chat-input");
  const sendBtn = win.querySelector("#bg-chat-send");

  function addMessage(text, who) {
    const div = document.createElement("div");
    div.className = "bg-msg " + who;
    div.textContent = text;
    messagesEl.appendChild(div);
    messagesEl.scrollTop = messagesEl.scrollHeight;
  }

  function toggleWindow() {
    const isOpen = win.style.display === "flex";
    win.style.display = isOpen ? "none" : "flex";
    if (!isOpen && messagesEl.children.length === 0) {
      addMessage("Xin chào! Mình là trợ lý Bogilab, có thể giúp gì cho bạn về linh kiện điện thoại (màn hình, pin, tai nghe...)?", "bot");
    }
  }

  bubble.addEventListener("click", toggleWindow);
  win.querySelector("#bg-chat-close").addEventListener("click", toggleWindow);

  async function sendMessage() {
    const text = inputEl.value.trim();
    if (!text) return;
    addMessage(text, "user");
    inputEl.value = "";
    sendBtn.disabled = true;

    try {
      const res = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: text, session_id: sessionId }),
      });
      if (!res.ok) throw new Error("HTTP " + res.status);
      const data = await res.json();
      sessionId = data.session_id;
      localStorage.setItem(STORAGE_KEY, sessionId);
      addMessage(data.reply, "bot");
    } catch (err) {
      addMessage("Xin lỗi, hiện không thể kết nối máy chủ. Vui lòng thử lại hoặc nhắn Telegram @Clickbuy_ru.", "bot");
    } finally {
      sendBtn.disabled = false;
    }
  }

  sendBtn.addEventListener("click", sendMessage);
  inputEl.addEventListener("keydown", (e) => {
    if (e.key === "Enter") sendMessage();
  });
})();

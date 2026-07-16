import { useEffect, useRef, useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { sendAgentChat, sendPlainChatStream } from "./api.js";

function newSessionId() {
  return crypto.randomUUID();
}

export default function App() {
  const [mode, setMode] = useState("plain");
  const [apiKey, setApiKey] = useState(() => localStorage.getItem("apiKey") || "");
  const [sessionId, setSessionId] = useState(() => localStorage.getItem("sessionId") || newSessionId());
  const [showSettings, setShowSettings] = useState(!apiKey);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState(null);
  const logRef = useRef(null);

  useEffect(() => localStorage.setItem("apiKey", apiKey), [apiKey]);
  useEffect(() => localStorage.setItem("sessionId", sessionId), [sessionId]);

  useEffect(() => {
    logRef.current?.scrollTo({ top: logRef.current.scrollHeight, behavior: "smooth" });
  }, [messages]);

  function appendMessage(msg) {
    setMessages((prev) => [...prev, msg]);
  }

  function updateLastAssistant(text) {
    setMessages((prev) => {
      const next = [...prev];
      next[next.length - 1] = { role: "assistant", content: text };
      return next;
    });
  }

  async function handleSend() {
    const message = input.trim();
    if (!message || busy) return;
    if (!apiKey) {
      setShowSettings(true);
      setError("Set your API key first.");
      return;
    }

    setError(null);
    setInput("");
    appendMessage({ role: "user", content: message });
    setBusy(true);

    try {
      if (mode === "agent") {
        appendMessage({ role: "assistant", content: "" });
        const reply = await sendAgentChat({ message, sessionId, apiKey });
        updateLastAssistant(reply);
      } else {
        appendMessage({ role: "assistant", content: "" });
        let text = "";
        await sendPlainChatStream({
          message,
          sessionId,
          apiKey,
          onToken: (chunk) => {
            text += chunk;
            updateLastAssistant(text);
          },
        });
      }
    } catch (err) {
      updateLastAssistant(`_Error: ${err.message}_`);
      setError(err.message);
    } finally {
      setBusy(false);
    }
  }

  function handleKeyDown(e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  }

  function handleNewSession() {
    setSessionId(newSessionId());
    setMessages([]);
    setError(null);
  }

  return (
    <div className="app">
      <header className="topbar">
        <h1>Local LLM Chat</h1>
        <div className="mode-toggle">
          <button className={mode === "plain" ? "active" : ""} onClick={() => setMode("plain")}>
            Plain
          </button>
          <button className={mode === "agent" ? "active" : ""} onClick={() => setMode("agent")}>
            Agent
          </button>
        </div>
        <div className="topbar-actions">
          <button onClick={handleNewSession} title="Start a new conversation">
            New session
          </button>
          <button onClick={() => setShowSettings((s) => !s)} title="API key">
            Settings
          </button>
        </div>
      </header>

      {showSettings && (
        <div className="settings-panel">
          <label>
            API key
            <input
              type="password"
              value={apiKey}
              onChange={(e) => setApiKey(e.target.value)}
              placeholder="x-api-key"
            />
          </label>
          <span className="session-id">session: {sessionId.slice(0, 8)}</span>
        </div>
      )}

      {error && <div className="error-banner">{error}</div>}

      <main className="log" ref={logRef}>
        {messages.length === 0 && (
          <div className="empty-state">
            {mode === "agent"
              ? "Agent mode has tools + memory for this session. Ask it something."
              : "Streaming chat with the local model. Say hello."}
          </div>
        )}
        {messages.map((m, i) => (
          <div key={i} className={`message ${m.role}`}>
            <div className="bubble">
              <ReactMarkdown remarkPlugins={[remarkGfm]}>{m.content || "…"}</ReactMarkdown>
            </div>
          </div>
        ))}
      </main>

      <footer className="composer">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Message the model… (Enter to send, Shift+Enter for newline)"
          rows={2}
        />
        <button className="send" onClick={handleSend} disabled={busy || !input.trim()}>
          {busy ? "…" : "Send"}
        </button>
      </footer>
    </div>
  );
}

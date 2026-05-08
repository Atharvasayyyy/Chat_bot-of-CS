import { useState } from "react";

export default function InputBox({ onSend, disabled = false, placeholder = "Describe the issue..." }) {
  const [text, setText] = useState("");
  const [file, setFile] = useState(null);

  const handleSend = () => {
    if (disabled) return;

    const trimmedText = text.trim();

    if (!trimmedText && !file) return;

    onSend(trimmedText, file);

    setText("");
    setFile(null);
  };

  const handleKeyDown = (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="input-box">
      <label className="file-chip">
        <input
          type="file"
          accept="image/*"
          onChange={(e) => setFile(e.target.files?.[0] || null)}
        />
        {file ? file.name : "Attach image"}
      </label>

      <div className="composer-stack">
        <textarea
          className="message-input"
          rows="3"
          value={text}
          onChange={(e) => setText(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder={placeholder}
        />

        <div className="composer-footer">
          <span className="composer-hint">Press Enter to send, Shift + Enter for a new line.</span>
          <button className="primary-button" onClick={handleSend} disabled={disabled}>
            {disabled ? "Sending..." : "Send message"}
          </button>
        </div>
      </div>
    </div>
  );
}
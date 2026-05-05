import ReactMarkdown from "react-markdown";

export default function Message({ msg }) {
  return (
    <div className={msg.role === "user" ? "message-row user" : "message-row"}>
      <div className={msg.role === "user" ? "message-bubble user" : "message-bubble"}>
        <ReactMarkdown>{msg.content}</ReactMarkdown>

        {msg.file && (
          <img
            src={URL.createObjectURL(msg.file)}
            alt="Uploaded preview"
            className="message-image"
          />
        )}
      </div>
    </div>
  );
}
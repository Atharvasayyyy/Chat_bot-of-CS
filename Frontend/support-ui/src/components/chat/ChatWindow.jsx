import { useEffect, useMemo, useState } from "react";
import { getUserOrders, sendMessage, checkBackendHealth } from "../../services/api";
import Message from "./Message";
import InputBox from "./InputBox";

const actionOptions = [
  { key: "refund", label: "Refund" },
  { key: "exchange", label: "Exchange" },
  { key: "query", label: "Query" },
  { key: "other", label: "Other" },
];

export default function ChatWindow() {
  const [messages, setMessages] = useState([]);
  const [sending, setSending] = useState(false);
  const [error, setError] = useState("");
  const [step, setStep] = useState("user_id");
  const [userIdInput, setUserIdInput] = useState("");
  const [activeUserId, setActiveUserId] = useState("");
  const [orders, setOrders] = useState([]);
  const [selectedOrder, setSelectedOrder] = useState(null);
  const [selectedAction, setSelectedAction] = useState("");
  const [loadingOrders, setLoadingOrders] = useState(false);
  const [isGeneralQuery, setIsGeneralQuery] = useState(false);

  // Check backend health on mount
  useEffect(() => {
    checkBackendHealth()
      .then((res) => {
        if (res.data.status !== "ok") {
          console.warn("Backend health check returned non-ok status:", res.data);
          setError(`Backend status: ${res.data.status}. ${res.data.error || ""}`);
        }
      })
      .catch((err) => {
        console.error("Backend health check failed:", err);
        setError(`Backend unavailable: ${err.message}`);
      });
  }, []);

  const statusText = useMemo(() => {
    if (step === "user_id") return "(These will be taken from Token) Enter user ID";
    if (step === "query_type") return "Choose query type";
    if (step === "order") return "Choose a purchased item";
    if (step === "action") return "Choose a support type";
    return sending ? "Sending" : "Ready";
  }, [step, sending]);

  const addBotMessage = (content) => {
    setMessages((prev) => [...prev, { role: "bot", content }]);
  };

  const handleUserIdSubmit = async () => {
    const cleanedUserId = userIdInput.trim().toUpperCase();
    if (!cleanedUserId) return;

    setSending(true);
    setError("");
    setActiveUserId(cleanedUserId);
    setMessages([
      { role: "bot", content: `User ID set to **${cleanedUserId}**.` },
    ]);

    try {
      setLoadingOrders(true);
      const res = await getUserOrders(cleanedUserId);
      const userOrders = res.data.orders || [];
      setOrders(userOrders);
      setStep("query_type");
      addBotMessage("What would you like to do? Ask a general question or get help with a specific order?");
    } catch (requestError) {
      setError(requestError?.response?.data?.message || requestError?.message || "Unable to load user orders.");
      setOrders([]);
      setStep("user_id");
    } finally {
      setLoadingOrders(false);
      setSending(false);
    }
  };

  const handleQueryTypeSelect = (isGeneral) => {
    setIsGeneralQuery(isGeneral);
    if (isGeneral) {
      setStep("general_query");
      addBotMessage("Sure! What would you like to know?");
    } else {
      setStep("order");
      addBotMessage("Select the product you need help with.");
    }
  };

  const handleOrderSelect = (order) => {
    setSelectedOrder(order);
    setSelectedAction("");
    setStep("action");
    addBotMessage(`Selected **${order.product_name}**. Now choose refund, exchange, or query.`);
  };

  const handleActionSelect = (action) => {
    setSelectedAction(action);
    if (action === "query") {
      setStep("query");
      addBotMessage(`You can now ask your question about **${selectedOrder?.product_name || "your item"}**. What would you like to know?`);
    } else {
      setStep("compose");
      const label = actionOptions.find((item) => item.key === action)?.label || action;
      addBotMessage(`You chose **${label}** for **${selectedOrder?.product_name || "your item"}**. Type the details and send your message.`);
    }
  };

  const handleSend = async (text, file) => {
    const messageText = text.trim();
    if (!messageText && !file) return;

    if (!activeUserId) {
      setError("Please enter a user ID first.");
      return;
    }

    if (!isGeneralQuery && !selectedOrder) {
      setError("Please select an item before sending.");
      return;
    }

    // For general queries, action is "query", for others we need selectedAction
    if (!isGeneralQuery && !selectedAction) {
      setError("Please select an action type before sending.");
      return;
    }

    const formData = new FormData();
    formData.append("user_id", activeUserId);
    formData.append("message", messageText);
    
    if (selectedOrder) {
      formData.append("selected_order_id", selectedOrder.order_id);
      formData.append("selected_product", selectedOrder.product_name);
      formData.append("selected_action", selectedAction || "query");
    } else {
      // General query - no specific order
      formData.append("selected_action", "query");
    }

    if (file) formData.append("image", file);

    // Add user message to chat
    setMessages((prev) => [...prev, { role: "user", content: messageText, file }]);
    setSending(true);
    setError("");

    try {
      const res = await sendMessage(formData);
      const payload = res.data || {};
      const botMessage =
        payload.message ||
        payload.response ||
        payload.detail ||
        payload.type ||
        "No response received.";

      setMessages((prev) => [
        ...prev,
        {
          role: "bot",
          content: typeof botMessage === "string" ? botMessage : JSON.stringify(botMessage),
          actions: payload.actions || [],
        },
      ]);
    } catch (err) {
      const backendMessage =
        err?.response?.data?.message || err?.response?.data?.detail || "An error occurred while processing your request.";

      setError(backendMessage);
      setMessages((prev) => [
        ...prev,
        {
          role: "bot",
          content: backendMessage,
        },
      ]);
    } finally {
      setSending(false);
    }
  };

  return (
    <div className="chat-window">
      <div className="chat-header">
        <div>
          <p className="section-kicker">Assistant</p>
          <h3>Guided support intake</h3>
          <p className="muted">
            Enter your user ID, select a purchased item, then ask your question or request a refund/exchange.
          </p>
        </div>
        <span className={sending ? "status-dot sending" : "status-dot"}>
          {loadingOrders ? "Loading" : statusText}
        </span>
      </div>

      <section className="wizard-card">
        {step === "user_id" && (
          <div className="wizard-section">
            <p className="wizard-label">Step 1</p>
            <h4>(These will be taken from Token) Enter user ID</h4>
            <div className="wizard-row">
              <input
                className="wizard-input"
                value={userIdInput}
                onChange={(event) => setUserIdInput(event.target.value)}
                placeholder="Example: U003"
              />
              <button className="primary-button" onClick={handleUserIdSubmit} disabled={loadingOrders}>
                {loadingOrders ? "Loading..." : "Continue"}
              </button>
            </div>
          </div>
        )}

        {step !== "user_id" && (
          <div className="wizard-section wizard-summary">
            <div>
              <p className="wizard-label">Selected user</p>
              <strong>{activeUserId}</strong>
            </div>
            {selectedOrder && (
              <div>
                <p className="wizard-label">Selected item</p>
                <strong>{selectedOrder.product_name}</strong>
              </div>
            )}
            {selectedAction && (
              <div>
                <p className="wizard-label">Action</p>
                <strong>{selectedAction}</strong>
              </div>
            )}
          </div>
        )}

        {step === "query_type" && (
          <div className="wizard-section">
            <p className="wizard-label">Step 2</p>
            <h4>How can we help?</h4>
            <div className="prompt-row">
              <button className="prompt-chip" onClick={() => handleQueryTypeSelect(true)}>
                General Question
              </button>
              <button className="prompt-chip" onClick={() => handleQueryTypeSelect(false)}>
                Help with an Order
              </button>
            </div>
          </div>
        )}

        {step === "general_query" && (
          <div className="wizard-section">
            <p className="wizard-label">Step 3</p>
            <h4>Ask your question</h4>
            <InputBox onSend={handleSend} disabled={sending} placeholder="Ask any question..." />
          </div>
        )}

        {step === "order" && (
          <div className="wizard-section">
            <p className="wizard-label">Step 3</p>
            <h4>Choose one of the purchased items</h4>
            <div className="order-grid">
              {orders.map((order) => (
                <button key={order.order_id} className="order-card" onClick={() => handleOrderSelect(order)}>
                  <strong>{order.product_name}</strong>
                  <span>Order {order.order_id}</span>
                  <span>Status: {order.status || "-"}</span>
                  <span>₹{order.price}</span>
                </button>
              ))}
            </div>
          </div>
        )}

        {step === "action" && (
          <div className="wizard-section">
            <p className="wizard-label">Step 4</p>
            <h4>What do you need help with?</h4>
            <div className="prompt-row">
              {actionOptions.map((action) => (
                <button key={action.key} className="prompt-chip" onClick={() => handleActionSelect(action.key)}>
                  {action.label}
                </button>
              ))}
            </div>
          </div>
        )}

        {step === "query" && selectedOrder && (
          <div className="wizard-section">
            <p className="wizard-label">Step 4</p>
            <h4>Ask your question about <strong>{selectedOrder.product_name}</strong></h4>
            <InputBox onSend={handleSend} disabled={sending} placeholder="What would you like to know about this item?" />
          </div>
        )}

        {step === "compose" && selectedOrder && selectedAction && (
          <div className="wizard-section">
            <p className="wizard-label">Step 5</p>
            <h4>Describe the issue for <strong>{selectedOrder.product_name}</strong></h4>
            <InputBox onSend={handleSend} disabled={sending} />
          </div>
        )}
      </section>

      <div className="message-stream">
        {messages.length === 0 && step === "user_id" && (
          <div className="empty-chat">
            <strong>Start here</strong>
            <p>Enter the user ID first. After that, you will see the items purchased for that user.</p>
          </div>
        )}

        {messages.map((m, i) => (
          <Message key={i} msg={m} onAction={handleSend} />
        ))}
      </div>

      {error && <p className="error-banner">{error}</p>}
    </div>
  );
}

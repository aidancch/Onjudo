import React, { useState } from 'react';

function Chat() {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');

    const sendMessage = async () => {
        if (input.trim() === '') return;
        
        const newMessage = { text: input, sender: "User" };
        setMessages([...messages, newMessage]);

        const response = await fetch("http://127.0.0.1:5000/api/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: input }),
        });

        const data = await response.json();
        setMessages([...messages, newMessage, { text: data.response, sender: "AI" }]);
        setInput('');
    };

    return (
        <div className="flex flex-col h-full">
            <div className="flex-1 overflow-y-auto p-4 border-b">
                {messages.map((msg, index) => (
                    <div key={index} className={msg.sender === "User" ? "text-right text-blue-600" : "text-left text-gray-600"}>
                        <p className="p-2 bg-gray-200 rounded inline-block">{msg.text}</p>
                    </div>
                ))}
            </div>
            <div className="p-4 flex">
                <input
                    className="flex-1 p-2 border rounded"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="Type a message..."
                />
                <button className="ml-2 bg-blue-500 text-white p-2 rounded" onClick={sendMessage}>Send</button>
            </div>
        </div>
    );
}

export default Chat;

"use client"

import { useState } from "react";

interface Message {
    text: string;
    sender: "user" | "bot"
}

const Chatbot = () => {

    const [messages, setMessages] = useState<Message[]>([])
    const [input, setInput] = useState<string>("")

    const handleSendMessage = () => {
        if (input.trim() === "") return;

        const userMessage: Message = { text: input, sender: 'user' }
        setMessages([...messages, userMessage])
        setInput("")

        setTimeout(() => {
            const botMessage: Message = { text: "This is a bot response. ", sender: 'bot' }
            setMessages([...messages, botMessage])
        }, 1000);
    }

    return (
        <main className=" flex flex-col justify-between bg-white h-screen">
            <div className=" flex-grow p-4 overflow-y-auto">
                {messages.map((message, index) => (
                    <div
                        key={index}
                        className={`p-2 rounded-lg mb-2 ${message.sender === "user" ? "bg-blue-100 self-end" : "bg-gray-100 self-start"}`}
                    >
                        <p>{message.text}</p>
                    </div>
                ))}
            </div>

            <div className=" p-4 border-t-2 border-black">
                <input 
                    type='text' 
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyPress={(e) => e.key === "Enter" && handleSendMessage()}
                    className="w-full text-black py-2 px-4 border-2 border-gray-300 rounded-lg"
                    placeholder="What's bothering you? 
                    Share it with me and I will provide individual advice." 
                />
                <button
                    onClick={handleSendMessage}
                    className="mt-2 bg-blue-500 text-white py-2 px-4 rounded-lg"
                >
                    Send
                </button>
            </div>
        </main>
    )
}

export default Chatbot
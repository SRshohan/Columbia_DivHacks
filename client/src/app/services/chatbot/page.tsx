"use client"

import { Button } from "@/components/ui/button";
import { useState } from "react";
import axios from "axios"
import AI_Assistant from "@/components/AI_Assistant";

interface Message {
    text: string;
    sender: "user" | "bot"
}

const preBuiltQuestions = [
    "Feeling anxious today? Let's find a calm space together",
    "Having a tough day? We're here to listen and help",
    "Feeling overwhelmed? Let's break things down together",
    "Feeling alone? Remember, we're in this together."
]

const Chatbot = () => {

    const [messages, setMessages] = useState<Message[]>([])
    const [input, setInput] = useState<string>("")
    const [preQuestSeen, SetPreQuestSeen] = useState(true);

    const handleSendMessage = async () => {
        if (input.trim() === "") return;

        try {
            const response = await axios.post('https://d1c6-209-2-226-50.ngrok-free.app', { user_input: input });
            const botResponse: string = response.data.response; // Предполагается, что ответ содержит поле `response`
            console.log("botResponse ", botResponse);

            const botMessage: Message = { text: botResponse, sender: 'bot' };
            const userMessage: Message = { text: input, sender: 'user' };

            setMessages([...messages, userMessage, botMessage]);
            SetPreQuestSeen(false);
            setInput("");
        } catch (error) {
            console.error("Error sending message:", error);
        }
    };

    const handlePreBuildQuestion = (question: string) => {
        setInput(question);
    }

    return (
        <>
            <div className=" fixed bottom-0 flex flex-col items-center justify-center w-full h-[93%] p-4">
                <div className="flex flex-col w-full max-w-md bg-white rounded-lg shadow-md p-4 h-full">
                    <div className="flex flex-col space-y-4 mb-4 overflow-y-auto flex-grow">
                        {messages.map((msg, index) => (
                            <div key={index} className={`flex ${msg.sender === "user" ? "justify-end" : "justify-start"}`}>
                                <div className={`p-2 rounded-lg ${msg.sender === "user" ? "bg-blue-500 text-white" : "bg-gray-200 text-black"}`}>
                                    {msg.text}
                                </div>
                            </div>
                        ))}
                    </div>
                    {preQuestSeen === true && (
                        <div className="flex flex-col space-y-2 mb-4">
                            {preBuiltQuestions.map((question, index) => (
                                <div
                                    key={index}
                                    onClick={() => handlePreBuildQuestion(question)}
                                    className="p-2 bg-gray-200 text-black rounded-lg cursor-pointer"
                                >
                                    {question}
                                </div>
                            ))}
                        </div>
                    )}
                    <div className="flex flex-row items-center">
                        <input
                            type="text"
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            className="flex-grow p-2 border border-gray-300 rounded-l-lg"
                            placeholder="Type your message..."
                        />
                        <Button onClick={handleSendMessage} className="p-2 bg-blue-500 text-white rounded-r-lg">
                            Send
                        </Button>
                    </div>
                </div>
            </div>
            <AI_Assistant />
        </>
    );
}

export default Chatbot
"use client"
import { Button } from "@/components/ui/button";
import { Mic } from 'lucide-react';
import { useEffect, useState } from "react";
import axios from "axios";
import AI_Assistant from "@/components/AI_Assistant";
import storeDataToVerbwire from "@/functions/storeDataToVerbwire";
import fetchDataFromIPFS from "@/functions/fethcDataFromVerbwire";

interface Message {
    text: string;
    sender: "user" | "bot";
}

const preBuiltQuestions = [
    "Feeling anxious today? Let's find a calm space together",
    "Having a tough day? We're here to listen and help",
    "Feeling overwhelmed? Let's break things down together",
    "Feeling alone? Remember, we're in this together."
];

const Chatbot = () => {
    const [messages, setMessages] = useState<Message[]>([]);
    const [input, setInput] = useState<string>("");
    const [file, setFile] = useState<File | null>(null);
    const [preQuestSeen, SetPreQuestSeen] = useState(true);
    const [retrievedData, setRetrievedData] = useState(null);
    const [ipfsUrl, setIpfsUrl] = useState<string | null>(null);
    // Mic
    const [isToggled, setIsToggled] = useState(false);


    const handleSendMessage = async () => {
        if (input.trim() === "") return;

        try {
            // Store the user input to Verbwire
            if (input && file) {
                await storeDataToVerbwire({input, file});
            }

            // Send the user input to the AI model
            const response = await axios.post('https://6666-209-2-226-50.ngrok-free.app', { user_input: input });
            const botResponse: string = response.data.response; // Предполагается, что ответ содержит поле `response`
            console.log("botResponse ", botResponse);

            const botMessage: Message = { text: botResponse, sender: 'bot' };
            const userMessage: Message = { text: input, sender: 'user' };

            setMessages([...messages, userMessage, botMessage]);
            SetPreQuestSeen(false);
            setInput("");
            setFile(null);
        } catch (error) {
            console.error("Error sending message:", error);
        }
    };

    const handlePreBuildQuestion = (question: string) => {
        setInput(question);
    };

    const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        if (event.target.files && event.target.files.length > 0) {
            setFile(event.target.files[0]);
        }
    };

    const handleFetchData = async () => {
        if (ipfsUrl) {
            try {
                const data = await fetchDataFromIPFS(ipfsUrl);
                setRetrievedData(data);
                setIpfsUrl(data);
            } catch (error) {
                console.error("Error fetching data:", error);
            }
        }
    };

    const toggleMicrophone = async () => {
        setIsToggled(prevState => !prevState);

        if (!isToggled) {
            try {
              const response = await axios.post("https://6666-209-2-226-50.ngrok-free.app", {
                user_input: "i feel bad"
              });
              console.log('POST request successful:', response.data);
            } catch (error) {
              console.error('Error making POST request:', error);
            }
        }
    };

    useEffect(() => {
        if (ipfsUrl) {
            handleFetchData();
        }
    }, [ipfsUrl]);

    return (
        <>
            <div className="fixed bottom-0 flex flex-col items-center justify-center w-full h-[93%] p-4">
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
            <div className=" absolute bottom-3 left-11">
                <p className=" text-3xl text-black">Provide a file for saving conversation</p>
                <input
                    type="file"
                    onChange={handleFileChange}
                    className="p-2 border border-gray-300"
                />
            </div>
            <AI_Assistant />
            {retrievedData && (
                <div className="mt-4 p-4 bg-white rounded-lg shadow-md">
                    <h2 className="text-xl font-bold mb-2">Retrieved Data</h2>
                    <pre className="whitespace-pre-wrap">{JSON.stringify(retrievedData, null, 2)}</pre>
                </div>
            )}

            <div className="fixed bottom-7 left-[65%] mr-10 transform -translate-x-1/2 flex justify-center items-center">
                <Mic
                    className={`w-11 h-11 ${isToggled ? 'text-red-500' : 'text-blue-500'} cursor-pointer`}
                    onClick={toggleMicrophone}
                />
            </div>
        </>
    );
};

export default Chatbot;

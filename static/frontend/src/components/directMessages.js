import React, {useState, useEffect } from 'react';
import { io } from "socket.io-client";

const DirectMessages = ({ friendId , conversationId }) => {
    const [message, setMessage] = useState('');
    const [chat, setChat] = useState([]);
    const socket = io("http://localhost:8000");

    useEffect(() => {
        //Listen for incoming messages
        socket.on('receive_message', (message) => {
            setChat(prevChat => [...prevChat, message]);
        });

        //Get existing messages
        if (conversationId){
            fetch(`/get_chat_messages/${conversationId}`)
            .then(response => response.json())
            .then(data => {
                if (data.error){
                    console.error("Conversation not found");
                }
                else{
                    setChat(data);
                }
            })
            .catch(error => console.log("Error fetching chat messages", error));
        }
        
        return () => {
            socket.disconnect();
        };
    }, [conversationId]);

    const sendMessage = () => {
        //Emits new message to server
        const newMessage = {
            content: message,
            senderid: friendId,
            timestamp: new Date().toISOString()
        };
        socket.emit('send_message', newMessage);
        setMessage('');
        setChat(prevChat => [...prevChat, newMessage])
    };

    return (
        <div>
            <p>Direct Messages Component</p>
            <div className="chatBox">
                {chat.map((message, index) => (
                    <div key={index}>{message.content}</div>
                ))}
            </div>
            <input value={message} onChange={(e) => setMessage(e.target.value)}/>
            <button onClick={sendMessage}>Send</button>
        </div>
    );
};
export default DirectMessages;
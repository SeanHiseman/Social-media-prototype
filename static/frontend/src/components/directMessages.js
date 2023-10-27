import React, {useState, useEffect } from 'react';
import { io } from "socket.io-client";

const Chat = ( friendId ) => {
    const [message, setMessage] = useState('');
    const [chat, setChat] = useState([]);
    const socket = io("http://localhost:8000");

    useEffect(() => {
        fetch(`/get_chat_messages/${friendId}`)
        .then(response => response.json())
        .then(data => setChat(data))
        .catch(error => console.log("Error fetching chat messages", error));
        
        socket.on('receive_message', (message) => {
            setChat([...chat, message]);
        });
        return () => {
            socket.disconnect();
        };
    }, [chat, friendId]);

    const sendMessage = () => {
        const messageData = {
            content: message,
            receiver_id: friendId
        };
        socket.emit('send_message', messageData);
        setMessage('');
    };

    return (
        <div>
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
export default Chat;
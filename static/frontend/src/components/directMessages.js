import React, {useState, useEffect, useRef } from 'react';
import { io } from "socket.io-client";
import '../css/messages.css';

const socket = io("http://localhost:8000/chat");

const DirectMessages = ({ friendId , friendName, conversationId, loggedInUserId }) => {
    const [message, setMessage] = useState('');
    const [chat, setChat] = useState([]);
    const chatBoxRef = useRef(null);

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
        
        return () => {socket.off('receive message');
        };
    }, [conversationId]);

    const sendMessage = () => {
        //Emits new message to server
        const newMessage = {
            content: message,
            senderId: loggedInUserId,
            conversationId: conversationId,
        };
        socket.emit('send_message', newMessage);
        setMessage('');
        setChat(prevChat => [...prevChat, newMessage])
    };
    console.log("Logged in user ID: ", loggedInUserId);
    console.log("Chat messages:", chat);
    return (
        <div className="chat-container">
            <div className="chat-header">
                {friendName} 
            </div>
            <div className="chat-messages" ref={chatBoxRef}>
                {chat.map((message) => (
                    <div key={message.id} className={`message ${message.senderId === loggedInUserId ? 'outgoing' : 'incoming'}`}>
                        {message.content}
                    </div>
                ))}
            </div>
            <div className="chat-input">
                <input type="text" value={message} onChange={(e) => setMessage(e.target.value)} placeholder="Type a message..."/>
                <button className="send" onClick={sendMessage}>Send</button>
            </div>
        </div>
    );
};
export default DirectMessages;
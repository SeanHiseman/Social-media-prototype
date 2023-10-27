import React, { useEffect, useState } from 'react';
import Chat from './directMessages'; 
import '../css/messages.css';

const MessagesButton = () => {
    const [isDropdownOpen, setDropdownOpen] = useState(false);
    const [messages, setMessages] = useState([]);
    const [currentChat, setCurrentChat] = useState(null);

    useEffect(() => {
        fetch('/get_friends')
        .then(response => response.json())
        .then(data => setMessages(data))
        .catch(error => console.log("Error fetching friends", error))
    }, []);

    const openChat = (friendId) => {
        setCurrentChat(friendId);
    };

    return (
        <div className="messages-container">
            <button id="messages-button" onClick={() => setDropdownOpen(!isDropdownOpen)}>Messages</button>

            {isDropdownOpen && (
                <div className="messages-dropdown">
                    {messages.map(item => (
                        <div key={item.friend_id} onClick={() => openChat(item.friend_id)}>
                            <p>{item.friend_name}</p>
                        </div>
                    ))}
                </div>
            )}
            {currentChat && <Chat friendId={currentChat} />}
        </div>
    );
};

export default MessagesButton;

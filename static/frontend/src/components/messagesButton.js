import React, { useEffect, useState } from 'react';
import '../css/messages.css';

const MessagesButton = () => {
    const [isDropdownOpen, setDropdownOpen] = useState(false);
    const [messages, setMessages] = useState([]);

    useEffect(() => {
        fetch('/get_messages')
        .then(response => response.json())
        .then(data => setMessages(data))
        .catch(error => console.log("Error fetching messages", error))
    }, []);

    return (
        <div className="messages-container">
            <button id="messages-button" onClick={() => setDropdownOpen(!isDropdownOpen)}>Messages</button>

            {isDropdownOpen && (
                <div className="messages-dropdown">
                    {messages.map(item => (
                        <div key={item.friend_name}>
                            <p>{item.friend_name}</p>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};

export default MessagesButton;

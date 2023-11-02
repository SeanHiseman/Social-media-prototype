import React, { useEffect, useState } from 'react';
import DirectMessages from './directMessages'; 
import '../css/messages.css';

const MessagesButton = () => {
    const [isDropdownOpen, setDropdownOpen] = useState(false);
    const [friends, setFriends] = useState([]);
    const [selectedFriend, setSelectedFriend] = useState(null);
    const [conversationId, setConversationId] = useState(null);

    useEffect(() => {
        fetch('/get_friends')
        .then(response => response.json())
        .then(data => setFriends(data))
        .catch(error => console.log("Error fetching friends", error))
    }, []);

    const handleFriendClick = async (friendId, friendName, conversationId) => {
        console.log("Friend clicked:", friendId, friendName, conversationId);
        setSelectedFriend(friendId);
        setConversationId(conversationId);
    };

    return (
        <div className="messages-container">
            <button id="messages-button" onClick={() => setDropdownOpen(!isDropdownOpen)}>Messages</button>

            {isDropdownOpen && (
                <div className="messages-dropdown">
                    {friends.map(friend => (
                        <div className="friend-chat-box" key={friend.friend_id} 
                        onClick={() => handleFriendClick(friend.friend_id, friend.friend_name, friend.conversation_id)}>
                            <p>{friend.friend_name}</p>
                        </div>
                    ))}
                </div>
            )}
            {selectedFriend && <DirectMessages friendId={selectedFriend} conversationId={conversationId} />}
        </div>
    );
};

export default MessagesButton;

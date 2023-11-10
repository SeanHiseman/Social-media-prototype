import React, { useEffect, useState } from 'react';
import MessagesButton from './messagesButton';
import DirectMessages from './directMessages';

const ChatApp = () => {
    const [selectedFriend, setSelectedFriend] = useState(null);
    const [conversationId, setConversationId] = useState(null);
    useEffect(() => {
      }, [selectedFriend, conversationId]);
    return (
        <div>
            <MessagesButton onSelectFriend={(friend, conversation) => {
                selectedFriend(friend);
                setConversationId(conversation);
            }}/>
            {selectedFriend && (
            <DirectMessages 
                friendId={selectedFriend} 
                conversationId={conversationId}
                loggedInUserId="47005264-9402-4002-82a0-7db358727e47"
            />
            )}
        </div>
    );
};

export default ChatApp;

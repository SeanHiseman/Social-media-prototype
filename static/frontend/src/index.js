import React from 'react';
import ReactDOM from 'react-dom';
import MessagesButton from './components/messagesButton';
import SendFriendRequestButton from './components/sendFriendRequest';
import FriendRequests from './components/friendRequestsList';

//Render the MessagesButton if its root exists
const messagesRoot = document.getElementById('messages-root');
if (messagesRoot) {
    ReactDOM.render(<MessagesButton />, messagesRoot);
}

//Render the SendFriendRequestButton if its root exists
const friendRequestRoot = document.getElementById('friend-request-root');
if (friendRequestRoot) {
    const receiverProfileId = friendRequestRoot.getAttribute('data-receiver-id');
    ReactDOM.render(
        <SendFriendRequestButton receiverProfileId={receiverProfileId} />, 
        friendRequestRoot
    );
}

//Render the FriendRequests if its root exists
const incomingRequestsRoot = document.getElementById('incoming-requests-root');
if (incomingRequestsRoot) {
    ReactDOM.render(
        <FriendRequests />,
        incomingRequestsRoot
    );
}

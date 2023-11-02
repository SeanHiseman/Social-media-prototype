import React from 'react';
import ReactDOM from 'react-dom';
//import MessagesButton from './components/messagesButton';
import SendFriendRequestButton from './components/sendFriendRequest';
import FriendRequests from './components/friendRequestsList';
import UpdateBioButton from './components/updateBio';
//import DirectMessages from './components/directMessages'
import ChatApp from './components/chatApp';

//Below functions check if a root exists so it can be rendered on the corresponding page

//const messagesRoot = document.getElementById('messages-root');
//if (messagesRoot) {
    //ReactDOM.render(<MessagesButton />, messagesRoot);
//}

const friendRequestRoot = document.getElementById('friend-request-root');
if (friendRequestRoot) {
    const receiverProfileId = friendRequestRoot.getAttribute('data-receiver-id');
    ReactDOM.render(
        <SendFriendRequestButton receiverProfileId={receiverProfileId} />, 
        friendRequestRoot
    );
}

const incomingRequestsRoot = document.getElementById('incoming-requests-root');
if (incomingRequestsRoot) {
    ReactDOM.render(
        <FriendRequests />,
        incomingRequestsRoot
    );
}

const updateBio = document.getElementById('update-bio');
if (updateBio) {
    ReactDOM.render(
        <UpdateBioButton />,
        updateBio
    );
}

//const directMessagesRoot = document.getElementById('direct-messages-root');
//if (directMessagesRoot) {
    //ReactDOM.render(
        //<DirectMessages />,
        //directMessagesRoot
    //);
//}

const chatAppRoot = document.getElementById('chat-app-root');
if (chatAppRoot){
    ReactDOM.render(<ChatApp />, chatAppRoot);
}

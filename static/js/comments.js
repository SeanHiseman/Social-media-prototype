async function toggleCommentSection(contentId) {
    var commentSection = document.getElementById(`comment-section-${contentId}`);
    commentSection.style.display = (commentSection.style.display === 'none' || commentSection.style.display === '') ? 'block' : 'none';
  
    if (commentSection.style.display === 'block') {
        fetchAndRenderComments(contentId);
    }
}

function renderComments(comments, parentId, container, depth, contentId){
    const filteredComments = comments.filter(c => c.parent_id === parentId);
    filteredComments.sort((a, b) => (b.likes - b.dislikes) - (a.likes - a.dislikes));
    //Iterates over comments
    filteredComments.forEach(comment => {
        //Container for each comment
        const commentContainer = document.createElement('div');
        commentContainer.className = 'comment-container';
        //indents by 20px for every reply
        commentContainer.style.marginLeft = `${depth*20}px`;

        //for profile photo and username
        const commentProfileContainer = document.createElement('div');
        commentProfileContainer.className = 'comment-profile-container';

        //Profile photo
        const profilePhoto = document.createElement('img');
        profilePhoto.className = 'profile-photo';
        profilePhoto.src = `/static/${comment.profile_photo}` || '/static/images/site_images/blank-profile.png';
        commentProfileContainer.appendChild(profilePhoto);

        //Username
        const usernameElement = document.createElement('div');
        usernameElement.className = 'username';
        const username = comment.username || 'Anonymous';
        usernameElement.textContent = username
        commentProfileContainer.appendChild(usernameElement) 

        //for appending features to
        const commentElement = document.createElement('div');
        commentElement.className = 'comment-element';        

        //contains everything except username (so it can appear above)
        const horizontalContainer = document.createElement('div');
        horizontalContainer.className = 'horizontal-container';
        horizontalContainer.appendChild(commentElement);             
        
        //comment text
        const commentText = document.createElement('span');
        commentText.className = `comment-text`
        commentText.textContent = comment.comment_text;
        commentElement.appendChild(commentText);

        //container for like/dislike total and buttons
        const likeDislikeContainer = document.createElement('div');
        likeDislikeContainer.className = 'like-dislike-container';

        //like button
        const likeButton = document.createElement('button');
        likeButton.className = "like-dislike-arrows"
        likeButton.style.backgroundImage = "url('/static/images/site_images/up.png')";
        likeButton.style.width = '20px';  
        likeButton.style.height = '20px';  
        likeButton.onclick = () => likeComment(comment.id, contentId);
        likeDislikeContainer.appendChild(likeButton);

        //Like/dislike total
        const netLikes = comment.likes - comment.dislikes;
        const netLikesElement = document.createElement('span');
        netLikesElement.className = 'net-likes';
        netLikesElement.textContent = `${netLikes}`;
        likeDislikeContainer.appendChild(netLikesElement)

        //Dislike button
        const dislikeButton = document.createElement('button');
        dislikeButton.className = "like-dislike-arrows"
        dislikeButton.style.backgroundImage = "url('/static/images/site_images/down.png')";
        dislikeButton.style.width = '20px'; 
        dislikeButton.style.height = '20px';  
        dislikeButton.onclick = () => dislikeComment(comment.id, contentId);
        likeDislikeContainer.appendChild(dislikeButton);              

        //reply buttons
        const replyButton = document.createElement('button');
        replyButton.textContent = 'Reply';
        replyButton.onclick = () => {
            let existingReplyInput = document.getElementById(`reply-input-${comment.id}`);
            let existingSubmitReplyButton = document.getElementById(`submit-reply-button-${comment.id}`);
        
            if (!existingReplyInput) {
                //Div so reply box is below comment
                const replyContainer = document.createElement('div');
                replyContainer.className = 'reply-container';
                
                const replyInput = document.createElement('textarea');
                replyInput.placeholder = 'Type your reply here...';
                replyInput.id = `reply-input-${comment.id}`;
                replyContainer.appendChild(replyInput);
        
                //Create and append 'Submit Reply' button if it doesn't already exist
                const submitReplyButton = document.createElement('button');
                submitReplyButton.textContent = 'Post';
                submitReplyButton.id = `submit-reply-button-${comment.id}`;
                submitReplyButton.onclick = () => {
                    const replyText = replyInput.value;
                    addComment(comment.content_id, comment.id, replyText);
                };
                
                replyContainer.appendChild(submitReplyButton);
                commentContainer.appendChild(replyContainer);

            } else {
                //Remove existing reply input box and 'Submit Reply' button
                existingReplyInput.parentNode.remove();
                if (existingSubmitReplyButton) {
                    existingSubmitReplyButton.remove();
                }
            }
        };
        replyButton.classList.add('reply-button');
        
        //brings elements together
        commentElement.appendChild(likeDislikeContainer);
        commentElement.appendChild(replyButton);
        commentContainer.appendChild(commentProfileContainer);
        commentContainer.appendChild(horizontalContainer)
        container.appendChild(commentContainer);

        // Recursion for nested replies
        renderComments(comments, comment.id, container, depth + 1, contentId);
    });
}

async function fetchAndRenderComments(contentId) {
    const response = await fetch(`/get_comments/${contentId}`);
    const comments = await response.json();

    const commentList = document.getElementById(`comment-list-${contentId}`);
    if (!commentList){
        console.log(`Element with ID comment-list-${contentId} not found.`);
        return;    
    }
    commentList.innerHTML = '';
    renderComments(comments, null, commentList, 0, contentId);
}

async function addComment(contentId, parentId, commentText) {
    try{
        const response = await fetch('/api/add_comment',{
            method: 'POST',
            headers:{
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                content_id: contentId,
                parent_id: parentId,
                comment_text: commentText,    
            }),
        });
        const data = await response.json();

        if (data.success){
            fetchAndRenderComments(contentId);
        }
        else{
            console.error(`Error adding comment: ${data.message}`);
        }
    }
    catch (error){
        console.error(`Error adding comment: ${error}`);
    }
}

async function like_dislike_comment(reaction_type, commentId, contentId){
    try{
        const response = await fetch('/api/like_dislike',{
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({comment_id: commentId, reaction_type:reaction_type})
        });
        const data = await response.json();
        if (data.success){
            fetchAndRenderComments(contentId);
        }
        else{
            console.error('Error updating reaction');
        }
    }
    catch (error){
        console.error('Error updating reaction')
    }
}

function likeComment(commentId, contentId){
    like_dislike_comment('like',commentId,contentId);
}
function dislikeComment(commentId, contentId){
    like_dislike_comment('dislike',commentId,contentId);
}
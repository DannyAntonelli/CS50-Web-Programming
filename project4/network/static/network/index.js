document.addEventListener('DOMContentLoaded', () => {

    // Use buttons to toggle between views
    const profileView = document.querySelector('#profile-view');
    profileView.style.display = "none";

    document.querySelector("#all-posts").addEventListener("click", () => {
        profileView.style.display = "none";
        loadPosts();
    });

    if (isAuthenticated()) {
        document.querySelector("#following").addEventListener("click", () => {
            profileView.style.display = "none";
            loadPosts("following/");
        });
        const user = document.querySelector(".user");
        user.addEventListener("click", () => {
            loadProfile(user.id);
        })
    }

    // By default load all the posts
    loadPosts();
})

function loadPosts(type="", page=1) {
    // Show the posts
    posts = document.getElementById("posts-view");
    posts.style.display = "block";
    posts.innerHTML = "";

    // Fetch the posts
    fetch("/get_posts/" + type + `page${page}`)
    .then(response => response.json())
    .then(response => {
        paginator(type, page, response.numPages);
        response.posts.forEach(post => showPost(post));
    })
}

function paginator(type, page, numPages) {

    // Get the pages div
    pages = document.getElementById("pages");
    pages.innerHTML = "";

    // Template of the innerHTML
    const a = '<a class="page-link" href="#">PLACEHOLDER</a>';

    // Create a "previous" button
    if (page != 1) {
        const previousPage = document.createElement("li");
        previousPage.className = "page-item col-2";
        previousPage.addEventListener("click", () => loadPosts(type, page-1));
        previousPage.innerHTML = a.replace("PLACEHOLDER", "Previous");
        pages.append(previousPage);
    }

    // Create a next button
    if (page != numPages) {
        const nextPage = document.createElement("li");
        nextPage.className = "page-item col-2";
        nextPage.addEventListener("click", () => loadPosts(type, page+1));
        nextPage.innerHTML = a.replace("PLACEHOLDER", "Next");
        pages.append(nextPage);
    }
}

function loadProfile(id) {

    // Load the posts of the profile
    loadPosts(`${id}/`);

    // Hide the "new post" form and show the profile-view
    document.querySelector("#new-post").style.display = "none";
    document.querySelector("#profile-view").style.display = "block";

    // Get the elements of the page
    const followButton = document.querySelector("#follow-button");
    const username = document.querySelector(".card-title");
    const numFollowers = document.querySelector("#num-followers");
    const numFollowing = document.querySelector("#num-following");

    // Fetch the profile
    fetch(`/profile/${id}`)
    .then(response => response.json())
    .then(profile => {
        // Set the correct data
        username.innerHTML = profile.username;
        numFollowers.innerHTML = (profile.numFollowers != 1) ? `${profile.numFollowers} followers` : `${profile.numFollowers} follower`;
        numFollowing.innerHTML = `${profile.numFollowing} following`;

        // Set the button
        if (!profile.canFollow) {
            followButton.style.display = "none";
        }
        else {
            followButton.style.display = "block";
            followButton.addEventListener("click", () => changeFollow(profile.id));
            if (profile.isFollowing) {
                followButton.innerHTML = "Unfollow";
            }
            else {
                followButton.innerHTML = "Follow";
            }
        }
    })
}

function showPost(post) {

    // Create the card of the post
    const card = document.createElement("div");
    card.id = `${post.id}-card`;
    card.className = "card col-auto";

    // Username and edit button
    const row = document.createElement("div");
    row.id = `${post.id}-header`;
    row.className = "row";

    const username = document.createElement("div");
    username.className = "card-title col-1";
    username.id = `${post.id}-username`;
    username.innerHTML = post.user;
    username.addEventListener("click", () => loadProfile(post.userID))
    row.append(username);

    if (post.canEdit) {
        edit = document.createElement("button");
        edit.type = "button";
        edit.className = "btn btn-link col-1";
        edit.id = `${post.id}-edit-button`;
        edit.innerHTML = "Edit";
        edit.addEventListener("click", () => editPost(post));
        row.append(edit);
    }
    card.append(row)

    // Timestamp
    const timestamp = document.createElement("h6");
    timestamp.className = "text-muted col";
    timestamp.innerHTML = post.timestamp;
    card.append(timestamp);

    // Text
    const text = document.createElement("p");
    text.id = `${post.id}-text`;
    text.className = "card-text";
    text.innerHTML = post.text;
    card.append(text);

    // Likes
    const likesRow = document.createElement("div");
    likesRow.className = "row";
    likesRow.id = `${post.id}-likes-row`;

    const likesIcon = document.createElement("i");
    likesIcon.id = `${post.id}-likes-icon`;
    if (post.liked) {
        likesIcon.className = "icon-heart col-auto";
    }
    else {
        likesIcon.className = "icon-heart-empty col-auto";
    }

    const numLikes = document.createElement("div");
    numLikes.id = `${post.id}-num-likes`;
    numLikes.innerHTML = (post.numLikes != 1) ? `${post.numLikes} likes` : `${post.numLikes} like`;

    likesRow.append(likesIcon);
    likesRow.append(numLikes);
    card.append(likesRow);

    // Check if user is logged and can leave a like
    if (isAuthenticated()) {
        likesIcon.addEventListener("click", () => changeLike(post));
    }
    else {
        likesIcon.addEventListener("click", () => {
            document.getElementById("login").click();
        })
    }
    
    // Add the post created to the posts-view
    postsView = document.getElementById("posts-view");
    postsView.append(card);
    br = document.createElement("br");
    postsView.append(br);
}

function changeLike(post) {

    // Get the like icon and the likes number
    const likesIcon = document.getElementById(`${post.id}-likes-icon`);
    const numLikes = document.getElementById(`${post.id}-num-likes`)

    // Do the API request to update the like
    fetch(`/post/${post.id}/change_like`)
    .then(response => response.json())
    .then(response => {
        if (response.liked) {
            likesIcon.className = "icon-heart col-auto";
        }
        else {
            likesIcon.className = "icon-heart-empty col-auto";
        }
        numLikes.innerHTML = (response.numLikes != 1) ? `${response.numLikes} likes` : `${response.numLikes} like`;
    })
}

function changeFollow(id) {

    // Get the follow button followers number
    const FollowButton = document.getElementById("follow-button");
    const numFollowers = document.getElementById("num-followers");

    // Do the API request to update the like
    fetch(`/profile/${id}/change_follow`)
    .then(response => response.json())
    .then(response => {
        if (response.following) {
            FollowButton.innerHTML = "Unfollow";
        }
        else {
            FollowButton.innerHTML = "Follow";
        }
        numFollowers.innerHTML = (response.numFollowers != 1) ? `${response.numFollowers} followers` : `${response.numFollowers} follower`;
    })
}

function editPost(post) {

    // Hide the edit button
    const editButton = document.getElementById(`${post.id}-edit-button`);
    editButton.style.display = "none";

    // Create save button and add it to the card
    const row = document.getElementById(`${post.id}-header`);
    const button = document.createElement("button");
    button.type = "button";
    button.className = "btn btn-link col-1";
    button.id = `${post.id}-save-button`;
    button.innerHTML = "Save";
    row.append(button);

    // Get the previous text
    const text = document.getElementById(`${post.id}-text`);
    text.contentEditable = true;

    button.addEventListener("click", () => {
        fetch("/new_post", {
            method: 'PUT',
            headers: {
                'X-CSRFToken': getCookie("csrftoken")
            },
            body: JSON.stringify({
                id: post.id,
                text: text.textContent
            })
        })
        .then(() => {
            text.innerHTML = text.textContent;
            text.contentEditable = false;
            button.style.display = "none";
            editButton.style.display = "block";
        });
    })
}

function isAuthenticated() {
    return (document.querySelector("#following")) ? true : false;
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
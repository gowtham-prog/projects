document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#profile').style.display = 'none';    
    window.history.pushState('The Network', 'The Network', 'http://127.0.0.1:8000/');
    if(document.getElementById('following')) {
        document.getElementById('following').addEventListener('click', () => load_posts("/followed",1));          
    } else {
        document.getElementById('newPost').addEventListener('click', () => force_login());
    }    
    load_posts("",1);
});

function load_posts(addon,page) {        
    if (addon.includes("?")) {
        addon+=`&page=${page}`;
    } else {
        document.querySelector('#profile').style.display = 'none';
        addon+=`?page=${page}`;
    }
    console.log(`access ${addon}`);
    fetch(`/load${addon}`)
    .then(response => response.json())
    .then(response => {
        document.getElementById('posts').innerHTML="";
        build_paginator(addon,page,response.num_pages);
        response.posts.forEach(post => build_post(post));
    })
}

function build_paginator(addon,page,num_pages) {
    page_list = document.getElementById('pagination');
    page_list.innerHTML="";

    const previous = document.createElement('li');
    if(page==1){
        previous.className = "page-item disabled";    
    } else {
        previous.className = "page-item";    
        previous.addEventListener('click', () => load_posts(addon,page-1));
    }        
    const page_a_previous = document.createElement('a');
    page_a_previous.className="page-link";

    page_a_previous.href="#";
    page_a_previous.innerHTML="Previous";
    previous.append(page_a_previous);    
    page_list.append(previous);
    
    for (let item=1; item<=num_pages; item++) {
        const page_icon = document.createElement('li');        
        if(item==page) {
            page_icon.className = "page-item active";
        } else {
            page_icon.className = "page-item";    
            page_icon.addEventListener('click', () => load_posts(addon,item));
        }        
        const page_a = document.createElement('a');
        page_a.className="page-link";
        page_a.href="#";
        page_a.innerHTML=item;
        page_icon.append(page_a);

        page_list.append(page_icon);
    }
    
    const next = document.createElement('li');        
    if(page==num_pages){
        next.className = "page-item disabled";    
    } else {
        next.className = "page-item";    
        next.addEventListener('click', () => load_posts(addon,page+1));
    }   
    const page_a_next = document.createElement('a');
    page_a_next.className="page-link"; 
    page_a_next.href="#";
    page_a_next.innerHTML="Next";
    next.append(page_a_next);
    page_list.append(next);
    
}

function show_profile(creator_id) {
    load_posts(`?profile=${creator_id}`,1);
    document.querySelector('#newPost').style.display = 'none';  
    follow_button = document.getElementById('follow-button'); 
    follow_button.style.display = 'none';
    document.querySelector('#profile').style.display = 'block';  
    fetch(`/profile/${creator_id}`)
    .then(response => response.json())
    .then(profile => {
        document.getElementById('following-amount').innerHTML=profile.following;
        document.getElementById('followers-amount').innerHTML=profile.followers;
        document.getElementById('profile_username').innerHTML=profile.profile_username;
        if(profile.follow_available) {               
            follow_button.style.display = 'unset'; 
            if(profile.currently_following) {
                follow_button.innerHTML = 'Unfollow';    
            } else {
                follow_button.innerHTML = 'Follow';    
            }
            follow_button.addEventListener('click', () => update_follow(creator_id) );
        }
    })
    window.scrollTo(0,0);
    
}

function build_post(post) {
    const post_card = document.createElement('div');
    post_card.className = "card col col-6";

    const header = document.createElement('div');
    header.className = "card-header profile";
    header.innerHTML = post.creator_username;
    post_card.append(header);
    header.addEventListener('click', () => show_profile(post.creator_id) );

    const card_body = document.createElement('div');
    card_body.className = "card-body";
    card_body.id = `post_body_${post.id}`;
    
    const text = document.createElement('p');
    text.className = "card-text";
    text.id = `content_${post.id}`;
    text.innerHTML = post.content;
    card_body.append(text);

    
    const likes_row = document.createElement('div');
    likes_row.id = `likes_row_${post.id}`;
    likes_row.className = "row align-items-center";

    const like_icon = document.createElement('i');
    like_icon.id = `like-icon-${post.id}`;
    let heart_bg;
    if(post.liked) {
        heart_bg="";
    } else {
        heart_bg="-empty";
    }
    like_icon.className = `icon-heart${heart_bg} col-auto`;
    if(document.getElementById('following')) {
        like_icon.addEventListener('click', () => update_like(post));        
    } else {
        like_icon.addEventListener('click', () => force_login());
    }
    
    likes_row.append(like_icon);


    const likes = document.createElement('div');
    likes.id = `likes-amount-${post.id}`;
    likes.className = "card-text likes col-auto ";
    likes.innerHTML = post.likes;
    likes_row.append(likes);

    const likes_text = document.createElement('div');
    likes_text.className = "card-text likes_text col-auto ";
    likes_text.innerHTML = " like(s)";
    likes_row.append(likes_text);

    const date = document.createElement('div');
    date.className = "blockquote-footer col-auto";
    date.innerHTML = post.created_date;
    likes_row.append(date);

    if(post.editable) {
        const edit = document.createElement('button');
        edit.className = "card-text col-auto btn btn-link";
        edit.innerHTML = "Edit";
        edit.addEventListener('click', () => edit_post(post) );
        likes_row.append(edit);
    }

    card_body.append(likes_row);    
    post_card.append(card_body);

    const row = document.createElement('div');
    row.className = "row justify-content-center";
    row.append(post_card);

    document.querySelector('#posts').append(row);
}

function update_like(post) {
    fetch(`/post/${post.id}/update_like`)
    .then(response => response.json())
    .then(response => {
        if (response.liked) {
            document.getElementById(`like-icon-${post.id}`).className = "icon-heart col-auto";
        } else {
            document.getElementById(`like-icon-${post.id}`).className = "icon-heart-empty col-auto";
        }
        document.getElementById(`likes-amount-${post.id}`).innerHTML=response.newAmount;
    })
}

function update_follow(profile_id) {
    fetch(`/profile/${profile_id}/update_follow`)
    .then(response => response.json())
    .then(response => {
        follow_button = document.getElementById('follow-button'); 
        if (response.newFollower) {
            follow_button.innerHTML = "Unfollow";
        } else {
            follow_button.innerHTML = "Follow";
        }
        document.getElementById('followers-amount').innerHTML=response.newAmount;
    })
}

function edit_post(post) {
    const likes_row = document.getElementById(`likes_row_${post.id}`);    
    const content = document.getElementById(`content_${post.id}`);
        
    const post_body  = content.parentNode;    

    const edit_buttons_row = document.createElement('div');
    edit_buttons_row.className = "row";


    const save_button = document.createElement('button');
    save_button.className = "btn btn-info col-auto";
    save_button.type = "button";
    save_button.innerHTML = "Save it";
    save_button.addEventListener('click', () => {
        const new_content = document.getElementById(`new_content_${post.id}`).value;
        fetch(`/save_post`, {
            method: 'PUT',
            headers: {
                'X-CSRFToken': getCookie("csrftoken")
            },
            body: body = JSON.stringify({
              post_id: post.id,
              new_content: new_content,
            })
        })
        .then(response => response.json())
        .then(response => {
            if(response.result) {
                content.innerHTML = new_content;
            } else {
                alert("Edit not authorized");
            }
            edit_buttons_row.remove();
            content_editable.remove();
            post_body.append(content);
            post_body.append(likes_row);
        })
    })
    edit_buttons_row.append(save_button);
    

    const content_editable = document.createElement('input');
    content_editable.id = `new_content_${post.id}`;
    content_editable.type = "textarea";
    content_editable.className = "form-control col-8";
    content_editable.value = content.innerHTML;
    
    
    document.getElementById(`likes_row_${post.id}`).remove();
    document.getElementById(`content_${post.id}`).remove();
    
    edit_buttons_row.append(content_editable);

    const cancel_button = document.createElement('button');
    cancel_button.className = "btn btn-light col-auto";
    cancel_button.type = "button";
    cancel_button.innerHTML = "Cancel";
    cancel_button.addEventListener('click', () => {
        edit_buttons_row.remove();
        content_editable.remove();
        post_body.append(content);
        post_body.append(likes_row);                  
    });
    edit_buttons_row.append(cancel_button);
    post_body.appendChild(edit_buttons_row);    
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
  }

function force_login() {
    document.getElementById('login').click();
}
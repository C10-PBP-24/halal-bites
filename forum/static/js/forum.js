document.getElementById('postForm').addEventListener('submit', function(e) {
    e.preventDefault();  // Prevent the default form submission behavior

    const form = document.getElementById('postForm');
    const formData = new FormData(form);
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch(form.action, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken
        },
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            // Post created successfully
            alert('Post created successfully!');
    
            // Create a new post element
            const newPost = `
                <div class="post-item">
                    <p>${formData.get('content')}</p>
                    <p>Posted on now by You</p>
                </div>
            `;
    
            // Append the new post to the post list
            const postList = document.getElementById('postList');  // Make sure your posts are inside an element with this ID
            postList.innerHTML += newPost;
    
            // Hide the modal and clear the form
            document.getElementById('postModal').classList.add('hidden');
            form.reset();  // Clear the form fields
        } else {
            alert('Failed to create post');
        }
    })
    
    .catch(error => console.error('Error:', error));
});

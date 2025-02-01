// Function to toggle between Sign In and Sign Up modes in the modal
function toggleModal(type) {
    const modalTitle = document.getElementById('signInModalLabel');
    const submitBtn = document.getElementById('submitBtn');
    const toggleLink = document.getElementById('toggleLink');
    const toggleText = document.getElementById('toggleText');

    if (type === 'signIn') {
        // Switch to Sign In
        modalTitle.innerText = 'Sign In';
        submitBtn.innerText = 'Sign In';
        toggleLink.innerText = 'Sign Up';
        toggleText.innerHTML = `Don't have an Account? <a href="#" onclick="toggleModal('signUp')" id="toggleLink">Sign Up</a>`;
    } else {
        // Switch to Sign Up
        modalTitle.innerText = 'Sign Up';
        submitBtn.innerText = 'Sign Up';
        toggleLink.innerText = 'Sign In';
        toggleText.innerHTML = `Already have an Account? <a href="#" onclick="toggleModal('signIn')" id="toggleLink">Sign In</a>`;
    }
}

// Handling form submission (sign-in or sign-up) using fetch
document.getElementById('submitBtn').addEventListener('click', function (event) {
    event.preventDefault();  // Prevent default form submission

    const email = document.getElementById('email').value;
    const password = document.getElementById('pass').value;
    const form = document.getElementById('authForm');

    const isSignUp = document.getElementById('submitBtn').innerText === 'Sign Up'; // Check if it's Sign Up or Sign In
    const url = isSignUp ? '/signup/' : '/signin/'; // Decide the URL based on the button text
    const method = 'POST';

    const formData = new FormData(form);  // Collect form data

    // Use fetch to submit form via AJAX
    fetch(url, {
        method: method,
        body: formData,
    })
        .then(response => response.json())
        .then(data => {
            // Check if the response is success or error
            if (data.success) {
                // Display success message and close modal
                const modal = bootstrap.Modal.getInstance(document.getElementById('signInModal'));
                modal.hide();
                alert(data.message);  // You can replace this with a custom notification
            } else {
                // Display error message
                alert(data.message);  // Show error message
            }
        })
        .catch(error => {
            alert('An error occurred: ' + error);  // Handle any fetch errors
        });
});

const modal = bootstrap.Modal.getInstance(document.getElementById('signInModal'));
modal.hide();  // Hide the modal on page load
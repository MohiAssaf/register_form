let registerForm = document.getElementById('register');

registerForm.addEventListener('submit', (e) => {
    e.preventDefault();

    var formData = {
        firstName: document.getElementById('first_name').value,
        lastName: document.getElementById('last_name').value,
        email: document.getElementById('email').value,
        username: document.getElementById('username').value,
        password: document.getElementById('password').value,
        confirm_password: document.getElementById('repassword').value,
    }

    console.log(formData)
})
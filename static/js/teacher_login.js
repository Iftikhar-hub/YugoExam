const togglePassword = document.querySelector('#togglePassword');
const passwordField = document.querySelector('#typePasswordX');

togglePassword.addEventListener('click', function (e) {
    // Toggle the type attribute of the password field
    const type = passwordField.getAttribute('type') === 'password' ? 'text' : 'password';
    passwordField.setAttribute('type', type);

    // Toggle the icon to show the appropriate eye symbol
    this.classList.toggle('fa-eye-slash');
});
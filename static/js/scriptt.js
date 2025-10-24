document.addEventListener('scroll', function () {
    const reportingElement = document.querySelector('.box1');
    const elementPosition = reportingElement.getBoundingClientRect().top;
    const offset = 600; // Increase this value to trigger the effect earlier
    const viewHeight = window.innerHeight;

    // Check if the element's top is within the defined offset from the top of the viewport
    if (elementPosition <= offset) {
        reportingElement.classList.add('visible');
    } else {
        reportingElement.classList.remove('visible');
    }
});

document.addEventListener('scroll', function () {
    const imageElement = document.querySelector('.image-content img');
    const elementPosition = imageElement.getBoundingClientRect().top;
    const offset = 600; // Adjust this value to trigger the effect earlier

    // Check if the image's top is within the defined offset from the top of the viewport
    if (elementPosition <= offset) {
        imageElement.classList.add('visible');
    } else {
        imageElement.classList.remove('visible');
    }
});

// Get the current URL path
const currentPage = window.location.pathname;

// Get all nav-links
const navLinks = document.querySelectorAll('.nav-link');

// Loop through each nav-link and check its href against the current page
navLinks.forEach(link => {
    // Extract the last part of the href (i.e., "index.html", "about.html", etc.)
    const linkPage = link.getAttribute('href');

    // Check if the current page matches the href of the nav-link
    if (currentPage.includes(linkPage)) {
        // Add the 'active' class to the matching nav-link
        link.classList.add('active');
    }
});


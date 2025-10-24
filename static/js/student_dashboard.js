
document.addEventListener('DOMContentLoaded', function () {
    const profileDropdown = document.getElementById('profileDropdown');
    const dropdownMenu = document.getElementById('dropdownMenu');

    if (!profileDropdown || !dropdownMenu) {
        console.error('Profile dropdown or dropdown menu element is missing.');
        return;
    }

    profileDropdown.addEventListener('click', function () {
        const isExpanded = profileDropdown.getAttribute('aria-expanded') === 'true';
        dropdownMenu.style.display = isExpanded ? 'none' : 'block';
        profileDropdown.setAttribute('aria-expanded', !isExpanded);
    });

    window.addEventListener('click', function (event) {
        if (!profileDropdown.contains(event.target) && !dropdownMenu.contains(event.target)) {
            dropdownMenu.style.display = 'none';
            profileDropdown.setAttribute('aria-expanded', 'false');
        }
    });
});

//  side bar toggle****************************
document.addEventListener('DOMContentLoaded', function () {
    const toggleButton = document.getElementById('toggleSidebar'); // The toggle button icon
    const sidebar = document.querySelector('.sidebar'); // The sidebar element
    const mainContent = document.querySelector('.main-content'); // Main content

    toggleButton.addEventListener('click', function () {
        sidebar.classList.toggle('collapsed'); // Toggle sidebar visibility
        mainContent.classList.toggle('expanded'); // Toggle content width
    });
});

// Exam examsDropdown*********************************

document.addEventListener('DOMContentLoaded', function () {
    const examsToggle = document.getElementById('examsToggle');
    const examsDropdown = document.getElementById('examsDropdown');
    const examsArrow = document.getElementById('examsArrow'); // Arrow icon element

    examsToggle.addEventListener('click', function (event) {
        event.preventDefault(); // Prevent default link behavior

        // Toggle the dropdown visibility with animation
        if (examsDropdown.style.display === "none" || !examsDropdown.style.display) {
            examsDropdown.style.display = "block"; // Show the dropdown
            setTimeout(function () {
                examsDropdown.classList.add('open'); // Add the 'open' class to animate
            }, 10); // Small delay for animation to apply

            // Change the arrow direction to point upward
            examsArrow.classList.remove('fa-arrow-down');
            examsArrow.classList.add('fa-arrow-up');
        } else {
            examsDropdown.classList.remove('open'); // Remove the 'open' class for animation
            setTimeout(function () {
                examsDropdown.style.display = "none"; // Hide the dropdown after animation
            }, 500); // Same duration as the animation time (0.5s)

            // Change the arrow direction back to downward
            examsArrow.classList.remove('fa-arrow-up');
            examsArrow.classList.add('fa-arrow-down');
        }
    });
});

document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.unroll-btn').forEach(button => {
        button.addEventListener('click', function () {
            const courseId = this.getAttribute('data-course-id');

            fetch(`/unroll_course/${courseId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': '{{ csrf_token }}',
                    'Content-Type': 'application/json'
                }
            }).then(response => response.json()).then(data => {
                if (data.status === 'unrolled') {
                    this.closest('li').remove();  // Remove the course from the list
                }
            });
        });
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const dashboardLink = document.getElementById('dashboardLink');
    const dashboardContent = document.getElementById('dashboardContent');

    const coursesLink = document.getElementById('coursesLink');
    const coursesContent = document.getElementById('coursesContent');

    const takeExamLink = document.getElementById('takeExamLink');
    const takeExamContent = document.getElementById('takeExamContent');

    dashboardLink.addEventListener('click', function (event) {
        event.preventDefault();
        dashboardContent.style.display = 'block'; 
        takeExamContent.style.display = 'none';
        examsDropdown.style.display = 'none'; 
        questionBankContent.style.display = 'none'; 
        coursesContent.style.display = 'none';
        examsArrow.classList.remove('fa-arrow-up');
        examsArrow.classList.add('fa-arrow-down');

    });

    coursesLink.addEventListener('click', function (event) {
        event.preventDefault();
        coursesContent.style.display = 'block'; 
        takeExamContent.style.display = 'none';
        dashboardContent.style.display = 'none'; 
        questionBankContent.style.display = 'none'; 
    });

    takeExamLink.addEventListener('click', function (event) {
        event.preventDefault();
        takeExamContent.style.display = 'block';
        coursesContent.style.display = 'none';
        dashboardContent.style.display = 'none';
        questionBankContent.style.display = 'none';
    });
});

// static/js/calendar.js

const calendarBody = document.getElementById('calendar-body');
const monthYear = document.getElementById('month-year');
const prevMonthBtn = document.getElementById('prev-month');
const nextMonthBtn = document.getElementById('next-month');

let currentDate = new Date();
let today = new Date(); // This is the current day

function renderCalendar() {
    // Clear previous calendar cells
    calendarBody.innerHTML = '';

    const year = currentDate.getFullYear();
    const month = currentDate.getMonth();

    // Get the first day of the month
    const firstDay = new Date(year, month, 1).getDay();

    // Get the number of days in the month
    const daysInMonth = new Date(year, month + 1, 0).getDate();

    // Update the month and year display
    monthYear.textContent = currentDate.toLocaleString('default', { month: 'long', year: 'numeric' });

    // Create blank cells for the days before the first day
    for (let i = 0; i < firstDay; i++) {
        const blankCell = document.createElement('div');
        blankCell.classList.add('day');
        calendarBody.appendChild(blankCell);
    }

    // Create cells for each day of the month
    for (let day = 1; day <= daysInMonth; day++) {
        const dayCell = document.createElement('div');
        dayCell.classList.add('day');
        dayCell.textContent = day;

        // Check if the current date matches today's date and apply inline styles
        if (
            day === today.getDate() &&
            month === today.getMonth() &&
            year === today.getFullYear()
        ) {
            dayCell.style.backgroundColor = 'rgb(255, 146, 0)'; 
            dayCell.style.color = 'green';
            dayCell.style.fontWeight = 'bold';
            dayCell.style.fontSize = '30px'
        }

        calendarBody.appendChild(dayCell);
    }
}

// Change month
prevMonthBtn.addEventListener('click', () => {
    currentDate.setMonth(currentDate.getMonth() - 1);
    renderCalendar();
});

nextMonthBtn.addEventListener('click', () => {
    currentDate.setMonth(currentDate.getMonth() + 1);
    renderCalendar();
});

// Initial render
renderCalendar();

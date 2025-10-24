// Example: Chart.js configuration for student progress
const ctx1 = document.getElementById('studentProgressChart').getContext('2d');
const studentProgressChart = new Chart(ctx1, {
    type: 'bar',
    data: {
        labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
        datasets: [{
            label: 'Progress (%)',
            data: [85, 92, 78, 88],
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 1
        }]
    }
});

// Example: Chart.js configuration for exam performance
const ctx2 = document.getElementById('examPerformanceChart').getContext('2d');
const examPerformanceChart = new Chart(ctx2, {
    type: 'line',
    data: {
        labels: ['Exam 1', 'Exam 2', 'Exam 3', 'Exam 4'],
        datasets: [{
            label: 'Scores',
            data: [75, 80, 85, 90],
            backgroundColor: 'rgba(153, 102, 255, 0.2)',
            borderColor: 'rgba(153, 102, 255, 1)',
            borderWidth: 1
        }]
    }
});
// document.getElementById('sidebarToggle').addEventListener('click', function () {
//     const sidebar = document.getElementById('sidebar');
//     sidebar.classList.toggle('collapsed');
// });


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

// <!-- *********** Create Exam Section ************************** -->

document.addEventListener('DOMContentLoaded', function () {
    const dashboardLink = document.getElementById('dashboardLink');
    const dashboardContent = document.getElementById('dashboardContent');

    const createExamLink = document.getElementById('createExamLink');
    const createExamContent = document.getElementById('createExamContent');

    const questionBankToggle = document.getElementById('questionBankToggle');
    const questionBankContent = document.getElementById('questionBankContent');

    const coursesLink = document.getElementById('coursesLink');
    const coursesContent = document.getElementById('coursesContent');

    const multipleExamLink = document.getElementById('multipleExamLink');
    const multipleExamContent = document.getElementById('multipleExamContent');

    const subjectiveExamLink = document.getElementById('subjectiveExamLink');
    const subjectiveExamContent = document.getElementById('subjectiveExamContent');
    
    const shortEasyLink = document.getElementById('shortEasyLink');
    const shortEssayContent = document.getElementById('shortEssayContent');
    
    const addQuestionLink = document.getElementById('addQuestionLink'); 
    const addQuestionsContent = document.getElementById('addQuestionsContent');

    dashboardLink.addEventListener('click', function (event) {
        event.preventDefault();
        dashboardContent.style.display = 'block'; // Show dashboard content
        shortEssayContent.style.display = 'none';
        createExamContent.style.display = 'none'; // Hide create exam content
        examsDropdown.style.display = 'none'; // Hide create exam content
        questionBankContent.style.display = 'none'; // Hide exam bank exam content
        coursesContent.style.display = 'none'; 
        examsArrow.classList.remove('fa-arrow-up');
        examsArrow.classList.add('fa-arrow-down'); 
        multipleExamContent.style.display = 'none';
        subjectiveExamContent.style.display = 'none';
        addQuestionsContent.style.display = 'none';
        
    });

    createExamLink.addEventListener('click', function (event) {
        event.preventDefault();
        dashboardContent.style.display = 'none'; // Hide dashboard content
        createExamContent.style.display = 'block'; 
        shortEssayContent.style.display = 'none';
        subjectiveExamContent.style.display = 'none';
        questionBankContent.style.display = 'none'; 
        coursesContent.style.display = 'none'; 
        multipleExamContent.style.display = 'none';
        addQuestionsContent.style.display = 'none';
       
        
     
    });
    
    questionBankToggle.addEventListener('click', function (event) {
        event.preventDefault();
        dashboardContent.style.display = 'none'; // Hide dashboard content
        createExamContent.style.display = 'none'; 
        questionBankContent.style.display = 'block'; 
        coursesContent.style.display = 'none'; 
        multipleExamContent.style.display = 'none';
        addQuestionsContent.style.display = 'none';
        subjectiveExamContent.style.display = 'none';
        shortEssayContent.style.display = 'none';
     
    });

    coursesLink.addEventListener('click', function (event) {
        event.preventDefault();
        dashboardContent.style.display = 'none'; // Hide dashboard content
        createExamContent.style.display = 'none'; // Hide create exam content
        questionBankContent.style.display = 'none'; // Hide exam bank content
        coursesContent.style.display = 'block'; // Show courses content
        shortEssayContent.style.display = 'none';
        multipleExamContent.style.display = 'none';
        addQuestionsContent.style.display = 'none';
        subjectiveExamContent.style.display = 'none';
        
    });

    multipleExamLink.addEventListener('click', function (event) {
        event.preventDefault();
        dashboardContent.style.display = 'none'; // Hide dashboard content
        multipleExamContent.style.display = 'block'; // Show create exam content
        shortEssayContent.style.display = 'none';
        createExamContent.style.display = 'none'; // Hide create exam content
        questionBankContent.style.display = 'none'; // Hide exam bank content
        coursesContent.style.display = 'none';
        addQuestionsContent.style.display = 'none';
        subjectiveExamContent.style.display = 'none';
        
    });
    subjectiveExamLink.addEventListener('click', function (event) {
        event.preventDefault();
        subjectiveExamContent.style.display = 'block';
        shortEssayContent.style.display = 'none';
        dashboardContent.style.display = 'none'; // Hide dashboard content
        multipleExamContent.style.display = 'none'; 
        createExamContent.style.display = 'none'; // Hide create exam content
        questionBankContent.style.display = 'none'; // Hide exam bank content
        coursesContent.style.display = 'none';
        addQuestionsContent.style.display = 'none';
       
       
        
    });

    shortEasyLink.addEventListener('click', function (event) {
        event.preventDefault();
        shortEssayContent.style.display = 'block';
        subjectiveExamContent.style.display = 'none';
        dashboardContent.style.display = 'none'; // Hide dashboard content
        multipleExamContent.style.display = 'none'; 
        createExamContent.style.display = 'none'; // Hide create exam content
        questionBankContent.style.display = 'none'; // Hide exam bank content
        coursesContent.style.display = 'none';
        addQuestionsContent.style.display = 'none';
        
       
        
    });

    addQuestionLink.addEventListener('click', function (event) {
        event.preventDefault();
        createExamContent.style.display = 'none'; // Hide create exam content
        addQuestionsContent.style.display = 'block'; // Show add question content
        dashboardContent.style.display = 'none'; // Hide dashboard content
        questionBankContent.style.display = 'none';
        coursesContent.style.display = 'none';
        multipleExamContent.style.display = 'none';
        subjectiveExamContent.style.display = 'none';
        shortEssayContent.style.display = 'none';
    });
});


// ***************************publish exam start *********************
document.querySelectorAll('.publish-toggle').forEach(toggle => {
    toggle.addEventListener('change', function () {
        let examId = this.getAttribute('data-exam-id');
        let isChecked = this.checked;

        fetch(`/toggle-publish/${examId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': '{{ csrf_token }}',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ published: isChecked })
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Publish status updated!');
                } else {
                    alert('Error updating publish status');
                }
            })
            .catch(error => console.error('Error:', error));
    });
});

// ***************************publish exam end *********************


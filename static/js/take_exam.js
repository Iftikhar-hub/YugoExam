// Timer functionality
let totalTime = parseInt(document.getElementById("timer").dataset.totalTime); // Total time in seconds
const timerElement = document.getElementById("timer");

function updateTimer() {
    const minutes = Math.floor(totalTime / 60);
    const seconds = totalTime % 60;
    timerElement.innerHTML = `Time Remaining: ${minutes}:${seconds < 10 ? "0" + seconds : seconds}`;
    totalTime--;

    if (totalTime < 0) {
        clearInterval(timer);
        document.getElementById("exam-form").submit(); // Auto-submit when time is up
    }
}
const timer = setInterval(updateTimer, 1000);
updateTimer();

// Auto-save functionality
function autoSaveAnswers() {
    const formData = new FormData(document.getElementById("exam-form"));

    fetch(timerElement.dataset.autoSaveUrl, {
        method: "POST",
        headers: {
            "X-CSRFToken": timerElement.dataset.csrfToken, // CSRF token passed from Django template
        },
        body: formData,
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.success) {
                console.log("Answers auto-saved successfully!");
            } else {
                console.error("Auto-save failed:", data.message);
            }
        })
        .catch((error) => console.error("Error during auto-save:", error));
}

// Trigger auto-save every 1 minute
setInterval(autoSaveAnswers, 60000); // 60000 ms = 1 minute


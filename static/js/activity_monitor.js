// Full-Screen Mode Lock
document.documentElement.requestFullscreen();

document.addEventListener("DOMContentLoaded", function () {
    // ---------- TAB / WINDOW SWITCHING DETECTION ----------
    let tabOffenseCount = 0;

    document.addEventListener("visibilitychange", function () {
        if (document.hidden) {
            // Increase offense count on every tab switch/minimize event
            tabOffenseCount++;
            if (tabOffenseCount === 1) {
                alert("Warning: You have switched tabs or minimized the window. Next time, the exam will be terminated!");
            } else if (tabOffenseCount >= 2) {
                alert("Exam terminated due to repeated tab switching/minimizing. Unattempted questions will be canceled.");
                terminateExam();
            }
        }
    });

    // ---------- CAMERA MONITORING ----------
    let cameraOffenseCount = 0;
    let darkCounter = 0; // Counts consecutive seconds of low brightness
    const brightnessThreshold = 50; // Adjust this threshold as needed (0 to 255)

    setInterval(function () {
        const video = document.getElementById("webcam");
        if (!video || video.readyState < 2) {
            return; // Not enough data to analyze yet.
        }
        // Create a canvas to capture the video frame
        const canvas = document.createElement("canvas");
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        const ctx = canvas.getContext("2d");
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
        const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
        const data = imageData.data;
        let totalBrightness = 0;
        // Sum brightness for each pixel (using standard luminance formula)
        for (let i = 0; i < data.length; i += 4) {
            const r = data[i];
            const g = data[i + 1];
            const b = data[i + 2];
            const brightness = 0.2126 * r + 0.7152 * g + 0.0722 * b;
            totalBrightness += brightness;
        }
        const avgBrightness = totalBrightness / (data.length / 4);

        if (avgBrightness < brightnessThreshold) {
            darkCounter++;
            if (darkCounter >= 3) { // 3 consecutive seconds of low brightness
                cameraOffenseCount++;
                if (cameraOffenseCount === 1) {
                    alert("Warning: Please keep your face visible to the camera.");
                } else if (cameraOffenseCount >= 2) {
                    alert("Exam terminated due to repeated camera blocking. Unattempted questions will be canceled.");
                    terminateExam();
                }
                darkCounter = 0; // Reset after an offense is recorded
            }
        } else {
            // Reset darkCounter if brightness returns to normal
            darkCounter = 0;
        }
    }, 1000);

    // ---------- START CAMERA ----------
    const cameraContainer = document.createElement("div");
    cameraContainer.id = "camera-container";
    cameraContainer.innerHTML = '<video id="webcam" autoplay muted playsinline></video>';
    document.body.appendChild(cameraContainer);

    navigator.mediaDevices.getUserMedia({ video: true })
        .then(stream => {
            const video = document.getElementById("webcam");
            video.srcObject = stream;
        })
        .catch(error => {
            console.error("Error accessing webcam:", error);
        });

    // ---------- TERMINATE EXAM FUNCTION ----------
    function terminateExam() {
        // Disable all unanswered questions so that only attempted questions are submitted
        const questionBoxes = document.querySelectorAll(".question-box");
        questionBoxes.forEach(qBox => {
            const inputs = qBox.querySelectorAll("input");
            let answered = Array.from(inputs).some(input => input.checked);
            if (!answered) {
                inputs.forEach(input => input.disabled = true);
            }
        });
        // Submit the exam form immediately
        document.getElementById("exam-form").submit();
    }
});

// Keystroke Logging (For Activity Monitoring)
document.addEventListener('keydown', function (event) {
    console.log('Key pressed: ' + event.key);
    // Optionally, send this data to the server for analysis
});

// Microphone Monitoring (Basic Audio Detection)
navigator.mediaDevices.getUserMedia({ audio: true })
    .then(function (stream) {
        const audioContext = new AudioContext();
        const analyser = audioContext.createAnalyser();
        const microphone = audioContext.createMediaStreamSource(stream);

        microphone.connect(analyser);
        setInterval(function () {
            const bufferLength = analyser.frequencyBinCount;
            const dataArray = new Uint8Array(bufferLength);
            analyser.getByteFrequencyData(dataArray);

            // Placeholder for audio pattern detection
            console.log("Analyzing audio for suspicious activity...");
        }, 1000);  // Check audio every second
    })
    .catch(function (err) {
        console.log('Microphone access denied: ' + err);
    });

// Toggle Theme Functionality
document.addEventListener("DOMContentLoaded", function () {
    const themeToggleButton = document.getElementById("theme-toggle");
    const body = document.body;

    // Check for saved theme in local storage
    const savedTheme = localStorage.getItem("theme");
    if (savedTheme) {
        body.classList.add(savedTheme);
        updateButtonText(savedTheme);
    }

    themeToggleButton.addEventListener("click", function () {
        if (body.classList.contains("dark-mode")) {
            body.classList.remove("dark-mode");
            body.classList.add("light-mode");
            localStorage.setItem("theme", "light-mode");
            updateButtonText("light-mode");
        } else {
            body.classList.remove("light-mode");
            body.classList.add("dark-mode");
            localStorage.setItem("theme", "dark-mode");
            updateButtonText("dark-mode");
        }
    });

    function updateButtonText(theme) {
        themeToggleButton.textContent = theme === "dark-mode" ? "☀️ Light Mode" : "🌙 Dark Mode";
    }
});

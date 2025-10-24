document.addEventListener("DOMContentLoaded", function () {
    const examType = document.body.getAttribute("data-exam-type");

    // ===================== MCQs Timer  =====================
    const mcqTimerContainer = document.getElementById("mcq-timer-container");
    const totalQuestions = document.querySelectorAll(".question-box[data-type='MCQ']").length;
    let totalTime = totalQuestions * 60;

    const minutesDisplay = document.getElementById("minutes");
    const secondsDisplay = document.getElementById("seconds");
    const minutesCircle = document.getElementById("minutes-circle");
    const secondsCircle = document.getElementById("seconds-circle");

    let remainingTime = totalTime;
    let timerInterval = null;

    function updateTimer() {
        if (remainingTime <= 0) {
            clearInterval(timerInterval);
            handleTimeout();
            return;
        }

        let minutes = Math.floor(remainingTime / 60);
        let seconds = remainingTime % 60;

        if (minutesDisplay && secondsDisplay) {
            minutesDisplay.textContent = minutes.toString().padStart(2, "0");
            secondsDisplay.textContent = seconds.toString().padStart(2, "0");
        }

        if (minutesCircle && secondsCircle) {
            let minutesProgress = (remainingTime / totalTime) * 184;
            let secondsProgress = (seconds / 60) * 184;
            minutesCircle.style.strokeDashoffset = 184 - minutesProgress;
            secondsCircle.style.strokeDashoffset = 184 - secondsProgress;
        }

        remainingTime--;
    }

    function handleTimeout() {
        alert("Time's up! Submitting your exam.");
        document.getElementById("exam-form").submit();
    }

    if (totalQuestions > 0 && examType === "MC") {
        mcqTimerContainer.style.display = "Flex";
        timerInterval = setInterval(updateTimer, 1000);
        updateTimer();
    } else {
        mcqTimerContainer.style.display = "none";
    }

    // ===================== Subjective Questions Timer  =====================
    const subjectiveTimerContainer = document.getElementById("subjective-timer-container");
    const subjectiveMinutesDisplay = document.getElementById("subjective-minutes");
    const subjectiveSecondsDisplay = document.getElementById("subjective-seconds");
    const subjectiveMinutesCircle = document.getElementById("subjective-minutes-circle");
    const subjectiveSecondsCircle = document.getElementById("subjective-seconds-circle");

    let totalSubjectiveMarks = 0;
    const subjectiveQuestions = document.querySelectorAll(".question-box[data-type='Subjective']");

    subjectiveQuestions.forEach(question => {
        const marks = parseInt(question.getAttribute("data-marks"), 10) || 0;
        totalSubjectiveMarks += marks;
    });

    let subjectiveTotalTime = totalSubjectiveMarks * 3 * 60;
    let subjectiveRemainingTime = subjectiveTotalTime;
    let subjectiveTimerInterval = null;

    function updateSubjectiveTimer() {
        if (subjectiveRemainingTime <= 0) {
            clearInterval(subjectiveTimerInterval);
            alert("Time's up for subjective questions! Submitting your exam.");
            document.getElementById("exam-form").submit();
            return;
        }

        let minutes = Math.floor(subjectiveRemainingTime / 60);
        let seconds = subjectiveRemainingTime % 60;

        if (subjectiveMinutesDisplay && subjectiveSecondsDisplay) {
            subjectiveMinutesDisplay.textContent = minutes.toString().padStart(2, "0");
            subjectiveSecondsDisplay.textContent = seconds.toString().padStart(2, "0");
        }

        if (subjectiveMinutesCircle && subjectiveSecondsCircle) {
            let minutesProgress = (subjectiveRemainingTime / subjectiveTotalTime) * 184;
            let secondsProgress = (seconds / 60) * 184;
            subjectiveMinutesCircle.style.strokeDashoffset = 184 - minutesProgress;
            subjectiveSecondsCircle.style.strokeDashoffset = 184 - secondsProgress;
        }

        subjectiveRemainingTime--;
    }

    if (subjectiveQuestions.length > 0 && (examType === "ST" || examType === "SE")) {
        subjectiveTimerContainer.style.display = "Flex";
        subjectiveTimerInterval = setInterval(updateSubjectiveTimer, 1000);
        updateSubjectiveTimer();
    } else {
        subjectiveTimerContainer.style.display = "none";
    }
});

let correctIncorrectChart = null;
let topicDistributionChart = null;

function updateCharts(data) {
    const correctIncorrectCtx = document.getElementById('correct-incorrect-chart').getContext('2d');
    const topicDistributionCtx = document.getElementById('topic-distribution-chart').getContext('2d');

    if (correctIncorrectChart) correctIncorrectChart.destroy();
    if (topicDistributionChart) topicDistributionChart.destroy();

    // Calculate average percentages for correctness
    const percentages = data.details.map(item => {
        const match = item.status.match(/\d+/);
        const correctPercent = match ? parseInt(match[0]) : 0;
        return correctPercent;
    });

    const averageCorrect = data.correctPercent;
    const averageIncorrect = data.incorrectPercent;


    // Correct vs Incorrect Percentage Chart
    correctIncorrectChart = new Chart(correctIncorrectCtx, {
        type: 'bar',
        data: {
            labels: ['Correct (%)', 'Incorrect (%)'],
            datasets: [{
                label: 'Answer Accuracy (%)',
                data: [averageIncorrect, averageCorrect,],
                backgroundColor: ['green', 'red'],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    title: {
                        display: true,
                        text: 'Percentage'
                    }
                }
            },
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            return `${context.label}: ${context.parsed.y}%`;
                        }
                    }
                }
            }
        }
    });

    // Topic Distribution Pie Chart
    if (data.topics && typeof data.topics === 'object') {
        const topicLabels = Object.keys(data.topics);
        const topicData = topicLabels.map(topic => data.topics[topic]);

        topicDistributionChart = new Chart(topicDistributionCtx, {
            type: 'pie',
            data: {
                labels: topicLabels,
                datasets: [{
                    label: 'Topic Distribution',
                    data: topicData,
                    backgroundColor: [
                        '#FF6384', '#36A2EB', '#FFCE56', '#FF5733', '#C70039',
                        '#8E44AD', '#1ABC9C', '#34495E', '#F39C12', '#2ECC71'
                    ],
                    hoverOffset: 4
                }]
            }
        });
    } else {
        console.warn('No topic data to display');
    }
}

function loadAnalysis(examId, exam_type) {
    if (exam_type === "MC") {
        alert("Analysis is only available for subjective exams.");
        return;
    }

    const analysisSection = document.getElementById("analysis-section");
    const isVisible = analysisSection.style.display === "block";

    if (isVisible) {
        analysisSection.style.display = "none";
        return;
    }

    analysisSection.style.display = "block";

    fetch(`/exam/analysis/${examId}/`)
        .then(response => {
            if (!response.ok) throw new Error("Network response was not OK");
            return response.json();
        })
        .then(data => {
            const resultsTable = document.getElementById("results-body");
            resultsTable.innerHTML = "";

            data.details.forEach(item => {
                const row = document.createElement("tr");

                const qCell = document.createElement("td");
                qCell.textContent = item.question;
                row.appendChild(qCell);

                const yourAnswerCell = document.createElement("td");
                yourAnswerCell.textContent = item.your_answer;
                row.appendChild(yourAnswerCell);

                const correctAnswerCell = document.createElement("td");
                correctAnswerCell.textContent = item.correct_answer;
                row.appendChild(correctAnswerCell);

                const statusCell = document.createElement("td");
                const isCorrect = item.status.startsWith("Correct");
                const statusColor = isCorrect ? "green" : "red";
                const displayStatus = isCorrect ? "Satisfied" : "Need Improvement";

                statusCell.innerHTML = `<span style="color: ${statusColor};">${displayStatus}</span>`;

                if (!isCorrect) {
                    const percentage = parseInt(item.status.match(/\d+/)?.[0] || "0", 10);
                    statusCell.innerHTML += `<br><span style="color: ${statusColor};">${percentage}%</span>`;
                }

                row.appendChild(statusCell);

                const topicCell = document.createElement("td");
                topicCell.innerHTML = `<a href="${item.external_link}" target="_blank">${item.topic}</a>`;
                row.appendChild(topicCell);

                resultsTable.appendChild(row);
            });

            document.getElementById("correct-count").textContent = `${data.correct} questions`;
            document.getElementById("incorrect-count").textContent = `${data.incorrect} questions`;

            updateCharts({
                ...data,
                correctPercent: data.average_correct,
                incorrectPercent: data.average_incorrect
            });

        })
        .catch(error => {
            console.error("Error loading analysis:", error);
            alert("Failed to load analysis. Please try again later.");
        });
}

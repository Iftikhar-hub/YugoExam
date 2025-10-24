function toggleResults(examId, button) {
    const row = document.getElementById(`results-${examId}`);
    if (!row) return;

    const isVisible = row.style.display === 'table-row';
    row.style.display = isVisible ? 'none' : 'table-row';
    button.textContent = isVisible ? 'View Results' : 'Hide Results';
}

function toggleAnalysis(studentExamId, button) {
    const row = document.getElementById(`analysis-${studentExamId}`);
    if (!row) return;

    const isVisible = row.style.display === 'table-row';
    row.style.display = isVisible ? 'none' : 'table-row';
    button.textContent = isVisible ? 'View Analysis' : 'Hide Analysis';
}

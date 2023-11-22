function toggleGraphs() {
    var graphsContainer = document.getElementById('graphs-container');
    var toggleButton = document.getElementById('toggle-button');

    if (graphsContainer.style.display === 'none' || graphsContainer.style.display === '') {
        graphsContainer.style.display = 'block';
        toggleButton.textContent = 'Hide Graphs';
    } else {
        graphsContainer.style.display = 'none';
        toggleButton.textContent = 'Show Graphs';
    }
}
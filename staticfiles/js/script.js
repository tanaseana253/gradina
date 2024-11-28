document.addEventListener('DOMContentLoaded', function() {
    const toggleButton = document.getElementById('toggleButton');

    toggleButton.addEventListener('click', function() {
        this.classList.toggle('btn-primary');
        this.classList.toggle('btn-success');
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const heart = document.getElementById('heart');
    const isFavorite = localStorage.getItem('favorite') === 'true';

    if (isFavorite) {
        heart.classList.add('red');
    }

    heart.addEventListener('click', function() {
        heart.classList.toggle('red');
        localStorage.setItem('favorite', heart.classList.contains('red'));
    });
});

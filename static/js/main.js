// static/js/main.js

// Auto-hide des messages flash après 5 secondes
document.addEventListener('DOMContentLoaded', function() {
    const flashMessages = document.querySelectorAll('.flash-message');
    
    flashMessages.forEach(msg => {
        setTimeout(() => {
            msg.style.transition = 'opacity 0.5s, transform 0.5s';
            msg.style.opacity = '0';
            msg.style.transform = 'translateX(-20px)';
            setTimeout(() => msg.remove(), 500);
        }, 5000);
    });
    
    // Animation d'entrée pour les nouvelles tâches
    const newTaskRow = document.querySelector('.task-enter');
    if (newTaskRow) {
        newTaskRow.style.animation = 'fadeIn 0.4s ease';
    }
    
    // Confirmation avant suppression
    document.querySelectorAll('.btn-delete').forEach(link => {
        link.addEventListener('click', function(e) {
            if (!confirm('Êtes-vous sûr de vouloir supprimer cette tâche ?')) {
                e.preventDefault();
            }
        });
    });
});

// Fonction utilitaire pour les requêtes fetch
async function apiRequest(url, method = 'GET', data = null) {
    const options = {
        method,
        headers: {
            'Content-Type': 'application/json',
        }
    };
    
    if (data) {
        options.body = JSON.stringify(data);
    }
    
    try {
        const response = await fetch(url, options);
        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}
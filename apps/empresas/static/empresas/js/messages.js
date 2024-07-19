document.addEventListener("DOMContentLoaded", function() {
    function showMessage(message, type) {
        alert(message);
    }

    const messages = JSON.parse(document.getElementById('django-messages').textContent);
    messages.forEach(function(message) {
        showMessage(message.message, message.tags);
    });
});
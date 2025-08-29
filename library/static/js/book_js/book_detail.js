document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll('form button[onclick]').forEach(button => {
        button.addEventListener('click', function (event) {
            if (!confirm('Сигурни ли сте, че искате да изтриете това ревю?')) {
                event.preventDefault();
            }
        });
    });
});

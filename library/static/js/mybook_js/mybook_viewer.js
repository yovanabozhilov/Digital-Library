document.addEventListener("DOMContentLoaded", function () {
    const toggleBtn = document.querySelector("#toggle-edit-title");
    const editForm = document.querySelector("#edit-title-form");

    if (toggleBtn && editForm) {
        editForm.style.display = "none";

        toggleBtn.addEventListener("click", function (e) {
            e.preventDefault();
            editForm.style.display = editForm.style.display === "none" ? "block" : "none";
        });
    }

    document.querySelectorAll("form.delete-chapter-form").forEach(form => {
        form.addEventListener("submit", function (e) {
            if (!confirm("Наистина ли искате да изтриете тази глава?")) {
                e.preventDefault();
            }
        });
    });

    const deleteBookForm = document.querySelector("form.delete-book-form");
    if (deleteBookForm) {
        deleteBookForm.addEventListener("submit", function (e) {
            if (!confirm("Сигурни ли сте, че искате да изтриете тази книга?")) {
                e.preventDefault();
            }
        });
    }
});

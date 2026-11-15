
document.addEventListener("DOMContentLoaded", function () {

    // Confirm before deleting a patient
    const deleteForms = document.querySelectorAll(".delete-form");

    deleteForms.forEach(function (form) {
        form.addEventListener("submit", function (event) {

            const confirmed = confirm(
                "Are you sure you want to delete this patient record?"
            );

            if (!confirmed) {
                event.preventDefault();
            }

        });
    });

});

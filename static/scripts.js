document.addEventListener("DOMContentLoaded", function() {
    const addEmployeeButton = document.getElementById("addEmployeeButton");

    if (addEmployeeButton) {
        addEmployeeButton.addEventListener("click", function() {
            window.location.href = "/add_employeee";
        });
    }
});

document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();

        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});
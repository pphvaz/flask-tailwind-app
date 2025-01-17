const button = document.getElementById("mobile-menu-button");
const openMenuIcon = document.getElementById("open-menu");
const closeMenuIcon = document.getElementById("close-menu");
const mobileMenu = document.getElementById("mobile-menu");

// Set initial visibility on page load
openMenuIcon.classList.remove("hidden");
closeMenuIcon.classList.add("hidden");
mobileMenu.classList.add("hidden");

button.addEventListener("click", function () {
    openMenuIcon.classList.toggle("hidden");
    closeMenuIcon.classList.toggle("hidden");
    mobileMenu.classList.toggle("hidden");
});

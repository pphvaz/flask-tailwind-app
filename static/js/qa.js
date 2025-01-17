const qaButtons = document.querySelectorAll(".qa-item button");
qaButtons.forEach((button) => {
    button.addEventListener("click", function (event) {
        const qaItem = button.closest(".qa-item");
        const answerDiv = qaItem.querySelector("div");
        const svgIcon = button.querySelector("svg");
    
        answerDiv.classList.toggle("hidden");
        button.classList.toggle("border-b-2");
        svgIcon.classList.toggle("rotate-180") 
    });
});

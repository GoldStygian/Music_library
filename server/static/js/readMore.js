const desc = document.getElementById("descrizione");
const readMoreBtn = document.getElementById("readMoreBtn");

if (desc) {
    const maxLength = 250;
    const fullText = desc.textContent.trim();

    if (fullText.length > maxLength) {
        const truncatedText = fullText.slice(0, maxLength) + "...";
        desc.textContent = truncatedText;
        readMoreBtn.style.display = "inline-block";

        readMoreBtn.addEventListener("click", function () {
            if (desc.textContent === truncatedText) {
                desc.textContent = fullText;
                readMoreBtn.textContent = "Read Less";
            } else {
                desc.textContent = truncatedText;
                readMoreBtn.textContent = "Read More";
            }
        });
    }
}
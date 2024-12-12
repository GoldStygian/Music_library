// function getCookie(name) {
//     let cookieValue = null;
//     if (document.cookie && document.cookie !== '') {
//         const cookies = document.cookie.split(';');
//         for (let i = 0; i < cookies.length; i++) {
//             const cookie = cookies[i].trim();
//             if (cookie.substring(0, name.length + 1) === (name + '=')) {
//                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                 break;
//             }
//         }
//     }
//     return cookieValue;
// }

function initReadMore() {
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
}

document.addEventListener("DOMContentLoaded", function () {
    // Delegazione eventi per i link con classe `.ajax-link`
    document.body.addEventListener("click", function (e) {
        const link = e.target.closest(".ajax-link");
        if (link) {
            console.log("Link Ajax Found")
            e.preventDefault();
            const url = link.getAttribute("href");

            fetch(url, {
                headers: { "X-Requested-With": "XMLHttpRequest" }
            })
            .then(response => {
                if (!response.ok) throw new Error("Errore nel caricamento");
                return response.text();
            })
            .then(html => {
                document.getElementById("content").innerHTML = html;
                history.pushState(null, "", url);
                // Richiama la funzione per inizializzare lo script
                initReadMore();
            })
            .catch(error => console.error("Errore:", error));
        }
    });

    // Intercettazione del submit del form
    // const form = document.querySelector("form");
    // if (form) {
    //     console.log("Form trovato");
    //     form.addEventListener("submit", function (e) {
    //         e.preventDefault(); // Blocca l'invio normale del form

    //         const formData = new FormData(form);
    //         const csrftoken = getCookie('csrftoken');
    //         console.log("CSRF Token: ", csrftoken)

    //         fetch(form.action, {
    //             method: "POST",
    //             body: formData,
    //             headers: { 
    //                 "X-Requested-With": "XMLHttpRequest",
    //                 "X-CSRFToken": csrftoken
    //              }
    //         })
    //         .then(response => {
    //             if (!response.ok) throw new Error("Errore durante l'invio del form");
    //             return response.text();
    //         })
    //         .then(html => {
    //             console.log("Risposta ricevuta:", html);
    //             document.getElementById("form-response").innerHTML = JSON.parse(html).message;
    //         })
    //         .catch(error => {
    //             console.error("Errore:", error);
    //         });
    //     });
    // }

    // Gestione della navigazione con il pulsante "indietro" del browser
    window.addEventListener("popstate", function () {
        fetch(location.href, {
            headers: { "X-Requested-With": "XMLHttpRequest" }
        })
        .then(response => response.text())
        .then(html => document.getElementById("content").innerHTML = html)
        .catch(error => console.error("Errore:", error));
    });
});

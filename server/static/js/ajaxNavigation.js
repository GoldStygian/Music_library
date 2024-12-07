document.addEventListener("DOMContentLoaded", function () {
    // Delegazione eventi per i link con classe `.ajax-link`
    document.body.addEventListener("click", function (e) {
        console.log("Evento click catturato sul body");
        const link = e.target.closest(".ajax-link"); // Controlla se il click proviene da un `.ajax-link`
        if (link) {
            e.preventDefault(); // Evita il comportamento predefinito
            console.log("Link con classe .ajax-link trovato:", link.href);
            const url = link.getAttribute("href");

            // Effettua la richiesta AJAX
            fetch(url, {
                headers: {
                    "X-Requested-With": "XMLHttpRequest" // Indica che la richiesta è AJAX
                }
            })
            .then(response => {
                if (!response.ok) throw new Error("Errore nel caricamento");
                return response.text();
            })
            .then(html => {
                document.getElementById("content").innerHTML = html; // Aggiorna il contenitore dinamico
                history.pushState(null, "", url); // Aggiorna la URL senza ricaricare
            })
            .catch(error => console.error("Errore:", error));
        } else{

            // Intercettazione del submit del form
            const form = document.querySelector("form");
            if (form) {
                console.log("Form ajax trovato")
                form.addEventListener("submit", function (e) {
                    e.preventDefault(); // Blocca l'invio normale del form

                    const formData = new FormData(form); // Crea l'oggetto FormData

                    fetch(form.action, {
                        method:"POST"
                    })
                    .then(response => {
                        console.log("1")
                        if (!response.ok) throw new Error("Errore durante l'invio del form");
                        return response.text();
                    })
                    .then(html => {
                        console.log("11")
                        document.getElementById("form-response").innerHTML = JSON.parse(html).message; // Aggiorna il contenitore dinamico con la risposta del server
                        
                    })
                    .catch(error => {
                        console.error("Errore:", error);
                    });
                });
            }
        }

    });

    // Gestione della navigazione con il pulsante "indietro" del browser
    window.addEventListener("popstate", function () {
        fetch(location.href, {
            headers: {
                "X-Requested-With": "XMLHttpRequest"
            }
        })
        .then(response => response.text())
        .then(html => document.getElementById("content").innerHTML = html)
        .catch(error => console.error("Errore:", error));
    })


});

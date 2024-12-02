// document.addEventListener("DOMContentLoaded", function() {
//     // Seleziona tutti i link di navigazione
//     document.querySelectorAll(".ajax-link").forEach(link => {
//         link.addEventListener("click", function(e) {
//             e.preventDefault(); // Evita il ricaricamento della pagina

//             const url = link.getAttribute("href");

//             // Effettua la richiesta AJAX
//             fetch(url, {
//                 headers: {
//                     "X-Requested-With": "XMLHttpRequest" // Indica che la richiesta è AJAX
//                 }
//             })
//             .then(response => {
//                 if (!response.ok) throw new Error("Errore nel caricamento");
//                 return response.text();
//             })
//             .then(html => {
//                 document.getElementById("content").innerHTML = html; // Aggiorna solo il contenitore dinamico
//                 history.pushState(null, "", url); // Aggiorna la URL senza ricaricare
//             })
//             .catch(error => console.error("Errore:", error));
//         });
//     });

//     // Gestione della navigazione con il pulsante "indietro" del browser
//     window.addEventListener("popstate", function() {
//         fetch(location.href, {
//             headers: {
//                 "X-Requested-With": "XMLHttpRequest"
//             }
//         })
//         .then(response => response.text())
//         .then(html => document.getElementById("content").innerHTML = html)
//         .catch(error => console.error("Errore:", error));
//     });
// });
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
            console.log("Il click non è su un .ajax-link");
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
    });
});

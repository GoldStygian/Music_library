function loadExternalScript(src) {
    return new Promise((resolve, reject) => {
        const script = document.createElement("script");
        script.src = src;
        script.async = true;
        script.onload = resolve;
        script.onerror = reject;
        document.head.appendChild(script);
    });
}

function executeInlineScripts(container) {
    const scripts = container.querySelectorAll("script");
    scripts.forEach(script => {
        if (script.src) {
            loadExternalScript(script.src);
        } else {
            try {
                // Esegui il codice inline
                new Function(script.textContent)();
            } catch (error) {
                console.error("Errore nell'esecuzione dello script inline:", error);
            }
        }
    });
}

document.addEventListener("DOMContentLoaded", function () {
    const contentContainer = document.getElementById("content");

    function loadContent(url) {
        fetch(url, { headers: { "X-Requested-With": "XMLHttpRequest" } })
            .then(response => {
                if (!response.ok) throw new Error("Errore nel caricamento");
                return response.text();
            })
            .then(html => {
                const tempDiv = document.createElement("div");
                tempDiv.innerHTML = html;

                // Aggiorna il contenuto
                contentContainer.innerHTML = tempDiv.innerHTML;

                // Esegui gli script trovati
                executeInlineScripts(tempDiv);

                // Aggiorna la cronologia del browser
                history.pushState(null, "", url);
            })
            .catch(error => console.error("Errore:", error));
    }

    document.body.addEventListener("click", function (e) {
        const link = e.target.closest(".ajax-link");
        if (link) {
            e.preventDefault();
            const url = link.getAttribute("href");
            loadContent(url);
        }
    });

    window.addEventListener("popstate", function () {
        loadContent(location.href);
    });
});
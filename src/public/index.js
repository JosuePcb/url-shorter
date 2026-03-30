const API_URL = "http://127.0.0.1:8000";

// ===== Tema =====
const themeToggle = document.getElementById("themeToggle");
const themeIcon = themeToggle.querySelector("i");
themeToggle.addEventListener("click", () => {
  const isLight = document.body.classList.toggle("light-mode");
  themeIcon.setAttribute("data-lucide", isLight ? "moon" : "sun");
  lucide.createIcons();
});


// ===== Acortar URL =====

const generateBtn = document.getElementById("generateBtn");
const resultContainer = document.getElementById("result-container");
const responseInput = document.getElementById("response");
const copyBtn = document.getElementById("copyBtn");

generateBtn.addEventListener("click", shortenUrl);

async function shortenUrl() {
    const url = document.getElementById("request").value.trim();

    if (!url) {
        alert("Por favor, ingresa una URL.");
        return;
    }

    generateBtn.disabled = true;
    generateBtn.textContent = "Acortando...";

    try {
        const response = await fetch(API_URL + "/shorten", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ url: url }),
        });

        if (!response.ok) {
            throw new Error("Error al acortar la URL");
        }

        const data = await response.json();
        responseInput.value = data.short_url;
        resultContainer.style.display = "flex";
        lucide.createIcons();
    } catch (error) {
        alert("Error: " + error.message);
    } finally {
        generateBtn.disabled = false;
        generateBtn.textContent = "Acortar URL";
    }
}


// ===== Copiar al portapapeles =====

copyBtn.addEventListener("click", () => {
    navigator.clipboard.writeText(responseInput.value).then(() => {
        const icon = copyBtn.querySelector("i");
        icon.setAttribute("data-lucide", "check");
        lucide.createIcons();
        setTimeout(() => {
            icon.setAttribute("data-lucide", "copy");
            lucide.createIcons();
        }, 1500);
    });
});
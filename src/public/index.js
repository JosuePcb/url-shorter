

// ===== Tema =====
const themeToggle  = document.getElementById("themeToggle");
const themeIcon    = themeToggle.querySelector("i");
themeToggle.addEventListener("click", () => {
  const isLight = document.body.classList.toggle("light-mode");
  themeIcon.setAttribute("data-lucide", isLight ? "moon" : "sun");
  lucide.createIcons();
});

// Recibir link

var generateBtn = document.getElementById("generateBtn");

async function shortenUrl() {
    var url = document.getElementById("request").value.trim()

    if (!url){
        alert("Por favor, ingresa una URL.");
        return;
    }


}
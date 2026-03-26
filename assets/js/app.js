(function () {
  const progressEl = document.getElementById("progressBar");
  const progressText = document.getElementById("progressText");
  const chapterIndex = Number(document.body.dataset.chapterIndex || 0);
  const chapterTotal = Number(document.body.dataset.chapterTotal || 1);

  if (progressEl && progressText) {
    const pct = Math.round((chapterIndex / chapterTotal) * 100);
    progressEl.style.width = pct + "%";
    progressText.textContent = "Progression du livre: chapitre " + chapterIndex + " / " + chapterTotal;
  }

  const markButtons = document.querySelectorAll("[data-mark-read]");
  markButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
      localStorage.setItem("immovision_last_read", String(chapterIndex));
      btn.textContent = "Chapitre marque comme lu";
      btn.disabled = true;
    });
  });

  const resumeLink = document.getElementById("resumeReading");
  if (resumeLink) {
    const last = Number(localStorage.getItem("immovision_last_read") || 0);
    const map = {
      1: "pages/02-methodologie.html",
      2: "pages/03-collecte.html",
      3: "pages/04-etl.html",
      4: "pages/05-exploration.html",
      5: "pages/06-conclusion.html",
      6: "pages/06-conclusion.html"
    };
    if (last > 0 && map[last]) {
      resumeLink.href = map[last];
      resumeLink.style.display = "inline-block";
    }
  }
})();

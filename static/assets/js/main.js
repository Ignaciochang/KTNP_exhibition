(() => {
  const root = document.documentElement;
  const savedTheme = localStorage.getItem("theme");
  const preferredDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
  root.dataset.theme = savedTheme || (preferredDark ? "dark" : "light");

  document.querySelector("#theme-toggle")?.addEventListener("click", () => {
    root.dataset.theme = root.dataset.theme === "dark" ? "light" : "dark";
    localStorage.setItem("theme", root.dataset.theme);
  });

  const dialog = document.querySelector("#search-dialog");
  const input = document.querySelector("#search-input");
  const results = document.querySelector("#search-results");
  let index = null;

  document.querySelector("#search-open")?.addEventListener("click", async () => {
    dialog.showModal();
    input.focus();
    if (!index) index = await fetch(document.body.dataset.searchIndex).then(r => r.json());
  });

  input?.addEventListener("input", () => {
    const term = input.value.trim().toLocaleLowerCase();
    if (!term) {
      results.innerHTML = "<p class=\"search-empty\">輸入關鍵字開始搜尋</p>";
      return;
    }
    const matches = index.filter(item => `${item.title} ${item.text}`.toLocaleLowerCase().includes(term)).slice(0, 12);
    results.innerHTML = matches.length
      ? matches.map(item => `<a href="${item.url}"><time>${item.date}</time><strong>${escapeHtml(item.title)}</strong></a>`).join("")
      : "<p class=\"search-empty\">找不到符合的文章</p>";
  });

  document.querySelector(".comments-load")?.addEventListener("click", event => {
    const button = event.currentTarget;
    window.disqus_config = function () {
      this.page.url = button.dataset.url;
      this.page.identifier = button.dataset.identifier;
      this.page.title = button.dataset.title;
    };
    const script = document.createElement("script");
    script.src = `https://${button.dataset.shortname}.disqus.com/embed.js`;
    script.dataset.timestamp = String(Date.now());
    script.async = true;
    document.head.appendChild(script);
    button.disabled = true;
    button.textContent = "留言載入中…";
  }, { once: true });

  function escapeHtml(value) {
    const node = document.createElement("span");
    node.textContent = value;
    return node.innerHTML;
  }
})();

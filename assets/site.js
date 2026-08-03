(() => {
  document.body.classList.add("js-ready");
  const config = window.ESSAY_CONFIG || { essayId: "library", theme: "library", glossary: [] };
  const root = document.documentElement;
  const reduced = window.matchMedia?.("(prefers-reduced-motion: reduce)").matches;
  const $ = (selector, scope = document) => scope.querySelector(selector);
  const $$ = (selector, scope = document) => [...scope.querySelectorAll(selector)];

  const savedTheme = localStorage.getItem("faith-theme");
  root.dataset.theme = savedTheme || "dark";
  $("#theme-btn")?.addEventListener("click", () => {
    const next = root.dataset.theme === "light" ? "dark" : "light";
    root.dataset.theme = next;
    localStorage.setItem("faith-theme", next);
  });

  const overlay = $("#menu-overlay");
  const menuButton = $("#menu-btn");
  const closeMenu = () => {
    if (!overlay) return;
    overlay.hidden = true;
    overlay.classList.remove("open");
    menuButton?.setAttribute("aria-expanded", "false");
  };
  menuButton?.addEventListener("click", () => {
    if (!overlay) return;
    overlay.hidden = false;
    overlay.classList.add("open");
    menuButton.setAttribute("aria-expanded", "true");
    $("#menu-close", overlay)?.focus();
  });
  $("#menu-close")?.addEventListener("click", closeMenu);
  overlay?.addEventListener("click", (event) => { if (event.target === overlay) closeMenu(); });
  overlay && $$('a[href^="#"]', overlay).forEach((link) => link.addEventListener("click", closeMenu));

  const bar = $("#topbar");
  const progress = $("#progress");
  const updateScroll = () => {
    const doc = document.documentElement;
    if (progress) progress.style.width = `${(doc.scrollTop / Math.max(1, doc.scrollHeight - doc.clientHeight)) * 100}%`;
    bar?.classList.toggle("on", doc.scrollTop > window.innerHeight * 0.58);
  };
  window.addEventListener("scroll", updateScroll, { passive: true });
  updateScroll();

  const sections = $$(".chapter");
  const chapterLabel = $("#chap-label");
  const rail = $$('[data-chapter-link]');
  if ("IntersectionObserver" in window) {
    const observer = new IntersectionObserver((entries) => entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      rail.forEach((link) => link.classList.toggle("active", link.getAttribute("href") === `#${entry.target.id}`));
      if (chapterLabel) chapterLabel.textContent = entry.target.querySelector("h2")?.textContent || "";
    }), { rootMargin: "-36% 0px -56% 0px" });
    sections.forEach((section) => observer.observe(section));
  }

  const reveal = $$(".reveal, .support-visual, .reading-key");
  if (reduced || !("IntersectionObserver" in window)) reveal.forEach((item) => item.classList.add("in"));
  else {
    const revealObserver = new IntersectionObserver((entries) => entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      entry.target.classList.add("in");
      revealObserver.unobserve(entry.target);
    }), { threshold: 0.05, rootMargin: "0px 0px -4%" });
    reveal.forEach((item) => revealObserver.observe(item));
  }

  const glossary = Object.fromEntries((config.glossary || []).map((entry) => [entry.key, entry]));
  const card = $("#term-card");
  let activeTerm = null;
  const closeCard = () => {
    if (!card) return;
    card.hidden = true;
    activeTerm?.classList.remove("open");
    activeTerm = null;
  };
  const openCard = (term) => {
    const entry = glossary[term.dataset.termKey];
    if (!entry || !card) return;
    activeTerm?.classList.remove("open");
    activeTerm = term;
    term.classList.add("open");
    card.innerHTML = `<div class="tc-tag">${entry.type === "person" ? "Who's Who" : "Working term"}</div><h2>${entry.name || entry.term}</h2><p>${entry.definition}</p>${entry.link ? `<a href="${entry.link}" target="_blank" rel="noopener">Source ↗</a>` : ""}`;
    card.hidden = false;
    if (window.innerWidth > 720) {
      const rect = term.getBoundingClientRect();
      const width = Math.min(360, window.innerWidth - 24);
      card.style.width = `${width}px`;
      card.style.left = `${Math.max(12, Math.min(window.innerWidth - width - 12, rect.left + rect.width / 2 - width / 2))}px`;
      card.style.top = `${Math.max(64, rect.top - card.offsetHeight - 14)}px`;
    }
  };
  $("#essay-content")?.addEventListener("click", (event) => {
    const term = event.target.closest(".term");
    if (term) { event.preventDefault(); activeTerm === term && !card.hidden ? closeCard() : openCard(term); return; }
    if (!event.target.closest(".term-card")) closeCard();
  });
  $$('[data-switcher]').forEach((switcher) => {
    const buttons = $$('[data-value]', switcher);
    const panels = $$('[data-panel]', switcher);
    buttons.forEach((button) => button.addEventListener("click", () => {
      const value = button.dataset.value;
      buttons.forEach((item) => item.setAttribute("aria-selected", String(item === button)));
      panels.forEach((panel) => { panel.hidden = panel.dataset.panel !== value; });
    }));
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") { closeMenu(); closeCard(); }
  });

  const canvas = $("#dust");
  if (canvas && !reduced) {
    const context = canvas.getContext("2d");
    let width = 0; let height = 0;
    const particles = Array.from({ length: 64 }, () => ({ x: Math.random(), y: Math.random(), r: Math.random() * 1.8 + 0.3, speed: Math.random() * 0.00035 + 0.0001 }));
    const resize = () => { width = canvas.width = canvas.offsetWidth * devicePixelRatio; height = canvas.height = canvas.offsetHeight * devicePixelRatio; };
    resize(); window.addEventListener("resize", resize);
    const tick = () => {
      context.clearRect(0, 0, width, height);
      particles.forEach((particle) => { particle.y -= particle.speed; if (particle.y < 0) particle.y = 1; context.beginPath(); context.arc(particle.x * width, particle.y * height, particle.r * devicePixelRatio, 0, Math.PI * 2); context.fillStyle = "rgba(226, 194, 113, .48)"; context.fill(); });
      requestAnimationFrame(tick);
    };
    tick();
  }
})();

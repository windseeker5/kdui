(() => {
  const triggers = () => Array.from(document.querySelectorAll("[data-command-search-trigger]"));

  const dialogFor = (trigger) => {
    const id = trigger?.dataset.commandSearchTarget;
    return id ? document.getElementById(id) : null;
  };

  const openSearch = (trigger) => {
    const dialog = dialogFor(trigger);
    if (!dialog) return;
    if (!dialog.open) dialog.showModal();
    requestAnimationFrame(() => dialog.querySelector("header input")?.focus());
  };

  document.addEventListener("click", (event) => {
    const trigger = event.target.closest("[data-command-search-trigger]");
    if (trigger) openSearch(trigger);
  });

  document.addEventListener("keydown", (event) => {
    const trigger = event.target.closest?.("[data-command-search-trigger]");
    if (trigger && (event.key === "Enter" || event.key === " ")) {
      event.preventDefault();
      openSearch(trigger);
      return;
    }

    if (!(event.metaKey || event.ctrlKey) || event.key.toLowerCase() !== "k") return;
    const primaryTrigger = triggers()[0];
    const dialog = dialogFor(primaryTrigger);
    if (!dialog) return;
    event.preventDefault();
    if (dialog.open) dialog.close();
    else openSearch(primaryTrigger);
  });
})();

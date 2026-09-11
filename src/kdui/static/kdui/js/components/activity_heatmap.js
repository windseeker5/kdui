(() => {
  const selector = "[data-kdui-activity-heatmap]";

  function selectDate(root, button) {
    const date = button.dataset.activityDate;
    const dateLabel = button.dataset.activityDateLabel;
    const details = root.querySelector("[data-activity-details]");
    const heading = root.querySelector("[data-activity-heading]");
    const empty = root.querySelector("[data-activity-empty]");
    const panel = root.querySelector(`[data-activity-panel="${CSS.escape(date)}"]`);

    root.querySelectorAll("[data-activity-date]").forEach((day) => {
      const selected = day === button;
      day.classList.toggle("is-selected", selected);
      day.setAttribute("aria-pressed", String(selected));
    });

    root.querySelectorAll("[data-activity-panel]").forEach((item) => {
      item.hidden = item !== panel;
    });

    details.hidden = false;
    heading.textContent = `Activity for ${dateLabel}`;
    empty.hidden = Boolean(panel);

    root.dispatchEvent(new CustomEvent("kdui:activity-date-change", {
      bubbles: true,
      detail: { date, dateLabel },
    }));
  }

  function resetSelection(root) {
    const selected = root.querySelector("[data-activity-date][aria-pressed=true]");
    const details = root.querySelector("[data-activity-details]");

    root.querySelectorAll("[data-activity-date]").forEach((day) => {
      day.classList.remove("is-selected");
      day.setAttribute("aria-pressed", "false");
    });
    root.querySelectorAll("[data-activity-panel]").forEach((panel) => {
      panel.hidden = true;
    });
    root.querySelector("[data-activity-empty]").hidden = true;
    details.hidden = true;
    selected?.focus();

    root.dispatchEvent(new CustomEvent("kdui:activity-date-change", {
      bubbles: true,
      detail: { date: null, dateLabel: null },
    }));
  }

  function revealSelectedDate(root) {
    const selected = root.querySelector("[data-activity-date][aria-pressed=true]");
    const scroller = root.querySelector(".kdui-activity-heatmap__scroll");
    if (!selected || !scroller || scroller.scrollWidth <= scroller.clientWidth) return;

    const selectedRect = selected.getBoundingClientRect();
    const scrollerRect = scroller.getBoundingClientRect();
    scroller.scrollLeft += selectedRect.left - scrollerRect.left - (scroller.clientWidth / 2);
  }

  document.addEventListener("click", (event) => {
    const reset = event.target.closest("[data-activity-reset]");
    if (reset) {
      const root = reset.closest(selector);
      if (root) resetSelection(root);
      return;
    }

    const button = event.target.closest("[data-activity-date]");
    const root = button?.closest(selector);
    if (button && root) selectDate(root, button);
  });

  document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(selector).forEach(revealSelectedDate);
  });
})();

/*
  KD UI Kanban: two behaviours on a `[data-kanban]` board.

    1. Narrow layout: the tab strip shows one column at a time.
    2. Dragging a card into another column POSTs to the board's data-move-url
       and reloads, so totals and server-made changes are always right. Cards
       also move from their own menu, so dragging is never the only way.

  Without JavaScript the columns just stack one under the other.
*/

(() => {
  const initBoard = (board) => {
    if (board.dataset.kduiKanbanInitialized) return;
    board.dataset.kduiKanbanInitialized = 'true';
    board.setAttribute('data-enhanced', '');

    const columns = [...board.querySelectorAll('[data-kanban-col]')];
    const tabs = [...board.querySelectorAll('[data-kanban-tab]')];

    /* ---- Narrow layout: one column at a time ---- */
    const show = (id) => {
      columns.forEach((column) => column.toggleAttribute('data-active', column.dataset.kanbanCol === id));
      tabs.forEach((tab) => {
        const on = tab.dataset.kanbanTab === id;
        tab.setAttribute('aria-selected', String(on));
        tab.tabIndex = on ? 0 : -1;
      });
    };
    const first = columns.some((c) => c.dataset.kanbanCol === board.dataset.active)
      ? board.dataset.active
      : columns[0]?.dataset.kanbanCol;
    show(first);

    tabs.forEach((tab, index) => {
      tab.addEventListener('click', () => show(tab.dataset.kanbanTab));
      tab.addEventListener('keydown', (event) => {
        const step = { ArrowRight: 1, ArrowLeft: -1 }[event.key];
        if (!step) return;
        event.preventDefault();
        const next = tabs[(index + step + tabs.length) % tabs.length];
        show(next.dataset.kanbanTab);
        next.focus();
        next.scrollIntoView({ inline: 'center', block: 'nearest' });
      });
    });

    /* ---- Dragging a card into another column ---- */
    const moveUrl = board.dataset.moveUrl;
    if (!moveUrl) return;
    let dragged = null;

    const clearOver = () => board.querySelectorAll('[data-over]').forEach((lane) => lane.removeAttribute('data-over'));

    board.addEventListener('dragstart', (event) => {
      const card = event.target.closest('[data-kanban-card]');
      if (!card) return;
      dragged = card;
      card.setAttribute('data-dragging', '');
      event.dataTransfer.effectAllowed = 'move';
      event.dataTransfer.setData('text/plain', card.dataset.id);
    });

    board.addEventListener('dragover', (event) => {
      const lane = event.target.closest('[data-kanban-lane]');
      if (!dragged || !lane) return;
      event.preventDefault();
      clearOver();
      lane.setAttribute('data-over', '');
    });

    board.addEventListener('dragleave', (event) => {
      const lane = event.target.closest('[data-kanban-lane]');
      if (lane && !lane.contains(event.relatedTarget)) lane.removeAttribute('data-over');
    });

    board.addEventListener('drop', (event) => {
      const lane = event.target.closest('[data-kanban-lane]');
      if (!dragged || !lane) return;
      event.preventDefault();
      const target = lane.closest('[data-kanban-col]').dataset.kanbanCol;
      const source = dragged.closest('[data-kanban-col]').dataset.kanbanCol;
      const id = dragged.dataset.id;
      dragged = null;
      clearOver();
      if (target === source) return;
      const body = new URLSearchParams({
        csrf_token: board.dataset.csrf,
        stage: target,
        position: String(lane.querySelectorAll('[data-kanban-card]').length),
      });
      // redirect: 'manual' keeps the server's redirect from being followed here. Following it would
      // show (and use up) the "moved" message on a page nobody sees. The reload below shows it.
      fetch(moveUrl.replace('{id}', encodeURIComponent(id)), {
        method: 'POST',
        body,
        redirect: 'manual',
        credentials: 'same-origin',
      }).finally(() => location.reload());
    });

    board.addEventListener('dragend', () => {
      board.querySelectorAll('[data-dragging]').forEach((card) => card.removeAttribute('data-dragging'));
      clearOver();
      dragged = null;
    });
  };

  const initAll = () => document.querySelectorAll('[data-kanban]').forEach(initBoard);
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', initAll);
  else initAll();
})();

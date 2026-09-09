/*
  KD UI Data Table — toolbar search toggle and filter-tabs indicator.

  Two independent behaviors:
    - On narrow containers, the toolbar's search icon replaces the visible
      tab row with a full-width input.
    - Filter tabs get a sliding "active pill" indicator that animates
      when the active tab changes without a page navigation.

  Uses container queries, so the same component works in side panels and
  full-width contexts without relying on viewport breakpoints.
*/

(() => {
  const TOOLBAR_SELECTOR = '.kdui-table-toolbar';
  const TABS_SELECTOR = '.kdui-filter-tabs';
  const INDICATOR_SELECTOR = '.kdui-filter-tabs__indicator';
  const ACTIVE_TAB_SELECTOR = '.kdui-filter-btn.active';

  /* ---- Toolbar search collapse/expand ---- */
  const initToolbar = (toolbar) => {
    if (toolbar.dataset.kduiTableToolbarInitialized) return;
    toolbar.dataset.kduiTableToolbarInitialized = 'true';

    const btn = toolbar.querySelector('.kdui-table-toolbar__search-btn');
    const input = toolbar.querySelector('.kdui-table-toolbar__search-input');
    if (!btn || !input) return;

    const open = () => {
      toolbar.setAttribute('data-search-open', '');
      btn.setAttribute('aria-expanded', 'true');
      input.focus();
    };

    const close = (clear) => {
      if (clear) input.value = '';
      toolbar.removeAttribute('data-search-open');
      btn.setAttribute('aria-expanded', 'false');
    };

    btn.addEventListener('click', () => {
      if (toolbar.hasAttribute('data-search-open')) {
        close(true);
        btn.focus();
      } else {
        open();
      }
    });

    input.addEventListener('blur', () => {
      if (!input.value) close(false);
    });

    input.addEventListener('keydown', (event) => {
      if (event.key === 'Escape') {
        event.preventDefault();
        close(true);
        btn.focus();
      }
    });
  };

  /* ---- Filter-tabs sliding indicator ---- */
  const positionIndicator = (root, animate = true) => {
    const indicator = root.querySelector(INDICATOR_SELECTOR);
    if (!indicator) return;
    const active = root.querySelector(ACTIVE_TAB_SELECTOR);
    if (!active) {
      indicator.style.opacity = '0';
      indicator.style.width = '0';
      return;
    }
    if (!animate) indicator.style.transition = 'none';
    indicator.style.transform = `translateX(${active.offsetLeft}px)`;
    indicator.style.width = `${active.offsetWidth}px`;
    indicator.classList.add('is-ready');
    if (!animate) {
      void indicator.offsetWidth;
      indicator.style.transition = '';
    }
  };

  const initFilterTabs = (root) => {
    if (root.dataset.kduiFilterTabsInitialized) return;
    root.dataset.kduiFilterTabsInitialized = 'true';

    positionIndicator(root, false);
    window.addEventListener('resize', () => positionIndicator(root, false));

    root.querySelectorAll('.kdui-filter-btn').forEach((tab) => {
      tab.addEventListener('click', (event) => {
        const href = tab.getAttribute('href');
        if (href && href !== '#' && !href.startsWith('javascript:')) return; // real navigation
        event.preventDefault();
        root.querySelectorAll('.kdui-filter-btn').forEach((t) => t.classList.remove('active'));
        tab.classList.add('active');
        positionIndicator(root, true);
      });
    });
  };

  /* ---- Bootstrap on load and DOM mutations ---- */
  const refresh = () => {
    document.querySelectorAll(TOOLBAR_SELECTOR).forEach(initToolbar);
    document.querySelectorAll(TABS_SELECTOR).forEach(initFilterTabs);
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', refresh);
  } else {
    refresh();
  }

  const observer = new MutationObserver(refresh);
  observer.observe(document.body, { childList: true, subtree: true });

  window.kduiDataTable = { refresh };
})();

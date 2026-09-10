/*
  KD UI KPI Card — period dropdown wiring.

  When a KPI card has a period dropdown, clicking a period option updates
  the trigger label and toggles the active state. Real fetched data is not
  included here; a consuming page can attach root.onPeriodChange(period).
*/

(() => {
  const CARD_SELECTOR = '.kdui-kpi-card';
  const PERIOD_SHORT_LABELS = {
    '7d': '7D',
    '30d': '30D',
    '90d': '90D',
    'fy': 'FY',
    'all': 'All',
  };

  const initCard = (card) => {
    if (card.dataset.kduiKpiCardInitialized) return;
    card.dataset.kduiKpiCardInitialized = 'true';

    const menu = card.querySelector('[role="menu"]');
    if (!menu) return;

    const labelEl = card.querySelector('[id$="-period-label"]');

    menu.addEventListener('click', (event) => {
      const item = event.target.closest('[data-period-value]');
      if (!item) return;

      const period = item.dataset.periodValue;
      card.dataset.kpiPeriod = period;

      if (labelEl) {
        labelEl.textContent = PERIOD_SHORT_LABELS[period] || item.textContent.trim();
      }

      menu.querySelectorAll('[role="menuitem"]').forEach((mi) => mi.classList.remove('active'));
      item.classList.add('active');

      if (typeof card.onPeriodChange === 'function') {
        try {
          card.onPeriodChange(period);
        } catch (err) {
          console.error('kpi-card.onPeriodChange failed:', err);
        }
      }
    });
  };

  const refresh = () => {
    document.querySelectorAll(CARD_SELECTOR).forEach(initCard);
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', refresh);
  } else {
    refresh();
  }

  const observer = new MutationObserver(refresh);
  observer.observe(document.body, { childList: true, subtree: true });

  window.kduiKpiCard = { refresh };
})();

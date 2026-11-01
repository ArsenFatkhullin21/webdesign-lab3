// Сбор метрик A/B-теста: клики по CTA, время до клика, глубина скролла, rage clicks.
// События уходят в Microsoft Clarity (если подключён) и копятся в localStorage —
// их можно выгрузить из консоли: copy(JSON.stringify(__ab()))
(function () {
  const variant = (document.currentScript && document.currentScript.dataset.variant) || 'a';
  const t0 = performance.now();
  const KEY = 'ab-metrics';
  const state = { variant, ctaClicks: 0, timeToFirstCtaMs: null, maxScrollPct: 0, rageClicks: 0 };

  const clarity = (...a) => { if (typeof window.clarity === 'function') window.clarity(...a); };
  clarity('set', 'variant', variant);

  const save = () => localStorage.setItem(KEY, JSON.stringify(state));
  window.__ab = () => JSON.parse(localStorage.getItem(KEY) || '{}');

  document.addEventListener('click', e => {
    const cta = e.target.closest('[data-cta]');
    if (!cta) return;
    state.ctaClicks++;
    if (state.timeToFirstCtaMs === null) state.timeToFirstCtaMs = Math.round(performance.now() - t0);
    clarity('event', 'cta_click_' + cta.dataset.cta);
    save();
  });

  let ticking = false;
  addEventListener('scroll', () => {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(() => {
      const d = document.documentElement;
      const pct = Math.round(((scrollY + innerHeight) / d.scrollHeight) * 100);
      if (pct > state.maxScrollPct) { state.maxScrollPct = pct; save(); }
      ticking = false;
    });
  }, { passive: true });

  // rage click: 3+ клика за 700 мс в радиусе 30 px
  let recent = [];
  document.addEventListener('click', e => {
    const now = performance.now();
    recent = recent.filter(c => now - c.t < 700 && Math.hypot(c.x - e.clientX, c.y - e.clientY) < 30);
    recent.push({ t: now, x: e.clientX, y: e.clientY });
    if (recent.length === 3) { state.rageClicks++; clarity('event', 'rage_click'); save(); }
  });
})();

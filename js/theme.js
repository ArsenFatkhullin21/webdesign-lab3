const STORAGE_KEY = 'theme';
const root = document.documentElement;

// Определение начальной темы: сохранённая → системная
function getPreferredTheme() {
  const saved = localStorage.getItem(STORAGE_KEY);
  if (saved === 'dark' || saved === 'light') return saved;
  return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
}

// Применение темы. JS меняет только data-theme — цвета считает CSS.
function applyTheme(theme, persist = true) {
  root.setAttribute('data-theme', theme);
  if (persist) localStorage.setItem(STORAGE_KEY, theme);
  document.querySelectorAll('[data-theme-toggle]').forEach(btn => {
    btn.setAttribute('aria-pressed', String(theme === 'dark'));
  });
}

applyTheme(getPreferredTheme(), false);

document.addEventListener('click', e => {
  const btn = e.target.closest('[data-theme-toggle]');
  if (!btn) return;
  applyTheme(root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark');
});

// Реакция на смену системной темы (только если пользователь не выбирал вручную)
window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
  if (!localStorage.getItem(STORAGE_KEY)) applyTheme(e.matches ? 'dark' : 'light', false);
});

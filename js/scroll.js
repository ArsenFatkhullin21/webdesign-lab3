// 1. Появление элементов при скролле
const observer = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('is-visible');
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.15, rootMargin: '0px 0px -50px 0px' });

document.querySelectorAll('[data-animate]').forEach(el => observer.observe(el));

// 2. Прогресс-бар прокрутки + состояние шапки
const bar = document.querySelector('.progress');
const header = document.querySelector('.header');
let ticking = false;
let max = 0;

// Геометрию читаем редко (при загрузке/ресайзе), а не в каждом кадре скролла —
// так убираем forced reflow (Lighthouse: forced-reflow-insight).
function measure() {
  max = document.documentElement.scrollHeight - window.innerHeight;
}

function update() {
  const ratio = max > 0 ? window.scrollY / max : 0;
  if (bar) bar.style.transform = `scaleX(${Math.min(1, ratio)})`;
  if (header) header.classList.toggle('is-scrolled', window.scrollY > 8);
  ticking = false;
}

window.addEventListener('scroll', () => {
  if (!ticking) { requestAnimationFrame(update); ticking = true; }
}, { passive: true });
window.addEventListener('resize', () => { measure(); update(); });
window.addEventListener('load', () => { measure(); update(); });
requestAnimationFrame(() => { measure(); update(); });

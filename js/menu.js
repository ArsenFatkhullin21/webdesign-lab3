// Мобильное меню: открытие/закрытие по клику, Esc, переход по ссылке
const burger = document.querySelector('.burger');
const menu = document.getElementById('mobile-menu');

if (burger && menu) {
  const setOpen = open => {
    menu.classList.toggle('is-open', open);
    burger.setAttribute('aria-expanded', String(open));
    burger.setAttribute('aria-label', open ? 'Закрыть меню' : 'Открыть меню');
    document.body.classList.toggle('menu-open', open);
  };

  burger.addEventListener('click', () => {
    setOpen(burger.getAttribute('aria-expanded') !== 'true');
  });

  document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && menu.classList.contains('is-open')) {
      setOpen(false);
      burger.focus();
    }
  });

  menu.addEventListener('click', e => {
    if (e.target.closest('a')) setOpen(false);
  });

  // При переходе на десктопную ширину закрываем меню
  window.matchMedia('(min-width: 768px)').addEventListener('change', e => {
    if (e.matches) setOpen(false);
  });
}

// Фиктивная отправка форм (демо)
document.querySelectorAll('form[data-demo-form]').forEach(form => {
  form.addEventListener('submit', e => {
    e.preventDefault();
    const status = form.querySelector('.form-status');
    if (status) status.textContent = 'Спасибо! Заявка отправлена (демо-режим).';
    form.reset();
  });
});

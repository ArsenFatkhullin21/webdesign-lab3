#!/usr/bin/env python3
"""Генератор статических страниц CodeLab.

Шапка, подвал, мобильное меню и хлебные крошки определены один раз и
подставляются в каждую страницу -> сквозные элементы всегда едины.
Запуск:  python3 tools/build.py   (из корня проекта)
"""
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Параметры сборки (Лаб. 3): вариант A/B и ID проекта Microsoft Clarity
VARIANT = os.environ.get("VARIANT", "a").lower()          # a | b
CLARITY_ID = os.environ.get("CLARITY_ID", "").strip()     # пусто -> Clarity не подключается
CSS_FILES = ["tokens", "base", "layout", "components", "pages"]
FONTS_URL = "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Manrope:wght@700;800&display=swap"

NAV = [("index", "index.html", "Главная"), ("courses", "courses.html", "Курсы"),
       ("teachers", "teachers.html", "Преподаватели"), ("blog", "blog.html", "Блог"),
       ("contacts", "contacts.html", "Контакты")]

SVG = 'xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"'
ICONS = {
    "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M4.93 19.07l1.41-1.41M17.66 6.34l1.41-1.41"/>',
    "moon": '<path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>',
    "code": '<path d="m16 18 6-6-6-6M8 6l-6 6 6 6"/>',
    "users": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/>',
    "briefcase": '<rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/>',
    "tg": '<path d="m22 2-7 20-4-9-9-4z"/><path d="M22 2 11 13"/>',
    "gh": '<path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"/>',
    "yt": '<path d="M22.54 6.42a2.78 2.78 0 0 0-1.94-2C18.88 4 12 4 12 4s-6.88 0-8.6.46a2.78 2.78 0 0 0-1.94 2A29 29 0 0 0 1 11.75a29 29 0 0 0 .46 5.33A2.78 2.78 0 0 0 3.4 19c1.72.46 8.6.46 8.6.46s6.88 0 8.6-.46a2.78 2.78 0 0 0 1.94-2 29 29 0 0 0 .46-5.25 29 29 0 0 0-.46-5.33z"/><path d="m9.75 15.02 5.75-3.27-5.75-3.27z"/>',
}


def icon(name, cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<svg {SVG}{c}>{ICONS[name]}</svg>'


# ---------------------------------------------------------------- изображения
PALETTES = [("#2563EB", "#7C3AED"), ("#0EA5E9", "#2563EB"), ("#10B981", "#0EA5E9"),
            ("#F59E0B", "#EF4444"), ("#8B5CF6", "#EC4899"), ("#14B8A6", "#3B82F6")]


def write_cover(name, label, i, w=800, h=450, fs=0.22):
    a, b = PALETTES[i % len(PALETTES)]
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
           f'<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{a}"/>'
           f'<stop offset="1" stop-color="{b}"/></linearGradient></defs>'
           f'<rect width="{w}" height="{h}" fill="url(#g)"/>'
           f'<circle cx="{w*0.82}" cy="{h*0.2}" r="{h*0.35}" fill="#fff" opacity=".12"/>'
           f'<circle cx="{w*0.15}" cy="{h*0.95}" r="{h*0.4}" fill="#fff" opacity=".1"/>'
           f'<text x="{w/2}" y="{h/2+h*0.08}" text-anchor="middle" font-family="monospace" '
           f'font-size="{h*fs}" font-weight="700" fill="#fff">{label}</text></svg>')
    (ROOT / "img/photos" / f"{name}.svg").write_text(svg, encoding="utf-8")


def write_avatar(name, initials, i):
    write_cover(name, initials, i, 400, 400)


def write_logo():
    (ROOT / "img/logo.svg").write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32">'
        '<rect width="32" height="32" rx="8" fill="#2563EB"/>'
        '<path d="m13 11-5 5 5 5M19 11l5 5-5 5" fill="none" stroke="#fff" stroke-width="2.5" '
        'stroke-linecap="round" stroke-linejoin="round"/></svg>', encoding="utf-8")
    (ROOT / "img/favicon.svg").write_text((ROOT / "img/logo.svg").read_text(encoding="utf-8"), encoding="utf-8")


# ---------------------------------------------------------------- шаблон
def header(active):
    links = "".join(
        f'<a class="nav__link{" nav__link--active" if k == active else ""}" href="{h}"'
        f'{" aria-current=\"page\"" if k == active else ""}>{t}</a>' for k, h, t in NAV)
    mlinks = "".join(
        f'<a class="mobile-menu__link{" mobile-menu__link--active" if k == active else ""}" href="{h}"'
        f'{" aria-current=\"page\"" if k == active else ""}>{t}</a>' for k, h, t in NAV)
    return f'''<div class="progress" role="presentation"></div>
<a class="skip-link" href="#main">Перейти к содержимому</a>
<header class="header">
  <div class="container header__inner">
    <a class="logo" href="index.html" aria-label="CodeLab — на главную"><img src="img/logo.svg" alt="" width="32" height="32">CodeLab</a>
    <nav class="nav" aria-label="Основная навигация">{links}</nav>
    <div class="header__actions">
      <button class="theme-toggle" type="button" data-theme-toggle aria-label="Переключить тему" aria-pressed="false">
        {icon("sun", "theme-toggle__icon theme-toggle__icon--sun")}
        {icon("moon", "theme-toggle__icon theme-toggle__icon--moon")}
      </button>
      <a class="btn btn--primary btn--sm header__login" href="contacts.html#enroll">Войти</a>
      <button class="burger" type="button" aria-expanded="false" aria-controls="mobile-menu" aria-label="Открыть меню"><span class="burger__lines"></span></button>
    </div>
  </div>
</header>
<nav class="mobile-menu" id="mobile-menu" aria-label="Мобильная навигация">{mlinks}
  <a class="btn btn--primary btn--lg" href="contacts.html#enroll">Войти</a>
</nav>'''


FOOTER = f'''<footer class="footer">
  <div class="container">
    <div class="footer__grid">
      <div class="footer__brand">
        <a class="logo" href="index.html"><img src="img/logo.svg" alt="" width="32" height="32">CodeLab</a>
        <p class="form-note" style="margin-top:12px;max-width:320px">Онлайн-школа программирования: практика, наставники и помощь с трудоустройством.</p>
        <div class="socials">
          <a href="https://t.me/" aria-label="Telegram">{icon("tg")}</a>
          <a href="https://github.com/" aria-label="GitHub">{icon("gh")}</a>
          <a href="https://youtube.com/" aria-label="YouTube">{icon("yt")}</a>
        </div>
      </div>
      <div><h2 class="footer__title">Обучение</h2><ul class="footer__list">
        <li><a href="courses.html">Все курсы</a></li><li><a href="course.html">Frontend-разработчик</a></li><li><a href="teachers.html">Преподаватели</a></li></ul></div>
      <div><h2 class="footer__title">Ресурсы</h2><ul class="footer__list">
        <li><a href="blog.html">Блог</a></li><li><a href="post.html">Как начать в IT</a></li></ul></div>
      <div><h2 class="footer__title">Контакты</h2><ul class="footer__list">
        <li><a href="contacts.html">Написать нам</a></li><li><a href="mailto:hello@codelab.example">hello@codelab.example</a></li></ul></div>
    </div>
    <div class="footer__bottom"><p>© 2026 CodeLab. Учебный проект, лабораторная работа №2.</p><p>Сделано с CSS Grid и любовью к доступности</p></div>
  </div>
</footer>'''


def crumbs(items):
    """items: [(text, href|None)], последний — текущая страница."""
    if not items:
        return ""
    li = ""
    for i, (t, h) in enumerate(items):
        li += (f'<li><a href="{h}">{t}</a></li>' if h else f'<li><span aria-current="page">{t}</span></li>')
    return f'<nav class="breadcrumbs" aria-label="Хлебные крошки"><ol>{li}</ol></nav>'


CLARITY_SNIPPET = """  <script>
    (function(c,l,a,r,i,t,y){c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
    t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
    y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
    })(window, document, "clarity", "script", "%s");
  </script>
"""


def page(fname, title, desc, active, body, preload=""):
    CLARITY = CLARITY_SNIPPET % CLARITY_ID if CLARITY_ID else ""
    PRELOAD = preload
    html = f'''<!DOCTYPE html>
<html lang="ru" data-theme="light">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} — CodeLab</title>
  <meta name="description" content="{desc}">
  <meta name="color-scheme" content="light dark">
  <link rel="icon" href="img/favicon.svg" type="image/svg+xml">
  <script>
    /* Ранняя установка темы — без «вспышки» при загрузке */
    (function () {{
      var s = localStorage.getItem('theme');
      var t = (s === 'dark' || s === 'light') ? s : (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
      document.documentElement.setAttribute('data-theme', t);
    }})();
  </script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  {PRELOAD}<link rel="stylesheet" href="css/bundle.css">
  <link rel="stylesheet" href="{FONTS_URL}" media="print" onload="this.media='all'">
  <noscript><link rel="stylesheet" href="{FONTS_URL}"></noscript>
{CLARITY}</head>
<body>
{header(active)}
<main id="main">
{body}
</main>
{FOOTER}
<script src="js/theme.js" defer></script>
<script src="js/menu.js" defer></script>
<script src="js/scroll.js" defer></script>
<script src="js/ab.js" defer data-variant="{VARIANT}"></script>
</body>
</html>
'''
    (ROOT / fname).write_text(html, encoding="utf-8")


def hero(title, lead, bc):
    return f'''<section class="page-hero"><div class="container">{crumbs(bc)}<h1>{title}</h1><p>{lead}</p></div></section>'''


# ---------------------------------------------------------------- данные
COURSES = [
    ("frontend", "Frontend-разработчик", "HTML, CSS, JavaScript и React с нуля до первого оффера.", "6 месяцев", "89 000 ₽", "FE", "Веб"),
    ("python", "Python-разработчик", "Бэкенд на Python: Django, базы данных, REST API.", "7 месяцев", "95 000 ₽", "PY", "Бэкенд"),
    ("design", "UI/UX-дизайн", "Figma, дизайн-системы, исследования и прототипы.", "4 месяца", "69 000 ₽", "UX", "Дизайн"),
    ("data", "Аналитик данных", "SQL, Python, Pandas и визуализация данных.", "5 месяцев", "79 000 ₽", "SQL", "Данные"),
    ("mobile", "Мобильная разработка", "Kotlin и Android: от интерфейса до публикации.", "6 месяцев", "92 000 ₽", "KT", "Мобайл"),
    ("devops", "DevOps-инженер", "Linux, Docker, CI/CD и облачная инфраструктура.", "5 месяцев", "85 000 ₽", "OPS", "Инфра"),
]
TEACHERS = [
    ("Анна Соколова", "Frontend, 8 лет опыта", "Ведёт курс по JavaScript. Ранее — Яндекс.", "АС"),
    ("Дмитрий Орлов", "Python / Backend", "Архитектор высоконагруженных сервисов.", "ДО"),
    ("Мария Левина", "UI/UX-дизайнер", "Создала дизайн-системы для трёх продуктов.", "МЛ"),
    ("Илья Громов", "Аналитик данных", "Строит аналитику для e-commerce.", "ИГ"),
    ("Елена Ким", "Android-разработчик", "Автор приложений с 1 млн скачиваний.", "ЕК"),
    ("Артём Белов", "DevOps-инженер", "Переводит команды на CI/CD и Kubernetes.", "АБ"),
]
POSTS = [
    ("post", "Как начать карьеру в IT: пошаговый план", "Разбираем путь новичка: от выбора направления до первого собеседования.", "12 октября 2026", "6 мин"),
    ("post", "5 ошибок при вёрстке тёмной темы", "Контраст, тени, изображения — на что смотреть, чтобы тема не «ломалась».", "28 сентября 2026", "5 мин"),
    ("post", "Дизайн-токены: зачем они нужны", "Семантические токены позволяют менять тему и бренд в одном месте.", "15 сентября 2026", "7 мин"),
    ("post", "Доступность: минимум, который стоит знать", "Контраст, фокус, семантика и alt-тексты — основа WCAG 2.1 AA.", "2 сентября 2026", "4 мин"),
]


def write_bundle():
    """Склейка CSS в один файл: 5 блокирующих запросов -> 1."""
    parts = [(ROOT / "css" / f"{n}.css").read_text(encoding="utf-8") for n in CSS_FILES]
    (ROOT / "css" / "bundle.css").write_text("\n".join(parts), encoding="utf-8")


def build():
    write_bundle()
    write_logo()
    for i, c in enumerate(COURSES):
        write_cover(f"course-{c[0]}", c[5], i)
    for i, t in enumerate(TEACHERS):
        write_avatar(f"teacher-{i+1}", t[3], i)
    for i in range(len(POSTS)):
        write_cover(f"post-{i+1}", "{ }", i + 2)
    write_cover("hero", "&lt;/&gt; CodeLab", 0, 800, 600, 0.13)

    # ---- index
    feats = [("code", "Практика с первого дня", "Каждое занятие — задачи и ревью кода от наставников."),
             ("users", "Живое комьюнити", "Чаты, командные проекты и хакатоны вместе с однокурсниками."),
             ("briefcase", "Помощь с карьерой", "Резюме, моки собеседований и подборка вакансий партнёров.")]
    feat_html = "".join(
        f'<article class="feature" data-animate style="--animate-delay: {100*(i+1)}ms"><div class="feature__icon">{icon(ic)}</div>'
        f'<h3>{t}</h3><p>{d}</p></article>' for i, (ic, t, d) in enumerate(feats))
    reviews = [("Максим К.", "Frontend, выпуск 2025", "За полгода перешёл из поддержки в разработку. Ревью кода — лучшее, что было на курсе.", 1),
               ("Ольга Р.", "UI/UX, выпуск 2026", "Дизайн-система из курса теперь живёт в моём рабочем проекте. Рекомендую!", 3),
               ("Сергей Т.", "Python, выпуск 2025", "Сильная практика и отзывчивые преподаватели. Оффер получил через 2 месяца.", 5)]
    rev_html = "".join(
        f'<figure class="quote" data-animate style="--animate-delay: {100*(i+1)}ms"><blockquote style="margin:0;padding:0;background:none;border:0"><p>«{q}»</p></blockquote>'
        f'<footer><img src="img/photos/teacher-{n}.svg" alt="" width="48" height="48" loading="lazy"><span><strong>{a}</strong>{r}</span></footer></figure>'
        for i, (a, r, q, n) in enumerate(reviews))
    course_cards = "".join(card_course(c, i) for i, c in enumerate(COURSES[:3]))
    hero_cta = ('<a class="btn btn--success btn--lg" href="courses.html" data-cta="hero">Начать бесплатно</a>' if VARIANT == "b"
                else '<a class="btn btn--primary btn--lg" href="courses.html" data-cta="hero">Выбрать курс</a>')
    page("index.html", "Онлайн-школа программирования", "CodeLab — онлайн-школа программирования: курсы, наставники и помощь с трудоустройством.", "index", f'''
<!-- Первый экран без анимации появления: иначе LCP (h1) ждёт JS и transition -->
<section class="hero"><div class="container hero__grid">
  <div>
    <p class="hero__eyebrow">Онлайн-школа IT-профессий</p>
    <h1>Научись программировать и найди работу мечты</h1>
    <p class="hero__lead">Практические курсы с наставниками, реальными проектами и поддержкой на пути к первому офферу.</p>
    <div class="hero__actions">
      {hero_cta}
      <a class="btn btn--secondary btn--lg" href="contacts.html">Бесплатная консультация</a>
    </div>
    <dl class="hero__stats">
      <div><dt>5 000+</dt><dd>выпускников</dd></div><div><dt>87%</dt><dd>находят работу</dd></div><div><dt>4.9</dt><dd>средняя оценка</dd></div>
    </dl>
  </div>
  <img class="hero__image" src="img/photos/hero.svg" alt="Иллюстрация: код на экране" width="800" height="600" loading="eager" fetchpriority="high" decoding="async">
</div></section>

<section class="section section--alt" id="services"><div class="container">
  <div class="section__head" data-animate="fade"><h2>Почему CodeLab</h2><p>Мы строим обучение вокруг практики и обратной связи.</p></div>
  <div class="grid grid--3">{feat_html}</div>
</div></section>

<section class="section"><div class="container">
  <div class="section__head" data-animate="fade"><h2>Популярные курсы</h2><p>Выберите направление и начните уже на этой неделе.</p></div>
  <div class="grid grid--3">{course_cards}</div>
  <p style="margin-top:32px;text-align:center"><a class="btn btn--ghost" href="courses.html">Смотреть все курсы →</a></p>
</div></section>

<section class="section section--alt"><div class="container">
  <div class="section__head" data-animate="fade"><h2>Отзывы выпускников</h2></div>
  <div class="grid grid--3">{rev_html}</div>
</div></section>

<section class="section"><div class="container"><div class="cta" data-animate>
  <h2>Готовы начать?</h2><p>Оставьте заявку — поможем выбрать курс и ответим на все вопросы.</p>
  <a class="btn btn--lg" href="contacts.html#enroll" data-cta="footer">Записаться на консультацию</a>
</div></div></section>''', preload='<link rel="preload" as="image" href="img/photos/hero.svg" fetchpriority="high">\n  ')

    # ---- courses
    cards = "".join(card_course(c, i, True, 2) for i, c in enumerate(COURSES))
    page("courses.html", "Курсы", "Каталог курсов CodeLab: frontend, Python, дизайн, аналитика, мобильная разработка и DevOps.", "courses",
         hero("Курсы", "Выберите направление — от веб-разработки до аналитики данных.", [("Главная", "index.html"), ("Курсы", None)]) +
         f'''<div class="container page-body"><div class="grid grid--3">{cards}</div>
<nav class="pagination" aria-label="Пагинация">
  <a class="pagination__link" href="#" aria-label="Предыдущая страница">←</a>
  <a class="pagination__link" href="courses.html" aria-current="page">1</a>
  <a class="pagination__link" href="#">2</a><a class="pagination__link" href="#">3</a>
  <a class="pagination__link" href="#" aria-label="Следующая страница">→</a>
</nav></div>''')

    # ---- course
    topics = ["Основы HTML и семантическая вёрстка", "CSS: Flexbox, Grid и адаптивность", "JavaScript: язык и работа с DOM",
              "Асинхронность, fetch и работа с API", "React: компоненты, состояние, роутинг", "Git, сборка и деплой проекта",
              "Доступность и производительность", "Дипломный проект и подготовка к собеседованиям"]
    syl = "".join(f"<li>{t}</li>" for t in topics)
    page("course.html", "Frontend-разработчик", "Курс «Frontend-разработчик»: HTML, CSS, JavaScript и React за 6 месяцев.", "courses",
         f'''<div class="container page-body">
{crumbs([("Главная", "index.html"), ("Курсы", "courses.html"), ("Frontend-разработчик", None)])}
<div class="with-sidebar">
  <article>
    <span class="badge">Веб</span>
    <h1 style="font-size:var(--fs-4xl)">Frontend-разработчик</h1>
    <div class="course-meta"><span>Длительность: <strong>6 месяцев</strong></span><span>Уровень: <strong>с нуля</strong></span><span>Формат: <strong>онлайн</strong></span></div>
    <img class="card__image" style="border-radius:16px;margin-bottom:32px" src="img/photos/course-frontend.svg" alt="Обложка курса Frontend-разработчик" width="800" height="450">
    <h2>О курсе</h2>
    <p>Вы освоите стек современного фронтенда: научитесь вёрстке, программированию на JavaScript и созданию интерфейсов на React. Курс построен вокруг реальных проектов — к выпуску у вас будет портфолио из пяти работ.</p>
    <h2>Программа</h2>
    <ol class="syllabus">{syl}</ol>
  </article>
  <aside class="sidebar" id="enroll" aria-label="Запись на курс">
    <p class="sidebar__price">89 000 ₽</p><p class="form-note">или от 7 400 ₽/мес в рассрочку</p>
    <ul><li>✓ Доступ к материалам навсегда</li><li>✓ Ревью кода от наставников</li><li>✓ Помощь с резюме</li></ul>
    <form data-demo-form>
      <div class="field"><label class="label" for="c-name">Имя</label><input class="input" id="c-name" name="name" placeholder="Ваше имя" required autocomplete="name"></div>
      <div class="field"><label class="label" for="c-email">Email</label><input class="input" id="c-email" type="email" name="email" placeholder="you@example.com" required autocomplete="email"></div>
      <button class="btn btn--primary btn--block" type="submit">Записаться</button>
      <p class="form-status" role="status"></p>
    </form>
  </aside>
</div></div>''')

    # ---- teachers
    tcards = "".join(
        f'''<article class="card teacher" data-animate style="--animate-delay:{(i%3)*100}ms"><img class="card__image card__image--square" src="img/photos/teacher-{i+1}.svg" alt="Фото: {n}" width="400" height="400" loading="lazy">
<div class="card__body"><h2 class="card__title">{n}</h2><p class="teacher__role">{r}</p><p class="card__text">{d}</p></div></article>''' for i, (n, r, d, _) in enumerate(TEACHERS))
    page("teachers.html", "Преподаватели", "Преподаватели CodeLab — практикующие специалисты из ведущих IT-компаний.", "teachers",
         hero("Преподаватели", "Нас учат практики, которые работают в индустрии каждый день.", [("Главная", "index.html"), ("Преподаватели", None)]) +
         f'<div class="container page-body"><div class="grid grid--3">{tcards}</div></div>')

    # ---- blog
    plist = "".join(
        f'''<article class="card" data-animate><img class="card__image" src="img/photos/post-{i+1}.svg" alt="" width="800" height="450" loading="lazy">
<div class="card__body"><h2 class="card__title"><a href="post.html">{t}</a></h2><p class="card__text">{d}</p>
<div class="card__meta"><span>{dt}</span><span>{rt} чтения</span></div></div></article>''' for i, (_, t, d, dt, rt) in enumerate(POSTS))
    page("blog.html", "Блог", "Блог CodeLab: статьи о карьере в IT, вёрстке, дизайне и доступности.", "blog",
         hero("Блог", "Полезные материалы о разработке, дизайне и карьере.", [("Главная", "index.html"), ("Блог", None)]) +
         f'<div class="container page-body"><div class="post-list">{plist}</div></div>')

    # ---- post
    page("post.html", "Как начать карьеру в IT", "Пошаговый план для новичка: выбор направления, обучение, портфолио и первое собеседование.", "blog",
         f'''<div class="container page-body">
{crumbs([("Главная", "index.html"), ("Блог", "blog.html"), ("Как начать карьеру в IT", None)])}
<div class="with-sidebar">
<article class="article">
  <h1 style="font-size:var(--fs-4xl)">Как начать карьеру в IT: пошаговый план</h1>
  <p class="article__meta">12 октября 2026 · 6 мин чтения · Анна Соколова</p>
  <img class="article__cover" src="img/photos/post-1.svg" alt="Обложка статьи" width="800" height="450">
  <p>Войти в IT без опыта реально, но нужен чёткий план. Ниже — путь, который прошли сотни наших выпускников.</p>
  <h2 id="direction">1. Выберите направление</h2>
  <p>Разработка, дизайн, аналитика, тестирование, DevOps — у каждого свои задачи и порог входа. Попробуйте по паре бесплатных уроков в каждом направлении и посмотрите, что увлекает.</p>
  <blockquote><p>Лучшее направление — то, в котором вы готовы регулярно разбираться в сложном.</p></blockquote>
  <h2 id="learn">2. Учитесь на практике</h2>
  <p>Теория без практики забывается за неделю. Делайте небольшие проекты, публикуйте код и просите обратную связь.</p>
<pre><code>git init
git add .
git commit -m "Первый проект"</code></pre>
  <h2 id="portfolio">3. Соберите портфолио</h2>
  <p>Три–пять законченных проектов лучше десяти недоделанных. Опишите задачу, решение и технологии в README каждого репозитория.</p>
  <h2 id="interview">4. Готовьтесь к собеседованиям</h2>
  <p>Тренируйте рассказ о себе, решайте типовые задачи и участвуйте в пробных интервью. Отказы — часть процесса: каждый даёт материал для улучшения.</p>
</article>
<aside class="toc sidebar" aria-labelledby="toc-title"><h2 id="toc-title">Оглавление</h2>
<ol><li><a href="#direction">Выберите направление</a></li><li><a href="#learn">Учитесь на практике</a></li><li><a href="#portfolio">Соберите портфолио</a></li><li><a href="#interview">Готовьтесь к собеседованиям</a></li></ol></aside>
</div></div>''')

    # ---- contacts
    page("contacts.html", "Контакты", "Свяжитесь с CodeLab: форма обратной связи, адрес, телефон и email.", "contacts",
         hero("Контакты", "Напишите нам — ответим в течение рабочего дня.", [("Главная", "index.html"), ("Контакты", None)]) +
         f'''<div class="container page-body"><div class="contacts-grid">
<section class="panel" id="enroll" aria-labelledby="form-title"><h2 id="form-title" style="font-size:var(--fs-2xl)">Оставить заявку</h2>
<form data-demo-form>
  <div class="field"><label class="label" for="name">Имя</label><input class="input" id="name" name="name" placeholder="Ваше имя" required autocomplete="name"></div>
  <div class="field"><label class="label" for="email">Email</label><input class="input" id="email" type="email" name="email" placeholder="you@example.com" required autocomplete="email"></div>
  <div class="field"><label class="label" for="topic">Тема</label><select class="select" id="topic" name="topic"><option>Выбор курса</option><option>Оплата и рассрочка</option><option>Сотрудничество</option></select></div>
  <div class="field"><label class="label" for="msg">Сообщение</label><textarea class="textarea" id="msg" name="msg" placeholder="Чем мы можем помочь?" required></textarea></div>
  <label class="checkbox field"><input type="checkbox" required><span>Согласен на обработку персональных данных</span></label>
  <button class="btn btn--primary" type="submit">Отправить</button>
  <p class="form-status form-status--ok" role="status"></p>
</form></section>
<section aria-labelledby="info-title"><h2 id="info-title" style="font-size:var(--fs-2xl)">Как нас найти</h2>
<ul class="contact-list">
  <li><strong>Адрес</strong>Москва, ул. Программистов, 42, офис 7</li>
  <li><strong>Телефон</strong><a href="tel:+78005550142">8 (800) 555-01-42</a></li>
  <li><strong>Email</strong><a href="mailto:hello@codelab.example">hello@codelab.example</a></li>
  <li><strong>Часы работы</strong>Пн–Пт, 10:00–19:00</li></ul>
<img class="map" src="img/photos/map.svg" alt="Схема проезда к офису CodeLab" width="800" height="450" loading="lazy"></section>
</div></div>''')
    write_map()


def write_map():
    lines = "".join(f'<path d="M{x} 0V450" stroke="#fff" stroke-width="10" opacity=".7"/>' for x in (150, 380, 620)) + \
            "".join(f'<path d="M0 {y}H800" stroke="#fff" stroke-width="10" opacity=".7"/>' for y in (110, 260, 380))
    (ROOT / "img/photos/map.svg").write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="800" height="450" viewBox="0 0 800 450"><rect width="800" height="450" fill="#CBD5E1"/>'
        f'<rect x="420" y="130" width="180" height="110" fill="#86EFAC"/>{lines}'
        f'<path d="M380 260a28 28 0 1 1 .01 0L380 300z" transform="translate(0 -60)" fill="#EF4444"/><circle cx="380" cy="172" r="9" fill="#fff"/></svg>',
        encoding="utf-8")


def card_course(c, i, animate=False, level=3):
    slug, title, desc, dur, price, _, tag = c
    href = "course.html"
    anim = f' data-animate style="--animate-delay:{(i%3)*100}ms"' if animate else ""
    return f'''<article class="card"{anim}><img class="card__image" src="img/photos/course-{slug}.svg" alt="" width="800" height="450" loading="lazy">
<div class="card__body"><span class="badge">{tag}</span><h{level} class="card__title"><a href="{href}">{title}</a></h{level}><p class="card__text">{desc}</p>
<div class="card__meta"><span>{dur}</span><span class="card__price">{price}</span></div></div></article>'''


if __name__ == "__main__":
    build()
    print("OK")

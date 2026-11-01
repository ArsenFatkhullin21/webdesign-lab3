# CodeLab — Лабораторная работа №3: юзабилити, Core Web Vitals, A/B

Сайт из лаб. 2, оптимизированный по Core Web Vitals и подготовленный к A/B-тесту и сбору данных (Clarity).

- Вариант A: https://arsenfatkhullin21.github.io/webdesign-lab3/
- Вариант B: https://arsenfatkhullin21.github.io/webdesign-lab3/b/
- Как провести исследование с участниками: [research/README.md](research/README.md)

```
tools/build.py        генератор страниц (VARIANT=a|b, CLARITY_ID=...)
tools/make_dist.py    собирает dist/a и dist/b для двух сайтов на Netlify
tools/lighthouse.sh   запуск Lighthouse (mobile + desktop)
tools/analyze.py      SUS, протокол, A/B: среднее, SD, t-тест Уэлча
js/ab.js              клики по CTA, время до клика, скролл, rage clicks
research/             шаблоны: протокол, SUS, результаты A/B, вопросы SUS
reports/before|after  локальные отчёты Lighthouse (первая итерация)
report/               источник отчёта, скриншоты, замеры PageSpeed/Lighthouse по опубликованным сайтам
.github/workflows/pages.yml   публикация A (корень) и B (/b/), CLARITY_ID из переменной репозитория
```

## Порядок работы

1. Публикация автоматическая (GitHub Actions). Clarity: `gh variable set CLARITY_ID --body <id>` и перезапуск workflow.
2. Локально: `python3 tools/make_dist.py` собирает `dist/a` и `dist/b`.
3. Провести тесты, заполнить `research/*.csv`, запустить `tools/analyze.py`.
4. Перенести цифры и скриншоты в `report/ОТЧЁТ.md`.

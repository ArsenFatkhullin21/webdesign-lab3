# CodeLab — Лабораторная работа №3: юзабилити, Core Web Vitals, A/B

Сайт из лаб. 2, оптимизированный по Lighthouse и подготовленный к A/B-тесту и сбору данных (Clarity).

```
tools/build.py        генератор страниц (VARIANT=a|b, CLARITY_ID=...)
tools/make_dist.py    собирает dist/a и dist/b для двух сайтов на Netlify
tools/lighthouse.sh   запуск Lighthouse (mobile + desktop)
tools/analyze.py      SUS, протокол, A/B: среднее, SD, t-тест Уэлча
js/ab.js              клики по CTA, время до клика, скролл, rage clicks
research/             шаблоны: протокол, SUS, результаты A/B, вопросы SUS
reports/before|after  отчёты Lighthouse (json + html) до и после оптимизации
report/ОТЧЁТ.md       отчёт (поля [ЗАПОЛНИТЬ] — данные от живых участников)
```

## Порядок работы

1. `CLARITY_ID=<id> python3 tools/make_dist.py` — собрать два варианта с Clarity.
2. Залить `dist/a` и `dist/b` на Netlify Drop → две ссылки; снять PSI и WebPageTest.
3. Провести тесты, заполнить `research/*.csv`, запустить `tools/analyze.py`.
4. Перенести цифры и скриншоты в `report/ОТЧЁТ.md`.

# Как провести исследование (лабораторная №3)

Всё, что можно было сделать без участников, уже сделано: сайты опубликованы, метрики сняты, отчёт собран.
Осталось провести исследование с живыми людьми. Таблицы и расчёты в отчёте появятся сами, как только CSV-файлы ниже заполнены.

## 0. Ссылки

- Вариант A (контроль): https://arsenfatkhullin21.github.io/webdesign-lab3/
- Вариант B: https://arsenfatkhullin21.github.io/webdesign-lab3/b/

## 1. Подключить Microsoft Clarity (10 минут)

1. clarity.microsoft.com → войти → **New project**: имя `WebDesign-Lab3`, URL `https://arsenfatkhullin21.github.io/webdesign-lab3/`, тип **HTML**.
2. Скопировать **Project ID** (10 символов, например `abcd123xyz`). Он виден в Settings → Overview.
3. В терминале (папка `lab3_webdesign`):
   ```bash
   gh variable set CLARITY_ID -R ArsenFatkhullin21/webdesign-lab3 --body abcd123xyz
   gh workflow run "Deploy A/B" -R ArsenFatkhullin21/webdesign-lab3
   ```
   Через 1–2 минуты код Clarity окажется на обоих вариантах. Оба варианта пишут в один проект, а вариант передаётся тегом `variant` (`a`/`b`), по нему фильтруются записи.
4. Проверка: открыть сайт, через 2–3 минуты в Clarity → Dashboard должна появиться сессия.

## 2. Юзабилити-тест (5 участников, Google Meet)

- Сценарий ведущего: `сценарий_модератора.md`. Читайте текст дословно и **не подсказывайте**.
- Профиль участника → `participants.csv`.
- Каждую задачу → строка в `protocol.csv`: `participant,scenario,time_s,success,errors,comments` (success: `да`/`нет`).
- После сессии участник заполняет форму SUS (текст формы — в `google_forms.md`). Ответы (числа 1–5) → `sus.csv`.

## 3. A/B-тест (20+ участников, по 10 на вариант)

- Текст приглашения: `приглашение_участникам.md`. Вариант назначается по дню рождения: чётный → A, нечётный → B.
- После задания участник открывает консоль браузера (F12 → Console), вводит `copy(JSON.stringify(__ab()))` и вставляет результат в форму. Если это сложно, те же данные есть в Clarity.
- Результаты → `ab_results.csv`: `variant` (A/B), `cta_clicks`, `time_to_cta_s`, `max_scroll_pct`, `rage_clicks`, `ease_1_5` (вопрос «Насколько легко…»), `sus` (балл SUS, если собирали).

## 4. Скриншоты Clarity → `../report/screens/clarity/`

Ожидаемые имена файлов (отчёт подставит их автоматически, вместо отсутствующих останется жёлтая рамка):

| Файл | Что на скриншоте |
|---|---|
| `dashboard.png` | Dashboard: сессии, Dead clicks, Rage clicks, Quick backs, Scroll depth |
| `heatmap-click-a.png` | Heatmaps → Click, главная, фильтр variant = a |
| `heatmap-click-b.png` | то же для варианта b |
| `heatmap-scroll.png` | Heatmaps → Scroll, главная |
| `recording.png` | Recordings: кадр сессии, где участник «застрял» |

## 5. Проблемы и выводы

- Найденные проблемы (минимум 5 из тестов и Clarity) дописать строками в `problems.csv`. Пять проблем из замеров производительности уже внесены.
- Наблюдения своими словами дописать в `observations.md`, этот файл вставляется в отчёт как есть.

## 6. Пересобрать отчёт

```bash
python3 ../_report_tools/build_report.py lab3_webdesign/report/ОТЧЁТ.md   # из папки «веб-дизайн»
```

Скрипт посчитает SUS, проценты успеха, средние, стандартные отклонения и t-тест Уэлча. Затем он перегенерирует DOCX и PDF в папке `Отчёты/`. Сколько жёлтых пометок осталось, скрипт напечатает в конце.

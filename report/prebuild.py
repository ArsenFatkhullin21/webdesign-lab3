#!/usr/bin/env python3
"""Генерирует таблицы отчёта (report/_gen/*.md) из замеров (report/data.json)
и данных исследования (research/*.csv). Пустой CSV -> жёлтая пометка [[ЗАПОЛНИТЬ]]."""
import csv, json, re, statistics as st, sys
from pathlib import Path

R = Path(__file__).resolve().parent
RES = R.parent / 'research'
sys.path.insert(0, str(R.parent / 'tools'))
from analyze import sus_score, sus_label, welch  # noqa: E402

G = R / '_gen'; G.mkdir(exist_ok=True)
d = json.loads((R / 'data.json').read_text(encoding='utf-8'))
w = lambda name, text: (G / name).write_text(text.rstrip() + '\n', encoding='utf-8')
read = lambda f: list(csv.DictReader(open(RES / f, encoding='utf-8'))) if (RES / f).exists() else []
fmt = lambda v: re.sub(r'(\d)\s*s$', r'\1 с', re.sub(r'(\d)\s*ms$', r'\1 мс', v)) if isinstance(v, str) else v
PAGES = {'index': 'Главная', 'courses': 'Курсы', 'contacts': 'Контакты'}
num = lambda x: f'{x:.1f}'.replace('.', ',')

# ---------- PageSpeed Insights
rows = ['| Этап | Устройство | Performance | FCP | LCP | TBT | CLS | Speed Index |', '|---|---|---|---|---|---|---|---|']
stage_name = {'before': 'До (сайт лаб. 2)', 'iter1': 'Итерация 1 (лаб. 3)', 'after': 'После (лаб. 3)'}
for x in d.get('psiIter1', []) + d['psi']:
    rows.append(f'| {stage_name[x["stage"]]} | {"Mobile" if x["formFactor"] == "mobile" else "Desktop"} | **{x["performance"]}** | {x["fcp"]} | **{x["lcp"]}** | {x["tbt"]} | {x["cls"]} | {x["si"]} |')
w('psi.md', '\n'.join(rows))

# ---------- Lighthouse до/после
lh = {(x['stage'], x['page'], x['device']): x for x in d['lighthouse']}
rows = ['| Страница | Устройство | Этап | Perf. | Access. | Best Pr. | SEO | FCP | LCP | CLS | TBT |', '|---|---|---|---|---|---|---|---|---|---|---|']
for pg, pn in PAGES.items():
    for dev in ('mobile', 'desktop'):
        for stg, sn in (('before', 'до'), ('after', 'после')):
            x = lh[(stg, pg, dev)]
            b = (lambda s: f'**{s}**') if stg == 'after' else str
            rows.append(f'| {pn} | {dev.capitalize()} | {sn} | {b(x["performance"])} | {x["accessibility"]} | {x["bestPractices"]} | {x["seo"]} | {fmt(x["fcp"])} | {b(fmt(x["lcp"]))} | {x["cls"]} | {fmt(x["tbt"])} |')
w('lighthouse.md', '\n'.join(rows))

# ---------- проваленные аудиты «до»
names = {'render-blocking-insight': 'Запросы, блокирующие отрисовку', 'network-dependency-tree-insight': 'Дерево зависимостей сети (цепочка CSS → шрифты)',
         'cache-insight': 'Неэффективное кэширование статики', 'document-latency-insight': 'Задержка ответа документа',
         'forced-reflow-insight': 'Принудительная перекомпоновка (forced reflow)', 'lcp-breakdown-insight': 'Разбивка LCP: задержка отрисовки элемента',
         'first-contentful-paint': 'First Contentful Paint', 'largest-contentful-paint': 'Largest Contentful Paint', 'speed-index': 'Speed Index'}
rows = ['| Аудит Lighthouse | Оценка | Значение |', '|---|---|---|']
for a in d['failedBefore']:
    val = re.sub(r'Est savings of ', 'ожидаемая экономия ', fmt(a['value'])).replace('KiB', 'КБ')
    rows.append(f'| {names.get(a["id"], a["title"])} | {round(a["score"] * 100)} / 100 | {val or "—"} |')
w('lh-failed.md', '\n'.join(rows))

# ---------- waterfall
wf = d['waterfall']
rng = lambda st, k: f'{num(min(r[k] for r in wf[st]["runs"]) / 1000)}–{num(max(r[k] for r in wf[st]["runs"]) / 1000)}'
rows = ['| Показатель (Slow 4G, главная, медиана 3 прогонов) | До | После |', '|---|---|---|',
        f'| Запросов | {wf["before"]["requests"]} | **{wf["after"]["requests"]}** |',
        f'| Из них CSS (блокируют отрисовку) | 6 | **1** |',
        f'| Передано, КБ | {wf["before"]["totalKB"]} | {wf["after"]["totalKB"]} |',
        f'| First Contentful Paint, с (разброс) | {num(wf["before"]["fcpMs"] / 1000)} ({rng("before", "fcp")}) | **{num(wf["after"]["fcpMs"] / 1000)}** ({rng("after", "fcp")}) |',
        f'| Largest Contentful Paint, с (разброс) | {num(wf["before"]["lcpMs"] / 1000)} ({rng("before", "lcp")}) | **{num(wf["after"]["lcpMs"] / 1000)}** ({rng("after", "lcp")}) |',
        f'| Полная загрузка (Load), с (разброс) | {num(wf["before"]["loadMs"] / 1000)} ({rng("before", "load")}) | **{num(wf["after"]["loadMs"] / 1000)}** ({rng("after", "load")}) |',
        f'| Самая длинная задача главного потока, мс | {wf["before"]["longTask"]["duration"]} | {wf["after"]["longTask"]["duration"]} |']
w('waterfall.md', '\n'.join(rows))
rows = ['| Ресурс | Тип | Размер, КБ |', '|---|---|---|'] + [f'| `{h["url"]}` | {h["type"]} | {num(h["kb"])} |' for h in wf['after']['heaviest']]
w('heaviest.md', '\n'.join(rows))

# ---------- участники
P = read('participants.csv')
rows = ['| Участник | Возраст | Опыт в интернете | Устройство | Знаком с сайтом |', '|---|---|---|---|---|']
rows += [f'| {p["participant"]} | {p["age"]} | {p["internet_experience"]} | {p["device"]} | {p["familiar_with_site"]} |' for p in P] or \
        ['| [[ЗАПОЛНИТЬ: research/participants.csv]] | | | | |']
w('participants.md', '\n'.join(rows))

# ---------- протокол
T = read('protocol.csv')
rows = ['| Участник | Сценарий | Время, с | Успех | Ошибки | Комментарии |', '|---|---|---|---|---|---|']
rows += [f'| {t["participant"]} | {t["scenario"]} | {t["time_s"]} | {t["success"]} | {t["errors"] or "—"} | {t["comments"] or "—"} |' for t in T] or \
        ['| [[ЗАПОЛНИТЬ: research/protocol.csv]] | | | | | |']
w('protocol.md', '\n'.join(rows))
rows = ['| Сценарий | Участников | Успешно | Доля успеха | Среднее время, с | Ст. отклонение, с |', '|---|---|---|---|---|---|']
by = {}
for t in T: by.setdefault(t['scenario'], []).append(t)
for sc in sorted(by):
    rs = by[sc]; ok = sum(r['success'].strip().lower() in ('да', 'yes', '1') for r in rs); times = [float(r['time_s']) for r in rs]
    rows.append(f'| {sc} | {len(rs)} | {ok} | {round(100 * ok / len(rs))}% | {num(st.mean(times))} | {num(st.stdev(times)) if len(times) > 1 else "—"} |')
if not by: rows.append('| [[ЗАПОЛНИТЬ: появится после заполнения protocol.csv]] | | | | | |')
w('protocol-summary.md', '\n'.join(rows))

# ---------- SUS
S = read('sus.csv')
rows = ['| Участник | Q1 | Q2 | Q3 | Q4 | Q5 | Q6 | Q7 | Q8 | Q9 | Q10 | SUS | Оценка |', '|---|---|---|---|---|---|---|---|---|---|---|---|---|']
scores = []
for s in S:
    sc = sus_score(s); scores.append(sc)
    rows.append('| ' + ' | '.join([s['participant']] + [s[f'q{i}'] for i in range(1, 11)]) + f' | **{num(sc)}** | {sus_label(sc)} |')
if scores:
    rows.append(f'| **Среднее** | | | | | | | | | | | **{num(st.mean(scores))}** | {sus_label(st.mean(scores))} |')
    w('sus-summary.md', f'Средний SUS = **{num(st.mean(scores))}** ({sus_label(st.mean(scores))}); стандартное отклонение {num(st.stdev(scores)) if len(scores) > 1 else "—"}; n = {len(scores)}.')
else:
    rows.append('| [[ЗАПОЛНИТЬ: research/sus.csv]] | | | | | | | | | | | | |')
    w('sus-summary.md', '[[ЗАПОЛНИТЬ: средний SUS появится после заполнения research/sus.csv]]')
w('sus.md', '\n'.join(rows))

# ---------- A/B
AB = read('ab_results.csv')
labels = {'cta_clicks': 'Клики по CTA', 'time_to_cta_s': 'Время до клика по CTA, с', 'max_scroll_pct': 'Глубина скролла, %',
          'rage_clicks': 'Rage clicks', 'ease_1_5': 'Лёгкость поиска (1–5)', 'sus': 'SUS'}
better_low = {'time_to_cta_s', 'rage_clicks'}
rows = ['| Метрика | A: среднее ± SD (n) | B: среднее ± SD (n) | t | p (Уэлч) | Лучше | Значимо (α = 0,05) |', '|---|---|---|---|---|---|---|']
concl = []
groups = {v: [r for r in AB if r['variant'].strip().upper() == v] for v in 'AB'}
for m, ln in labels.items():
    vals = {v: [float(r[m]) for r in rs if r.get(m, '').strip()] for v, rs in groups.items()}
    if min(len(vals['A']), len(vals['B'])) < 2: continue
    t, df, p = welch(vals['A'], vals['B'])
    ma, mb = st.mean(vals['A']), st.mean(vals['B'])
    best = ('A' if ma < mb else 'B') if m in better_low else ('A' if ma > mb else 'B')
    if ma == mb: best = '—'
    rows.append(f'| {ln} | {num(ma)} ± {num(st.stdev(vals["A"]))} ({len(vals["A"])}) | {num(mb)} ± {num(st.stdev(vals["B"]))} ({len(vals["B"])}) | {num(t)} | {f'{p:.3f}'.replace('.', ',')} | {best} | {"да" if p < 0.05 else "нет"} |')
    concl.append((ln, best, p, ma, mb))
if len(rows) == 2:
    rows.append('| [[ЗАПОЛНИТЬ: research/ab_results.csv, по 10+ участников на вариант]] | | | | | | |')
    w('ab-conclusion.md', '[[ЗАПОЛНИТЬ: вывод сформируется автоматически после заполнения research/ab_results.csv]]')
else:
    wins = {v: sum(1 for c in concl if c[1] == v) for v in 'AB'}
    sig = [c for c in concl if c[2] < 0.05]
    lead = 'B' if wins['B'] > wins['A'] else 'A' if wins['A'] > wins['B'] else None
    text = (f'Вариант {lead} лучше по {max(wins.values())} из {len(concl)} метрик. ' if lead else 'Варианты разделили метрики поровну. ')
    text += ('Статистически значимые различия (p < 0,05): ' + '; '.join(f'{c[0].lower()} (p = {c[2]:.3f}, лучше {c[1]})'.replace('.', ',') for c in sig) + '. ') if sig else \
            'Ни одно различие не достигло статистической значимости (p ≥ 0,05): при выборке такого размера наблюдаемые различия могут быть случайными. '
    text += (f'Рекомендуется принять вариант {lead}' + (', но подтвердить результат на большей выборке.' if not sig else '.')) if lead else 'Решение по данным не определяется; рекомендуется увеличить выборку.'
    w('ab-conclusion.md', text)
w('ab.md', '\n'.join(rows))
w('ab-n.md', f'Участников: вариант A — {len(groups["A"])}, вариант B — {len(groups["B"])}.' if AB else '[[ЗАПОЛНИТЬ: число участников по вариантам]]')

# ---------- проблемы и рекомендации
PR = read('problems.csv')
prio = lambda i, e: {('высокий', 'низкие'): 'Делать сейчас', ('высокий', 'высокие'): 'Планировать', ('высокий', 'средние'): 'Планировать',
                     ('средний', 'низкие'): 'Делать сейчас', ('средний', 'средние'): 'Планировать', ('низкий', 'низкие'): 'Делать при случае'}.get((i, e), 'Не делать')
rows = ['| № | Проблема | Источник данных | Решение | Эффект / усилия | Приоритет | Статус |', '|---|---|---|---|---|---|---|']
for k, p in enumerate(PR, 1):
    rows.append(f'| {k} | {p["problem"]} | {p["source"]} | {p["solution"]} | {p["impact"]} / {p["effort"]} | {prio(p["impact"], p["effort"])} | {p["status"]} |')
user_rows = sum(1 for p in PR if p['source'] and not re.search(r'Lighthouse|PageSpeed|Ручная', p['source']))
if user_rows < 5:
    rows.append(f'| {len(PR) + 1} | [[ЗАПОЛНИТЬ: ещё {5 - user_rows} и более проблем по итогам Clarity и юзабилити-тестов (research/problems.csv)]] | | | | | |')
w('problems.md', '\n'.join(rows))

obs = (RES / 'observations.md').read_text(encoding='utf-8') if (RES / 'observations.md').exists() else ''
obs = re.sub(r'<!--.*?-->', '', obs, flags=re.S).strip()
w('observations.md', obs or '[[ЗАПОЛНИТЬ: наблюдения из записей Clarity и юзабилити-сессий — research/observations.md]]')

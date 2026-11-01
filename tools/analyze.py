#!/usr/bin/env python3
"""Обработка результатов исследования (Лаб. 3) без внешних библиотек.

  python3 tools/analyze.py sus research/sus.csv            # SUS каждого участника + среднее
  python3 tools/analyze.py protocol research/protocol.csv  # успех и время по сценариям
  python3 tools/analyze.py ab research/ab_results.csv      # A/B: среднее, SD, t-тест Уэлча
"""
import csv, math, statistics as st, sys
from collections import defaultdict


def read(path):
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def sus_score(row):
    odd = sum(int(row[f"q{i}"]) - 1 for i in (1, 3, 5, 7, 9))
    even = sum(5 - int(row[f"q{i}"]) for i in (2, 4, 6, 8, 10))
    return (odd + even) * 2.5


def sus_label(x):
    return "отлично" if x >= 80 else "хорошо" if x >= 68 else "удовлетворительно" if x >= 50 else "плохо"


def _betacf(a, b, x):
    tiny = 1e-30
    qab, qap, qam = a + b, a + 1, a - 1
    c, d = 1.0, 1 - qab * x / qap
    d = 1 / (d if abs(d) > tiny else tiny)
    h = d
    for m in range(1, 200):
        m2 = 2 * m
        for aa in (m * (b - m) * x / ((qam + m2) * (a + m2)),
                   -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))):
            d = 1 + aa * d
            d = 1 / (d if abs(d) > tiny else tiny)
            c = 1 + aa / c
            c = c if abs(c) > tiny else tiny
            delta = d * c
            h *= delta
        if abs(delta - 1) < 1e-12:
            break
    return h


def _betainc(a, b, x):
    """Регуляризованная неполная бета-функция I_x(a, b)."""
    if x <= 0: return 0.0
    if x >= 1: return 1.0
    bt = math.exp(math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b) + a * math.log(x) + b * math.log(1 - x))
    if x < (a + 1) / (a + b + 2):
        return bt * _betacf(a, b, x) / a
    return 1 - bt * _betacf(b, a, 1 - x) / b


def welch(a, b):
    """t-тест Уэлча (двусторонний) — аналог T.TEST(A; B; 2; 3) в Google Sheets."""
    va, vb = st.variance(a) / len(a), st.variance(b) / len(b)
    t = (st.mean(a) - st.mean(b)) / math.sqrt(va + vb)
    df = (va + vb) ** 2 / (va ** 2 / (len(a) - 1) + vb ** 2 / (len(b) - 1))
    p = _betainc(df / 2, 0.5, df / (df + t * t))
    return t, df, p


def cmd_sus(rows):
    scores = [sus_score(r) for r in rows]
    for r, s in zip(rows, scores):
        print(f"участник {r['participant']}: SUS = {s:.1f} ({sus_label(s)})")
    if scores:
        print(f"средний SUS = {st.mean(scores):.1f} ({sus_label(st.mean(scores))}), n = {len(scores)}")


def cmd_protocol(rows):
    by = defaultdict(list)
    for r in rows:
        by[r["scenario"]].append(r)
    for sc, rs in sorted(by.items()):
        ok = sum(r["success"].strip().lower() in ("да", "yes", "1") for r in rs)
        times = [float(r["time_s"]) for r in rs]
        print(f"сценарий {sc}: успех {ok}/{len(rs)} ({100*ok/len(rs):.0f}%), среднее время {st.mean(times):.0f} с")


def cmd_ab(rows):
    groups = {v: [r for r in rows if r["variant"].upper() == v] for v in ("A", "B")}
    for metric in ("cta_clicks", "time_to_cta_s", "max_scroll_pct", "sus"):
        vals = {v: [float(r[metric]) for r in rs if r[metric] != ""] for v, rs in groups.items()}
        if min(len(vals["A"]), len(vals["B"])) < 2:
            print(f"{metric}: недостаточно данных")
            continue
        t, df, p = welch(vals["A"], vals["B"])
        print(f"{metric}: A = {st.mean(vals['A']):.2f} ± {st.stdev(vals['A']):.2f} (n={len(vals['A'])}), "
              f"B = {st.mean(vals['B']):.2f} ± {st.stdev(vals['B']):.2f} (n={len(vals['B'])}), "
              f"t = {t:.2f}, df = {df:.1f}, p = {p:.4f} -> {'значимо' if p < 0.05 else 'не значимо'} (α = 0.05)")


if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] not in ("sus", "protocol", "ab"):
        sys.exit(__doc__)
    {"sus": cmd_sus, "protocol": cmd_protocol, "ab": cmd_ab}[sys.argv[1]](read(sys.argv[2]))

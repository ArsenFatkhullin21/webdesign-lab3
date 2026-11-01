#!/usr/bin/env python3
"""Собирает два варианта сайта для A/B-теста в dist/a и dist/b.

Каждую папку можно перетащить на Netlify Drop (отдельный сайт на вариант).
Запуск:  CLARITY_ID=xxxxxxxxxx python3 tools/make_dist.py
(без CLARITY_ID сайт собирается без счётчика)
"""
import os, shutil, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KEEP = ["img", "js", "css", "_headers"]
for variant in ("a", "b"):
    subprocess.run([sys.executable, str(ROOT / "tools/build.py")], check=True, env={**os.environ, "VARIANT": variant})
    out = ROOT / "dist" / variant
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    for f in ROOT.glob("*.html"):
        shutil.copy(f, out / f.name)
    for name in KEEP:
        src = ROOT / name
        (shutil.copytree if src.is_dir() else shutil.copy)(src, out / name)
    shutil.rmtree(out / "css", ignore_errors=True)
    (out / "css").mkdir()
    shutil.copy(ROOT / "css/bundle.css", out / "css/bundle.css")
    print("dist/%s готов" % variant)
subprocess.run([sys.executable, str(ROOT / "tools/build.py")], check=True)  # вернуть вариант A в корне

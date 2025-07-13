"""Funciones utilitarias."""

import shutil
from pathlib import Path


def copytree(src: Path, dst: Path):
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)

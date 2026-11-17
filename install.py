#!/usr/bin/env python3
"""Install the meme-gen skill for your AI tool (stdlib only).

  python install.py --target claude            -> ~/.claude/skills/meme-gen
  python install.py --target agents            -> ~/.agents/skills/meme-gen   (Codex, Antigravity, others)
  python install.py --target gemini            -> ~/.gemini/config/skills/meme-gen
  python install.py --target all --project     -> ./.claude/skills and ./.agents/skills in the current folder
"""
import argparse, shutil, sys
from pathlib import Path

SRC = Path(__file__).resolve().parent / "skills" / "meme-gen"
DEST = {"claude": (".claude/skills",), "agents": (".agents/skills",), "gemini": (".gemini/config/skills",)}

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--target", choices=["claude", "agents", "gemini", "all"], default="all")
    p.add_argument("--project", action="store_true", help="install into the current folder instead of your home folder")
    a = p.parse_args()
    if not SRC.is_dir():
        sys.exit(f"skill folder not found: {SRC}")
    base = Path.cwd() if a.project else Path.home()
    keys = list(DEST) if a.target == "all" else [a.target]
    if a.project and "gemini" in keys:
        keys.remove("gemini")  # Antigravity reads project skills from .agents/skills
    for k in keys:
        dst = base / DEST[k][0] / "meme-gen"
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(SRC, dst, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        print(f"installed -> {dst}")
    print("Done. In your AI tool say: meme gen, 5 memes about <topic>")

if __name__ == "__main__":
    main()

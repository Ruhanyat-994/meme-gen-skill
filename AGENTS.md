# meme-gen (agent instructions)

When the user asks for "meme gen", memes, or to caption an image:

1. Read `skills/meme-gen/SKILL.md` and follow it exactly.
2. Run the CLI from the user's current folder: `python3 skills/meme-gen/scripts/meme_gen.py <command>` (adjust the path if the skill is installed elsewhere, e.g. `.agents/skills/meme-gen/`).
3. Output goes to `./memes/`. Look at the contact sheets from `check` before reporting done.

Commands: doctor, templates, url, render, batch, custom, check. Python 3.8+, no required dependencies (Pillow optional).
Network: needs HTTPS to `api.memegen.link`.

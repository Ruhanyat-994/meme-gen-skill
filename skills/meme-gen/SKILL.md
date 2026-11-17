---
name: meme-gen
description: AI meme generator. Makes funny, readable meme images from a topic, today's news, or your own image and saves them in the current folder. Use for "meme gen", "make N memes about X", meme maker, tech or programming memes, social media meme content, or adding text to an image.
---

# meme-gen

Makes captioned memes using the open-source memegen.link renderer and a stdlib-only Python CLI.
Output goes to `./memes/` in the folder the user is working in (the current working directory).

Always run the CLI from the user's current folder:
`python3 <path-to-this-skill>/scripts/meme_gen.py ...`  (use `python` on Windows if `python3` is missing)

## Request pattern

"meme gen: 10 memes about Kubernetes" -> topic memes. "meme gen: 5 memes from today's tech news" -> news mode.
"meme gen: put 'when the build passes' on photo.jpg" -> custom image mode. Default count if none is given: 5.

## Workflow (topic memes)

1. Run `doctor` once. If the network check fails, tell the user to allow HTTPS access to `api.memegen.link` in their tool's network/sandbox settings. Do not try other ways around it.
2. Run `templates` (optionally with a filter such as `templates escalation`) and read the `use for` hints. Pick a different template for each meme where you can.
3. Write the jokes (see `references/joke-shapes.md`): 3-8 words per box, max 12, one idea per meme, easy to get in two seconds. Match the number of boxes to the template, in the order shown in `boxes:`.
4. Save them as a JSON list, e.g. `memes-plan.json` in the scratch location, then show the user the plan (template + text) if they asked to approve first; otherwise go straight on.
   `[{"template":"drake","text":["Reading docs","Guessing until it works"],"caption":"optional post text","hashtags":["#dev"]}]`
5. Run `batch memes-plan.json` (writes images, `captions.csv`, `manifest.json` into `./memes/`).
6. Run `check memes` and LOOK at the contact sheets it prints (open the PNGs). Fix and re-render any meme with cut-off text, an unclear joke, or text on the wrong panel. Re-run only the fixed ones.
7. Tell the user the folder, the count, and anything you dropped. Mention that images come from memegen.link.

Single meme: `render --template drake --text "top" "bottom"`.

## News mode

Only if you have web search. Follow `references/news-mode.md`: find 3-6 real stories from the last 48 hours, confirm each in two sources, skip tragedies, politics and unverified claims, then write jokes about the decision, tool or situation (never about private people). Put a short source note in each `caption`.

## Custom image mode

`custom --image photo.jpg --top "when it works" --bottom "on the first try"` (local files need Pillow: `pip install pillow`).
Options: `--style bar` (caption bar above the image), `--box "0.1,0.7,0.8,0.25,o=text"` for free placement (x,y,w,h as fractions; style o=outlined white, k=black, w=white). An https image URL also works for plain top/bottom text. Check the result by viewing the image.

## Rules

- Funny about situations, tools, habits and company decisions. Never about private individuals, protected groups, tragedies, or politics. No real-person insults. See `references/safety.md`.
- Never put secrets, personal data, or someone's name/photo into captions.
- Be honest about failures: report which memes failed and why. Never claim success without running `check`.
- Do not fetch images from other hosts; the CLI only talks to the configured image service.

## Troubleshooting

- `HTTP 403` / network error -> allow `api.memegen.link` (see Workflow step 1).
- `404` -> unknown template id; run `templates --live <word>`.
- Text too long -> shorten; many words shrink and become unreadable.
- Full command reference: `python3 scripts/meme_gen.py --help` and `<command> --help`.

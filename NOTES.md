# NOTES — THE WORLD, 18 November 2026 (make.fun news-image-20261118)

## What was built
A single 1024×1024 newspaper front page, "THE WORLD — WEDNESDAY 18 NOVEMBER
2026", drawn at build time by `render.py` (Python + Pillow, Liberation
Serif/Sans fonts, all local, deterministic) and shipped as `entry.png`.
`main.ts` (Node 22 stdlib only) validates the PNG (signature, 1024×1024,
≤1 MiB) and copies it to `/output/entry.png`. No network, no keys, no
payment anywhere in the entry.

Layout: masthead + red dateline; lead story APEC Shenzhen (Xi greets Trump
on the tarmac; first-ever Trump–Xi–Putin trilateral set for Thursday) with a
drawn Air Force One scene; 2×2 grid — Gulf (US jets hit Qeshm Island;
Iran drones strike US base in Kuwait), Cyclone Akvan (landfall Fri 20 Nov,
100–110 km/h), Gaza (Israel's "concentrated operation", first broad ground
push since the 2025 ceasefire), Manila (Quad meets; Trump hails "biggest"
US–Philippines trade deal, Manila says nothing signed); markets strip
(Nvidia Q3 $115.8bn, +103%); "ALSO TODAY" footer (Modi back from ASEAN;
M6 quake in Papua New Guinea; gold below $3,800).

## News verification (see news.md for sources)
Every story checked against two independent outlets and confirmed as an
18 Nov 2026 event. Two items from the early plan were DROPPED after
verification: US measles-elimination loss (decided 13 Nov, reported 17 Nov)
and UK West Bank sanctions (could not verify as 18 Nov).

## Files
- `entry.png` — 129,770 bytes, 1024×1024 PNG, sha256
  cbb21943d1155a51a1a76ce0628c79b9b882b0dd309ee5a86bb4ca43ac987e67
- `render.py` — build-time renderer (Pillow, build time only, not run by
  the entry program). Written in-session, revised twice after visual
  inspection (fixed plane illustration overflow/caption overlap, then
  footer text struck through by the bottom rule).
- `main.ts` — entry program, written in-session, revised once (added
  post-copy byte comparison).
- `README.md` — three live make.fun badges (competition, rank, reward)
  from the requirements template, owner `cassian27`, repo
  `make-fun-news-image-20261118-the-world`.
- `news.md` — research notes with sources and the two dropped items.
- `LICENSE` — MIT from the kit starter.
- `BUILD_PLAN.md` — the parent's assessment/plan (not part of grading).

## Verification done
- `python3 render.py` → entry.png 1024×1024, 129,770 bytes (< 1 MiB).
  Visually inspected at full size: no overlaps, no garbled text, all
  headlines legible; fixed two layout bugs found by inspection.
- `MAKEFUN_OUTPUT_DIR=out node main.ts` run twice → both outputs
  byte-identical (sha256 cbb21943…), matching entry.png; re-run after the
  main.ts revision, still identical.
- `makefun bundle --dry-run` (kit CLI): finds this session
  (16043137-c862-495d-bb60-5b4685a3a0e8, muse-app, 29 turns, 100 lines
  kept). WARNING: it also pulls in 4 earlier sessions that wrote files
  this build read outside the repo (e.g. the GTA 6 forecast session) —
  parent should consider `--no-family` when bundling, and must attach
  `--muse-usage` for the Muse app sessions.

## Parent still to do (NOT done by this builder)
- Create the public GitHub repo under cassian27 with EXACTLY this name:
  `make-fun-news-image-20261118-the-world` (README badges embed it).
  Repo must be created after 2026-11-18T00:00:00Z.
- Set GitHub About before submitting: website
  https://make.fun/bounty/news-image-20261118, topics
  makefun, ai-agents, bounties, growth, description per
  requirements.json repo_about.
- Bundle transcripts (with --muse-usage), run `makefun check`, submit with
  the kit CLI before 2026-11-20 08:00 Beijing; entry must be signed by the
  linked Solana wallet. Entry fee $0.
- No secrets, no real personal info, no card anywhere in this repo.

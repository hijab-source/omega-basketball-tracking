# Basketball's Rise, Analytics' Absence

**A reproducible player-level data pipeline for club basketball in Pakistan.**

Submitted to the MIT Sloan Sports Analytics Conference (SSAC) Research Paper Competition.

> Note on terminology: this is a *player-level* pipeline built from official box scores,
> not optical/positional "player tracking" (x-y coordinate, movement-based tracking like
> SportVU/Second Spectrum). We use "tracking" in the everyday sense of systematically
> recording and following a stat over time, not the technical sports-analytics term.

## What this is

Basketball has been played in Pakistan since the early 1900s, and the national federation
has existed since 1952 [[1]](#sources) — yet structured, player-level performance data has
been largely absent at the club level. This isn't a capability gap: Pakistan's cricket
league runs AI-powered player-tracking cameras and Hawk-Eye analytics every season
[[2]](#sources). Basketball has simply never received that investment.

Omega plays in Karachi's League of Basketball (LOB) — the same grassroots league whose
handwritten scoresheets appear throughout this repository's excluded-games documentation.
Most LOB teams still record games only on those handwritten sheets. Omega was the first
LOB team to adopt official FIBA/Genius Sports box-score tracking, after a heavy loss to a
Lahore-based opponent; the practice has since spread to other teams across the league.

This repository contains the extraction pipeline that turns those official box-score PDFs
into structured, analysis-ready data, and the resulting dataset for Omega's 2025–26
season.

## Why this matters

This isn't a story about Pakistan lacking the technical capacity for sports analytics.
Two things make that clear:

- **Cricket already has it.** The Pakistan Super League runs AI-powered player-tracking
  cameras and a Hawk-Eye Decision Review System, with more than 30 broadcast cameras,
  augmented/virtual-reality graphics, and Spidercam (PCB's PSL 10 and PSL 11 technology
  rollouts, 2025–2026) [[3]](#sources)[[4]](#sources). Pakistani cricket analytics
  research exists too — e.g. Bhatti (2021), *"Predicting the Best Team Players of Pakistan
  Super League using Machine Learning Algorithms,"* ranked PSL batsmen and bowlers with
  Random Forest models, using ball-by-ball data that already existed on Cricinfo
  [[5]](#sources).
- **Pakistani researchers already do basketball machine learning — just not on Pakistani
  basketball.** Shahzad, Rehman, Batool & Ullah (2021), of COMSATS University Islamabad,
  built seven ML models to predict Kobe Bryant's shot outcomes — using a public Kaggle
  dataset of an NBA player, because no equivalent dataset existed for a Pakistani player
  or club [[6]](#sources). The interest and the skill were there. The data, for basketball
  in Pakistan, simply wasn't.

That's the gap this repository starts to close: not by building another model on data
someone else already collected, but by building the pipeline that creates the data in
the first place, for a sport that has largely lacked it.

We make no claim that this is the *only* structured basketball dataset that has ever
existed in Pakistan — only that we could not find a public, reproducible, club-level one,
and that this repository is offered as exactly that.

## Repository contents

```
extract_fiba_box_scores.py   # Parses official FIBA/Genius Sports box-score PDFs into
                              # tidy player-game rows (see "Pipeline" below)
data/
  omega_full_season_raw.csv  # All 239 player-game rows extracted from 8 fully-documented
                              # Omega games (Nov 2025-Jan 2026), both teams, all players
  karachi_5player_dataset.csv# The 5 rostered Omega players with complete season coverage
                              # (Ans Azhar, Zakaria Siddiqui, Shayan Qadri, Usman Khalid,
                              # Ali Chanzeb), with True Shooting%, Game Score, and AST/TOV
                              # computed per game, split into Early/Late season halves
  league_wide_evidence/      # Official digital box scores involving OTHER LOB teams
                              # (not Omega) -- documentary evidence only, not analyzed or
                              # included in any statistic above. See "League-wide evidence"
requirements.txt
LICENSE
```

## Pipeline

`extract_fiba_box_scores.py` reads a folder of PDF game reports and, for every file that
is a **FIBA Box Score** (as opposed to the five other Genius Sports report types a game
can generate — Line Up Analysis, Player Evaluation, Shot Areas, Scoresheet, and partial/
halftime box scores — which are skipped automatically), extracts:

- Game metadata: date, game number, both team names/abbreviations, report-generation
  timestamp, number of quarters played
- Every player's row: minutes (converted from MM:SS to decimal), FG/2P/3P/FT makes and
  attempts, offensive/defensive/total rebounds, assists, turnovers, steals, blocks,
  personal fouls, fouls drawn, plus-minus, and points — with DNP players correctly
  flagged rather than dropped

It then:

- **Deduplicates partial reports.** The same game sometimes generates more than one box
  score (e.g. a halftime report alongside the final one). Matching is keyed on **data
  extracted from each PDF's own content — game number and game date, as printed in the
  report header — never on source file names**, which are inconsistent, user-renamed, and
  not a reliable join key. The script groups rows by (game number, game date) and keeps
  only the report with the most quarters played, discarding the partial duplicate. The
  file name is retained in the output only as a provenance field, so every row can be
  traced back to its source PDF.
- **Normalizes inconsistent formatting.** Genius Sports' PDF export embeds zero-width
  Unicode characters that break naive text matching, and the same player can appear under
  several name/jersey-number variants across different games (e.g. `USMAN QADRI`,
  `USMAAN QADRI`, `QADRI USMAN` for the same player). The script strips invisible
  characters and resolves player identity by jersey number — also extracted from the
  report body, not inferred from any file name — cross-checked against name spelling.
- **Computes advanced metrics** per player-game: True Shooting % (`PTS / (2 × (FGA +
  0.44 × FTA))`), Game Score (Hollinger's formula), and Assist/Turnover ratio. AST/TOV is
  undefined for a zero-turnover game; those games are left blank (not zero, and not
  substituted with the raw assist count) and excluded from any season-average AST/TOV,
  matching the convention used for the paper's reported per-player averages.

### Usage

```bash
pip install -r requirements.txt
python3 extract_fiba_box_scores.py <folder_of_pdfs> <output.csv>
```

## Data

Omega played 11 games in the tracked window (Nov 22, 2025 – Jan 23, 2026). 8 of them have
official digital box scores; the other 3 (vs. Void, Raiders, and Backstreet Raiders) were
recorded only on handwritten LOB league scoresheets. Final scores on those 3 are legible
and consistent with the digital data, but tally-mark fields (rebounds, assists, blocks)
could not be transcribed with full confidence, so those games were kept out of the
statistical dataset rather than risk including uncertain numbers. All results below (7–1
record, margins, per-player stats) describe only the 8 digitally-documented games, not
Omega's full 11-game record in the window.

`data/omega_full_season_raw.csv` — 239 player-game rows extracted from those 8 games,
covering both teams' full rosters (starters, bench, and DNPs), cross-checked against the
source PDFs.

`data/karachi_5player_dataset.csv` — the 37-row subset used in the paper's Results
section: the 5 Omega players with the most complete records across the 8 games (6–8 games
each), with derived metrics (True Shooting%, Game Score, AST/TOV) and an Early/Late season
split for within-player comparison.

## League-wide evidence

`data/league_wide_evidence/` holds four additional official FIBA/Genius Sports box scores,
none of which involve Omega:

| Teams | Date |
|---|---|
| 23rd Street Ballers vs. Mambas | 31 Aug 2025 |
| 23rd Street Ballers vs. Raiders | 3 Aug 2025 |
| 23rd Street Ballers vs. Bounce | 11 Jan 2026 |
| Bounce vs. 23rd Street Ballers | 16 May 2026 |

These are included as **documentary evidence**, not as data: they confirm that digital
box-score tracking — the practice Omega adopted first — has since been used by at least
four other LOB teams, supporting the paper's claim that the practice spread across the
league. They are not parsed into any statistic reported in the abstract, and they do not
constitute season-level coverage of any of these teams; each file is a single incidentally
available game, not a systematic collection. Building an actual league-wide dataset — full
game logs per team, with documented completeness the way Omega's 8-of-11 is documented —
is future work, not something these four files establish on their own.

## Citation

If you use this pipeline or dataset, please cite the accompanying SSAC Research Paper
Competition abstract, *"Basketball's Rise, Analytics' Absence: A Reproducible
Player-Level Data Pipeline for Club Basketball in Pakistan."*

## Sources

1. Pakistan Basketball Federation — founding and history:
   [Wikipedia](https://en.wikipedia.org/wiki/Pakistan_Basketball_Federation),
   [official site](https://pbbf.com.pk/about.html)
2. FIBA Regional Office–Asia, "FIBA Regional Office-Asia sets course for development in
   Pakistan basketball" (May 2026):
   [about.fiba.basketball](https://about.fiba.basketball/en/news/fiba-regional-office-asia-sets-course-for-development-in-pakistan-basketball) —
   see also [The Nation, 18 May 2026](https://www.nation.com.pk/18-May-2026/fiba-backs-basketball-rebuild-pakistan)
   and [Minute Mirror](https://minutemirror.com.pk/fiba-visit-to-pakistan-signals-new-era-for-basketball-development-and-youth-training-557104/).
   Note: "grassroots and professional levels" is our own paraphrase of language used across
   this coverage, not a verbatim quote from a FIBA official — none of the three sources
   attribute that exact phrase to anyone by name.
3. PCB, PSL 10 player-tracking technology rollout:
   [Cricfit](https://cricfit.com/pcb-unveils-player-tracking-in-psl-10-check-the-details-here/)
4. PCB, PSL 11 broadcast upgrade (30+ cameras, DRS, AR, Spidercam):
   [LCCI](https://lcci.pk/pcb-upgrades-psl-11-broadcast-with-30-cameras-drs-ar-and-spidercam/)
5. Bhatti, K. (2021). "Predicting the Best Team Players of Pakistan Super League using
   Machine Learning Algorithms." *International Journal of Computer Applications*, 183(16).
   [IJCA (publisher)](https://www.ijcaonline.org/archives/volume183/number16/32008-2021921486/)
6. Shahzad, N., Rehman, A., Batool, S. & Ullah, F. (2021). "Kobe Bryant Shot Prediction
   using Machine Learning." COMSATS University Islamabad.
   [ResearchGate](https://www.researchgate.net/publication/354714486_Kobe_Braynt_Shot_Prediction_using_Machine_Learning)

## License

MIT — see `LICENSE`.

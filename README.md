# 🏀 Beyond Points-Only Scoresheets: Grassroots Basketball Analytics in Karachi

**Turning official club box scores into player efficiency and coaching insights: 8 games, 239 player records, 19 metrics per player-game.**

MSc thesis project · Data Analytics & AI · EDHEC Business School · **Work in progress**

---

## 🧩 The problem

In Karachi's League of Basketball (LOB), most teams still record games on handwritten
scoresheets that capture little more than points and fouls. Efficiency, rebounding,
ball control and overall contribution go unrecorded, so player evaluation, selection and
investment decisions rest on an incomplete picture.

## 📌 The gap

Basketball has been played in Pakistan since the early 1900s, and the national federation
has existed since 1952 [[1]](#-research-and-sources). Yet structured, club-level player
data is largely absent.

This is not a technology gap:

- **Cricket already has it.** The Pakistan Super League runs player-tracking cameras,
  Hawk-Eye and a full broadcast analytics set-up [[3]](#-research-and-sources)[[4]](#-research-and-sources),
  and Pakistani researchers publish machine learning work on PSL data [[5]](#-research-and-sources).
- **The data paradox.** Pakistani researchers have built basketball machine learning
  models on **Kobe Bryant** data, because no structured Pakistani basketball dataset
  existed [[6]](#-research-and-sources).

The skill and the interest are there. The data is not. This project builds the pipeline
that creates it.

## 🎓 Research questions

| # | Question | Status |
|---|---|---|
| **RQ1** | What does player-level data reveal that a points-only record hides? | ✅ Early results (8 games, 239 records) |
| **RQ2** | Can a low-cost, repeatable pipeline make this data usable for local clubs and federations? | 🔄 Built and validated on one club (Omega) |
| **RQ3** | How should insights be framed so coaches, athletes and federations act on them? (`Data → Insight → Action`) | ⏭️ Next phase |
| **RQ4** | How far does the framework scale, across the Karachi league and to other emerging-market sports? | 📋 Planned |

## 🔍 Early findings

The data covers **Omega**, the first LOB team to adopt official FIBA / Genius Sports
digital box scores: 8 digitally documented games (Nov 2025 to Jan 2026), 239 player-game
records across both rosters, and a 37-row analysis set for Omega's 5 core players.

**1. Volume hides efficiency.** Two players can look like comparable scorers on a
points-only sheet and play very different roles.

**2. Rebounding is invisible.** Zakaria Siddiqui ranked 4th of the 5 core players in
scoring but led them in rebounding, at 10.4 per game.

**3. Win-loss hides the season.** Omega went **7–1** in these games, with margins from
**+25 to a 3-point loss**: variation a bare record never shows.

**4. The core finding is the gap itself.** Each Omega player-game carries 19 box-score
and derived categories. Opponents' handwritten scoresheets record only points and fouls.

### Player roles the data reveals

| Player | Games | Points / game | True Shooting % | Rebounds / game | Role the data shows |
|---|---|---|---|---|---|
| Ans Azhar | 8 | 22.0 | 59.0% | 7.8 | Primary scorer, best ball control (1.27 AST/TOV) |
| Usman Khalid | 8 | 16.6 | 40.6% | 7.5 | High volume, low efficiency |
| Shayan Qadri | 6 | 13.7 | 52.3% | 2.3 | Secondary scorer (partial sample) |
| Zakaria Siddiqui | 8 | 8.6 | 56.3% | 10.4 | Rebounder, limited offensive role |
| Ali Chanzeb | 7 | 5.9 | 34.6% | 9.4 | Support role, strong on the boards |

*True Shooting % and AST/TOV are averages of per-game values; AST/TOV excludes
zero-turnover games. All figures cover the 8 digitally documented games only.*

## 💡 Implications

- **Coaches:** efficiency and rebounding measures identify how each player contributes,
  informing rotations and role allocation beyond points scored.
- **Players:** a fuller record of contribution, including work a points tally omits.
- **Federations and sponsors:** a low-cost, repeatable method for building the evidence
  base needed to identify undervalued talent and justify investment.

The project follows a **Data → Insight → Action** framework: Phase 1 establishes the data,
Phase 2 studies how insights must be presented for coaches and athletes to act on them.

This is infrastructure-stage work. It makes no causal claim about performance change.

## 💼 Business relevance

Missing performance data is a market problem as well as a sports one. Without it, clubs
misjudge player value, sponsors can't measure what they fund, and federations lack the
evidence to allocate resources. This project's next phases examine what drives clubs to
adopt performance data, what it costs to produce, and how it changes coaching and
selection decisions.

## 🗺️ Roadmap

- [x] **Phase 1: Data.** Extraction pipeline, Omega dataset, validation
- [ ] **Phase 2: Insight to action.** Player profiles and a simple coach-facing summary;
      test how coaches and players respond to different ways of presenting the same data
- [ ] **Phase 3: Scale.** A full season and other LOB clubs; a framework other
      under-resourced sports can reuse

## 📁 Repository contents

| File | What it is |
|---|---|
| `extract_fiba_box_scores.py` | Parses official FIBA / Genius Sports box-score PDFs into tidy player-game rows |
| `omega_full_season_raw.csv` | All 239 player-game rows from the 8 documented Omega games, both teams |
| `karachi_5player_dataset.csv` | The 37-row analysis set: Omega's 5 core players, with True Shooting %, Game Score, AST/TOV and an early/late-season split |
| `FIBA_Box_Score_23StreetBallers_*.pdf`, `FIBA_Box_Score_Bounce_*.pdf` | Four box scores from games not involving Omega. Kept as evidence that digital box scores have spread to other LOB teams; not analysed |
| `ABSTRACT.md` / `ABSTRACT.pdf` | Research abstract |
| `requirements.txt` | Python dependencies |

## ⚙️ How the pipeline works

`extract_fiba_box_scores.py` reads a folder of PDF game reports, keeps only FIBA Box Score
reports, and extracts game details and every player's line (minutes, shooting, rebounds,
assists, turnovers, steals, blocks, fouls, plus-minus, points). It then:

- **removes duplicate partial reports** (such as a halftime box score alongside the
  final one), matching on the game number and date printed inside each report, never on
  file names;
- **cleans inconsistent formatting**, including hidden characters in the PDF export and
  players listed under different name spellings, resolved by jersey number;
- **computes advanced metrics** per player-game: True Shooting %
  (`PTS / (2 × (FGA + 0.44 × FTA))`), Hollinger's Game Score, and AST/TOV (left blank
  for zero-turnover games rather than set to zero).

```bash
pip install -r requirements.txt
python3 extract_fiba_box_scores.py <folder_of_pdfs> <output.csv>
```

## ⚠️ Notes and limitations

- **"Tracking" here means recording stats over time**, not optical player tracking
  (x-y movement data such as SportVU or Second Spectrum).
- **Three of Omega's 11 games** in the window exist only as handwritten scoresheets.
  Their tally-mark fields could not be transcribed with confidence, so they are excluded.
- **One club, one partial season.** Findings describe this sample only.
- We could not find a public, reproducible club-level basketball dataset for Pakistan.
  We don't claim none has ever existed.

## 👤 Author

**Hijaab Fatima**, MSc Data Analytics & AI, EDHEC Business School. Former captain of
Pakistan's national women's basketball team, bringing first-hand knowledge of the league
context this project studies.

An earlier version of this work was submitted as an abstract to the MIT Sloan Sports
Analytics Conference Research Paper Competition.

Feedback is welcome, particularly from coaches, analysts and researchers working on sports
data in emerging markets. Please open an issue.

## 📚 Research and sources

**Research this project builds on**

5. Bhatti, K. (2021). "Predicting the Best Team Players of Pakistan Super League using
   Machine Learning Algorithms." *International Journal of Computer Applications*, 183(16).
   [IJCA](https://www.ijcaonline.org/archives/volume183/number16/32008-2021921486/)
6. Shahzad, N., Rehman, A., Batool, S. & Ullah, F. (2021). "Kobe Bryant Shot Prediction
   using Machine Learning." COMSATS University Islamabad.
   [ResearchGate](https://www.researchgate.net/publication/354714486_Kobe_Braynt_Shot_Prediction_using_Machine_Learning)

**Context**

1. Pakistan Basketball Federation, history:
   [Wikipedia](https://en.wikipedia.org/wiki/Pakistan_Basketball_Federation),
   [official site](https://pbbf.com.pk/about.html)
2. FIBA Regional Office–Asia, "FIBA Regional Office-Asia sets course for development in
   Pakistan basketball" (May 2026):
   [about.fiba.basketball](https://about.fiba.basketball/en/news/fiba-regional-office-asia-sets-course-for-development-in-pakistan-basketball);
   see also [The Nation, 18 May 2026](https://www.nation.com.pk/18-May-2026/fiba-backs-basketball-rebuild-pakistan)
3. PCB, PSL 10 player-tracking technology rollout:
   [Cricfit](https://cricfit.com/pcb-unveils-player-tracking-in-psl-10-check-the-details-here/)
4. PCB, PSL 11 broadcast upgrade (30+ cameras, DRS, AR, Spidercam):
   [LCCI](https://lcci.pk/pcb-upgrades-psl-11-broadcast-with-30-cameras-drs-ar-and-spidercam/)

## License

MIT. See `LICENSE`.

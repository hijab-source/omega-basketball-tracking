# Basketball's Rise, Analytics' Absence
### A Reproducible Player-Level Data Pipeline for Club Basketball in Pakistan

*Submitted to the MIT Sloan Sports Analytics Conference (SSAC) Research Paper Competition.*

## Introduction

Basketball has been played in Pakistan since the early 1900s, and the national federation
has existed since 1952. Yet structured player-level data has been almost entirely absent
at the club level. This is not a capability gap: Pakistan's cricket league runs AI-powered
player-tracking cameras and Hawk-Eye analytics every season. Basketball has never received
that investment. In May 2026, FIBA's Executive Director for Asia visited Pakistan to
discuss strengthening basketball at grassroots and professional levels, part of a wider
wave of grassroots organizing that includes Karachi's League of Basketball (LOB). Most LOB
teams still use only handwritten scoresheets. Omega was the first LOB team to adopt
FIBA/Genius Sports box-score tracking, after a heavy loss to a Lahore-based opponent, and
the practice has since taken hold across the league. A year later, in a rematch against
the same team, the margin collapsed from 10 points to 1, a shift we do not attribute to
tracking itself. We ask: what does player-level data reveal about a club's season that
this record-poor basketball culture has never been able to show?

## Methods

We built a Python extraction pipeline that converts FIBA/Genius Sports statistical reports
into structured player-game records, standardizing player, team, and game identifiers and
computing True Shooting%, Game Score, and AST/TOV per row. The pipeline resolves duplicate
partial reports through cross-game entity matching. We applied it to all
digitally-documented Omega games in the observation window (8 of 11 played, Nov 2025–Jan
2026; 3 others exist only as handwritten scoresheets and were excluded), extracting 239
player-game records across both rosters: 37 spanning the 5 Omega players with full
coverage. We cross-checked every extracted value against source PDFs and independently
re-verified all computations in a parallel spreadsheet.

## Results

Across these 8 games, Omega went 7-1, margins ranging from +25 to a 3-point loss:
variation invisible in a bare win-loss record. Tracking surfaces player roles no opponent
record could show: Ans Azhar carried a 22.0 PPG / 59.0% True Shooting and the team's best
ball control (1.27 AST/TOV) as primary scorer; Usman Khalid scored heavily (16.6 PPG) but
inefficiently (40.6% TS); Shayan Qadri added 13.7 PPG at 52.3% TS across a partial 6-game
sample; Zakaria Siddiqui averaged 10.4 rebounds in a limited offensive role; Ali Chanzeb,
at 5.9 PPG, filled a low-usage support role. Each player-game carries 19 box-score and
derived categories; opponents' handwritten scoresheets record only points and fouls. That
gap, not any single performance trend, is this paper's central, verifiable finding.

## Conclusion

This is infrastructure-stage work, not a causal claim about performance change: a
validated extraction method and open dataset for a data-poor sport. Applied more broadly,
the same low-cost pipeline could let clubs spot undervalued talent and give federations
evidence to justify investment: a small technical fix that could ripple across a
never-measured talent pipeline. The full manuscript will extend tracking across a complete
season and, where possible, to other Karachi LOB clubs that still track nothing.

---

*480 words (body), 494 including title.*

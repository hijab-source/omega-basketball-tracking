"""
FIBA / Genius Sports Box Score extractor.

Reads a folder of PDFs (official FIBA box score reports, possibly mixed in with
other report types: Line Up Analysis, Player Evaluation, Shot Areas -- and
possibly duplicate halftime vs final reports for the same game).

For each PDF:
  - Skips anything that isn't a "FIBA Box Score" report (by header text).
  - Extracts: game date, game number, both team names/abbreviations, and
    every player's row (skipping DNP).
  - Converts MM:SS minutes to decimal minutes.
  - Tags each row with the source file and report-generated timestamp, so
    that when the SAME game appears twice (halftime + final), we can keep
    only the most complete one (highest number of quarters / latest
    "Report Generated" timestamp) and drop the partial duplicate.

Output: one tidy CSV, one row per player per game, ready to filter down to
just the Karachi team and load into Karachi_Raw_Data.
"""

import re
import sys
import csv
from pathlib import Path
from datetime import datetime

import pdfplumber

# --- regex patterns -------------------------------------------------------

HEADER_DATE_RE = re.compile(
    r"([A-Za-z]{3}\s+\d{1,2}\s+[A-Za-z]{3}\s+\d{4})\s+Start time:\s*([\d:]+)"
)
GAME_NO_RE = re.compile(r"Game\s*No\.\s*:\s*(\d+)")
REPORT_GEN_RE = re.compile(r"Report Generated:\s*([A-Za-z]{3}\s+\d{1,2}\s+[A-Za-z]{3}\s+\d{4}\s+[\d:]+)")
QUARTER_HDR_RE = re.compile(r"\bQ1\b.*?(\bQ\d\b)(?!.*\bQ\d\b)", re.S)  # last Qn mentioned near the top scoring table
TEAM_HEADER_RE = re.compile(r"^([A-Za-z0-9&'\.\- ]+?)\s*\(([A-Z0-9]{2,5})\)(?:\s|$)")
SCORELINE_RE = re.compile(
    r"^(\*?)(\d{1,3})\s+(.+?)\s+(DNP|\d{1,3}:\d{2})\s*(.*)$"
)

NUMERIC_TAIL_LEN = 19  # tokens after Min for a played row: 8 (FG/2P/3P/FT M/A %) + OR DR TOT AS TO ST BS PF FD +/- PTS


def mmss_to_minutes(mmss: str) -> float:
    m, s = mmss.split(":")
    return round(int(m) + int(s) / 60, 2)


def parse_player_line(line: str):
    m = SCORELINE_RE.match(line.strip())
    if not m:
        return None
    starter, no, name, minutes, rest = m.groups()
    name = name.strip()
    STAT_FIELDS = ["Min", "FGM", "FGA", "2PM", "2PA", "3PM", "3PA", "FTM", "FTA",
                   "OREB", "DREB", "TREB", "AST", "TOV", "STL", "BLK", "PF", "FD",
                   "PlusMinus", "PTS"]
    if minutes == "DNP":
        row = {"No": no, "Name": name, "Starter": bool(starter), "DNP": True}
        row.update({k: None for k in STAT_FIELDS})
        return row
    tokens = rest.split()
    if len(tokens) < NUMERIC_TAIL_LEN:
        return None  # malformed / totals row / team-coach row, skip
    tokens = tokens[:NUMERIC_TAIL_LEN]
    (fg_ma, fg_pct, p2_ma, p2_pct, p3_ma, p3_pct, ft_ma, ft_pct,
     orb, drb, tot, ast, tov, stl, blk, pf, fd, plus_minus, pts) = tokens

    def split_ma(tok):
        made, att = tok.split("/")
        return int(made), int(att)

    fgm, fga = split_ma(fg_ma)
    p2m, p2a = split_ma(p2_ma)
    p3m, p3a = split_ma(p3_ma)
    ftm, fta = split_ma(ft_ma)

    return {
        "No": no, "Name": name, "Starter": bool(starter), "DNP": False,
        "Min": mmss_to_minutes(minutes),
        "FGM": fgm, "FGA": fga,
        "2PM": p2m, "2PA": p2a,
        "3PM": p3m, "3PA": p3a,
        "FTM": ftm, "FTA": fta,
        "OREB": int(orb), "DREB": int(drb), "TREB": int(tot),
        "AST": int(ast), "TOV": int(tov), "STL": int(stl), "BLK": int(blk),
        "PF": int(pf), "FD": int(fd),
        "PlusMinus": plus_minus,
        "PTS": int(pts),
    }


def extract_box_score(pdf_path: Path):
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[0]
        text = page.extract_text() or ""
    # strip zero-width / invisible unicode characters that Genius Sports'
    # PDF export sometimes embeds (breaks header/team regexes otherwise)
    text = re.sub(r"[​‌‍﻿]", "", text)

    if "FIBA Box Score" not in text and "Box Score" not in text.split("\n")[0:3].__str__():
        # cheap first check; refine below
        pass
    if "FIBA Box Score" not in text:
        return None  # not a box score report (Line Up Analysis / Player Evaluation / Shot Areas / unrelated)

    date_m = HEADER_DATE_RE.search(text)
    game_date = date_m.group(1) if date_m else None
    game_no_m = GAME_NO_RE.search(text)
    game_no = game_no_m.group(1) if game_no_m else None
    report_gen_m = REPORT_GEN_RE.search(text)
    report_gen = report_gen_m.group(1) if report_gen_m else None

    # quarters actually played: look at the "Scoring by X Minute intervals" block
    # crude but effective: count how many "Q<number>" labels appear in the header block
    header_block = text.split("Coach:")[0]
    quarters = sorted(set(int(q) for q in re.findall(r"\bQ(\d)\b", header_block)))
    num_quarters = max(quarters) if quarters else None

    teams = TEAM_HEADER_RE.findall(text)  # [(full name, abbrev), ...] appears once per team block
    # team blocks are separated by "Coach:" sections; split text there
    blocks = text.split("Coach:")
    rows = []
    current_team_full = None
    current_team_abbr = None
    for block in blocks[1:]:
        # the team header line is the last non-empty line BEFORE "Coach:" i.e. first line of prev block's tail
        pass

    # simpler: iterate line by line, track current team via TEAM_HEADER_RE matches in order
    lines = text.split("\n")
    team_positions = [(i, m.group(1).strip(), m.group(2)) for i, l in enumerate(lines)
                       for m in [TEAM_HEADER_RE.match(l.strip())] if m]

    for idx, (line_no, team_full, team_abbr) in enumerate(team_positions):
        end = team_positions[idx + 1][0] if idx + 1 < len(team_positions) else len(lines)
        for line in lines[line_no + 1:end]:
            parsed = parse_player_line(line)
            if parsed is None:
                continue
            parsed.update({
                "Team": team_full, "TeamAbbr": team_abbr,
                "GameDate": game_date, "GameNo": game_no,
                "ReportGenerated": report_gen, "NumQuarters": num_quarters,
                "SourceFile": pdf_path.name,
            })
            rows.append(parsed)

    return rows


def main(folder: str, out_csv: str):
    folder = Path(folder)
    all_rows = []
    skipped = []
    for pdf_path in sorted(folder.glob("*.pdf")):
        try:
            rows = extract_box_score(pdf_path)
        except Exception as e:
            skipped.append((pdf_path.name, f"ERROR: {e}"))
            continue
        if rows is None:
            skipped.append((pdf_path.name, "not a box score report"))
            continue
        all_rows.extend(rows)

    # dedupe halftime vs final: group by (GameNo, GameDate), keep rows from the
    # source file with the MOST quarters (fallback: latest ReportGenerated)
    from collections import defaultdict
    by_game = defaultdict(list)
    for r in all_rows:
        by_game[(r["GameNo"], r["GameDate"])].append(r)

    final_rows = []
    dedup_log = []
    for key, rows in by_game.items():
        files = {r["SourceFile"]: r["NumQuarters"] for r in rows}
        if len(files) > 1:
            best_file = max(files, key=lambda f: (files[f] or 0))
            dropped = [f for f in files if f != best_file]
            dedup_log.append((key, best_file, dropped))
            rows = [r for r in rows if r["SourceFile"] == best_file]
        final_rows.extend(rows)

    if final_rows:
        fieldnames = []
        for r in final_rows:
            for k in r.keys():
                if k not in fieldnames:
                    fieldnames.append(k)
        with open(out_csv, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=fieldnames)
            w.writeheader()
            w.writerows(final_rows)

    print(f"Parsed {len(final_rows)} player-game rows from {len(list(folder.glob('*.pdf')))} PDFs")
    print(f"Skipped {len(skipped)} non-box-score / errored files:")
    for name, reason in skipped:
        print(f"  - {name}: {reason}")
    if dedup_log:
        print(f"\nDeduped {len(dedup_log)} game(s) with multiple reports (kept the most complete one):")
        for key, kept, dropped in dedup_log:
            print(f"  - Game {key}: kept {kept}, dropped {dropped}")


if __name__ == "__main__":
    folder = sys.argv[1] if len(sys.argv) > 1 else "."
    out = sys.argv[2] if len(sys.argv) > 2 else "box_scores.csv"
    main(folder, out)

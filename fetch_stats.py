"""
NBA Stats Fetcher — pulls current season + career stats via ESPN public API.
ESPN's API works reliably from cloud servers (unlike stats.nba.com which blocks GitHub Actions).
Run: python fetch_stats.py
Output: stats.json (loaded by index.html)
"""
import json
import time
import random
from datetime import datetime

import requests

# ESPN player IDs (found via ESPN search API)
PLAYERS = [
    {"name": "LeBron James",  "espn_id": 1966,    "nba_id": 2544},
    {"name": "Deni Avdija",   "espn_id": 4683021, "nba_id": 1630166},
    {"name": "Stephen Curry", "espn_id": 3975,    "nba_id": 201939},
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
}

ESPN_BASE = "https://site.api.espn.com/apis/common/v3/sports/basketball/nba"
ESPN_WEB  = "https://site.web.api.espn.com/apis/common/v3/sports/basketball/nba"
ESPN_SITE = "https://site.api.espn.com/apis/site/v2/sports/basketball/nba"

MAX_RETRIES = 3
TIMEOUT = 30


def api_get(url):
    """GET with retry + backoff."""
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            r = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            if attempt == MAX_RETRIES:
                raise
            wait = 3 * attempt + random.uniform(1, 3)
            print(f"    [retry {attempt}/{MAX_RETRIES}] {type(e).__name__}: {e}")
            time.sleep(wait)


def fetch_player_stats(player):
    name = player["name"]
    eid = player["espn_id"]
    print(f"  Fetching {name} (ESPN ID: {eid})...")

    # 1. Basic athlete info (bio, current season stats)
    athlete_data = api_get(f"{ESPN_BASE}/athletes/{eid}")
    ath = athlete_data.get("athlete", {})
    time.sleep(1)

    # 2. Game log (all games this season)
    gamelog_data = api_get(f"{ESPN_WEB}/athletes/{eid}/gamelog")
    time.sleep(1)

    # Parse bio
    bio = {
        "height": ath.get("displayHeight", ""),
        "weight": ath.get("displayWeight", "").replace(" lbs", ""),
        "birthdate": ath.get("displayDOB", ""),
        "country": "",
        "draft_year": "",
        "draft_round": "",
        "draft_number": "",
        "years_pro": 0,
    }
    # Parse draft from displayDraft like "2003: Rd 1, Pk 1 (CLE)"
    draft_str = ath.get("displayDraft", "")
    if draft_str and ":" in draft_str:
        bio["draft_year"] = draft_str.split(":")[0].strip()
        if "Rd " in draft_str:
            bio["draft_round"] = draft_str.split("Rd ")[1].split(",")[0].strip()
        if "Pk " in draft_str:
            bio["draft_number"] = draft_str.split("Pk ")[1].split(" ")[0].strip()
    exp_str = ath.get("displayExperience", "")
    if exp_str:
        try:
            bio["years_pro"] = int(exp_str.split("st")[0].split("nd")[0].split("rd")[0].split("th")[0])
        except ValueError:
            pass
    birth_place = ath.get("displayBirthPlace", "")
    if birth_place:
        bio["country"] = birth_place.split(",")[-1].strip() if "," in birth_place else birth_place

    # Parse current season stats from athlete endpoint
    stats_list = ath.get("statistics", [])
    stats_map = {}
    for s in stats_list:
        stats_map[s.get("name", "")] = s.get("value", 0)

    team_info = ath.get("team", {})
    team_abbr = team_info.get("abbreviation", "")

    # Parse gamelog for last game + season totals
    season_types = gamelog_data.get("seasonTypes", [])
    all_events = {}  # eventId -> stats array
    event_order = []  # ordered list of eventIds (most recent first)

    # gamelog labels (column names)
    gl_labels = gamelog_data.get("names", [])

    for st in season_types:
        for cat in st.get("categories", []):
            for ev in cat.get("events", []):
                evid = ev.get("eventId")
                if evid and evid not in all_events:
                    all_events[evid] = ev.get("stats", [])
                    event_order.append(evid)

    # Map label index
    def idx(label):
        try:
            return gl_labels.index(label)
        except ValueError:
            return -1

    i_pts = idx("points")
    i_reb = idx("totalRebounds")
    i_ast = idx("assists")
    i_stl = idx("steals")
    i_blk = idx("blocks")
    i_min = idx("minutes")
    i_fgp = idx("fieldGoalPct")

    def safe_float(stats, index):
        if index < 0 or index >= len(stats):
            return 0
        try:
            return float(stats[index])
        except (ValueError, TypeError):
            return 0

    def safe_int(stats, index):
        return int(safe_float(stats, index))

    # Last game
    last_game = {}
    last_event_id = None
    if event_order:
        last_event_id = event_order[0]
        lg_stats = all_events[last_event_id]
        last_game = {
            "pts": safe_int(lg_stats, i_pts),
            "reb": safe_int(lg_stats, i_reb),
            "ast": safe_int(lg_stats, i_ast),
            "stl": safe_int(lg_stats, i_stl),
            "blk": safe_int(lg_stats, i_blk),
            "min": safe_int(lg_stats, i_min),
            "fg_pct": safe_float(lg_stats, i_fgp),
        }

    # Fetch last game score + matchup from ESPN summary
    if last_event_id:
        try:
            summary = api_get(f"{ESPN_SITE}/summary?event={last_event_id}")
            header = summary.get("header", {})
            competitions = header.get("competitions", [{}])
            comp = competitions[0] if competitions else {}

            competitors = comp.get("competitors", [])
            game_date_str = comp.get("date", "")

            # Parse date
            if game_date_str:
                try:
                    dt = datetime.fromisoformat(game_date_str.replace("Z", "+00:00"))
                    last_game["date"] = dt.strftime("%b %d, %Y")
                except Exception:
                    last_game["date"] = game_date_str[:10]

            # Parse teams + scores
            home_team = away_team = None
            for c in competitors:
                if c.get("homeAway") == "home":
                    home_team = c
                else:
                    away_team = c

            if home_team and away_team:
                home_abbr = home_team.get("team", {}).get("abbreviation", "")
                away_abbr = away_team.get("team", {}).get("abbreviation", "")
                home_score = int(home_team.get("score", "0"))
                away_score = int(away_team.get("score", "0"))

                # Determine matchup string (like "LAL @ PHX" or "LAL vs. PHX")
                if team_abbr == home_abbr:
                    last_game["matchup"] = f"{team_abbr} vs. {away_abbr}"
                    player_won = home_score > away_score
                else:
                    last_game["matchup"] = f"{team_abbr} @ {home_abbr}"
                    player_won = away_score > home_score

                last_game["result"] = "W" if player_won else "L"
                last_game["score"] = {
                    "team1_abbr": away_abbr,
                    "team1_pts": away_score,
                    "team2_abbr": home_abbr,
                    "team2_pts": home_score,
                }

            time.sleep(1)
        except Exception as e:
            print(f"    [!] Could not fetch game summary: {e}")

    # Calculate season totals from gamelog
    total_games = len(all_events)
    total_pts = sum(safe_int(s, i_pts) for s in all_events.values())
    total_reb = sum(safe_int(s, i_reb) for s in all_events.values())
    total_ast = sum(safe_int(s, i_ast) for s in all_events.values())
    total_stl = sum(safe_int(s, i_stl) for s in all_events.values())
    total_blk = sum(safe_int(s, i_blk) for s in all_events.values())

    gp = max(total_games, 1)

    result = {
        "name": name,
        "player_id": player.get("nba_id", eid),
        "bio": bio,
        "current_season": {
            "season": "2025-26",
            "team": team_abbr,
            "gp": total_games,
            "ppg": round(stats_map.get("avgPoints", total_pts / gp), 1),
            "rpg": round(stats_map.get("avgRebounds", total_reb / gp), 1),
            "apg": round(stats_map.get("avgAssists", total_ast / gp), 1),
            "spg": round(total_stl / gp, 1),
            "bpg": round(total_blk / gp, 1),
            "fg_pct": round(stats_map.get("fieldGoalPct", 0), 1),
            "fg3_pct": 0,
            "ft_pct": 0,
            "total_pts": total_pts,
            "total_reb": total_reb,
            "total_ast": total_ast,
        },
        "career": {
            "gp": 0,
            "total_pts": 0,
            "total_reb": 0,
            "total_ast": 0,
            "total_stl": 0,
            "total_blk": 0,
            "ppg": round(stats_map.get("avgPoints", 0), 1),
            "rpg": round(stats_map.get("avgRebounds", 0), 1),
            "apg": round(stats_map.get("avgAssists", 0), 1),
            "fg_pct": round(stats_map.get("fieldGoalPct", 0), 1),
            "seasons": bio["years_pro"],
            "best_season_pts": 0,
            "best_season_reb": 0,
            "best_season_ast": 0,
        },
        "last_game": last_game,
        "season_history": [],
    }

    return result


def main():
    print(f"NBA Stats Fetcher (ESPN) — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 50)

    # Load existing stats as fallback
    existing = {}
    try:
        with open("stats.json", "r", encoding="utf-8") as f:
            existing = json.load(f).get("players", {})
    except Exception:
        pass

    all_stats = {}
    for player in PLAYERS:
        name = player["name"]
        try:
            data = fetch_player_stats(player)
            if data:
                all_stats[name] = data
                print(f"    ✓ {name}: {data['last_game'].get('matchup', '?')} — {data['last_game'].get('pts', '?')} pts")
        except Exception as e:
            print(f"  [!] Failed to fetch {name}: {e}")
            if name in existing:
                print(f"  [*] Keeping previous data for {name}")
                all_stats[name] = existing[name]

    if not all_stats:
        print("\n[!] No data fetched. Keeping old stats.json.")
        return

    output = {
        "last_updated": datetime.now().isoformat(),
        "players": all_stats,
    }

    with open("stats.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\nSaved stats.json ({len(all_stats)} players)")
    print(f"Last updated: {output['last_updated']}")


if __name__ == "__main__":
    main()

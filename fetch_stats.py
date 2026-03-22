"""
NBA Stats Fetcher — pulls current season + career stats for showcase players.
Run: python fetch_stats.py
Output: stats.json (loaded by index.html)
"""
import json
import time
from datetime import datetime

from nba_api.stats.static import players as nba_players
from nba_api.stats.endpoints import (
    playercareerstats,
    commonplayerinfo,
    playergamelog,
    leaguegamelog,
)

# Players to fetch (match the showcase)
PLAYER_NAMES = ["LeBron James", "Deni Avdija", "Stephen Curry"]

# Cache of all league games (loaded once, reused per player)
_all_league_games = None

def get_league_games():
    global _all_league_games
    if _all_league_games is None:
        print("  Loading league game log (once)...")
        lgl = leaguegamelog.LeagueGameLog(season="2025-26")
        games = lgl.get_normalized_dict().get("LeagueGameLog", [])
        # Index by game_id for fast lookup
        _all_league_games = {}
        for g in games:
            gid = g.get("GAME_ID")
            if gid not in _all_league_games:
                _all_league_games[gid] = []
            _all_league_games[gid].append(g)
        time.sleep(1)
    return _all_league_games

def find_player_id(name):
    results = nba_players.find_players_by_full_name(name)
    if results:
        return results[0]["id"]
    return None

def fetch_player_stats(name):
    pid = find_player_id(name)
    if not pid:
        print(f"  [!] Player not found: {name}")
        return None

    print(f"  Fetching {name} (ID: {pid})...")
    time.sleep(1)  # Rate limit

    # Career stats
    career = playercareerstats.PlayerCareerStats(player_id=pid)
    career_data = career.get_normalized_dict()
    time.sleep(1)

    # Player info
    info = commonplayerinfo.CommonPlayerInfo(player_id=pid)
    info_data = info.get_normalized_dict()
    time.sleep(1)

    # Last game log
    gamelog = playergamelog.PlayerGameLog(player_id=pid, season="2025-26")
    gamelog_data = gamelog.get_normalized_dict()
    time.sleep(1)

    # Extract last game
    games = gamelog_data.get("PlayerGameLog", [])
    last_game = games[0] if games else {}

    # Fetch final score from league game log (already loaded)
    game_score = {}
    game_id = last_game.get("Game_ID")
    if game_id:
        try:
            all_games = get_league_games()
            teams_in_game = all_games.get(game_id, [])
            if len(teams_in_game) >= 2:
                t1, t2 = teams_in_game[0], teams_in_game[1]
                game_score = {
                    "team1_abbr": t1.get("TEAM_ABBREVIATION", ""),
                    "team1_pts": t1.get("PTS", 0),
                    "team2_abbr": t2.get("TEAM_ABBREVIATION", ""),
                    "team2_pts": t2.get("PTS", 0),
                }
        except Exception as e:
            print(f"  [!] Could not fetch game score: {e}")

    # Extract current season (last entry in regular season)
    reg_season = career_data.get("SeasonTotalsRegularSeason", [])
    current_season = reg_season[-1] if reg_season else {}

    # Career totals
    career_totals_list = career_data.get("CareerTotalsRegularSeason", [])
    career_totals = career_totals_list[0] if career_totals_list else {}

    # Player bio
    bio = info_data.get("CommonPlayerInfo", [{}])[0] if info_data.get("CommonPlayerInfo") else {}

    # Find season highs from all seasons
    all_seasons_pts = [s.get("PTS", 0) for s in reg_season if s.get("PTS")]
    all_seasons_reb = [s.get("REB", 0) for s in reg_season if s.get("REB")]
    all_seasons_ast = [s.get("AST", 0) for s in reg_season if s.get("AST")]

    # Calculate per-game averages for current season
    gp = current_season.get("GP", 1) or 1

    result = {
        "name": name,
        "player_id": pid,
        "bio": {
            "height": bio.get("HEIGHT", ""),
            "weight": bio.get("WEIGHT", ""),
            "birthdate": bio.get("BIRTHDATE", "")[:10] if bio.get("BIRTHDATE") else "",
            "country": bio.get("COUNTRY", ""),
            "draft_year": bio.get("DRAFT_YEAR", ""),
            "draft_round": bio.get("DRAFT_ROUND", ""),
            "draft_number": bio.get("DRAFT_NUMBER", ""),
            "years_pro": bio.get("SEASON_EXP", 0),
        },
        "current_season": {
            "season": current_season.get("SEASON_ID", ""),
            "team": current_season.get("TEAM_ABBREVIATION", ""),
            "gp": current_season.get("GP", 0),
            "ppg": round(current_season.get("PTS", 0) / gp, 1),
            "rpg": round(current_season.get("REB", 0) / gp, 1),
            "apg": round(current_season.get("AST", 0) / gp, 1),
            "spg": round(current_season.get("STL", 0) / gp, 1),
            "bpg": round(current_season.get("BLK", 0) / gp, 1),
            "fg_pct": round((current_season.get("FG_PCT", 0) or 0) * 100, 1),
            "fg3_pct": round((current_season.get("FG3_PCT", 0) or 0) * 100, 1),
            "ft_pct": round((current_season.get("FT_PCT", 0) or 0) * 100, 1),
            "total_pts": current_season.get("PTS", 0),
            "total_reb": current_season.get("REB", 0),
            "total_ast": current_season.get("AST", 0),
        },
        "career": {
            "gp": career_totals.get("GP", 0),
            "total_pts": career_totals.get("PTS", 0),
            "total_reb": career_totals.get("REB", 0),
            "total_ast": career_totals.get("AST", 0),
            "total_stl": career_totals.get("STL", 0),
            "total_blk": career_totals.get("BLK", 0),
            "ppg": round(career_totals.get("PTS", 0) / max(career_totals.get("GP", 1), 1), 1),
            "rpg": round(career_totals.get("REB", 0) / max(career_totals.get("GP", 1), 1), 1),
            "apg": round(career_totals.get("AST", 0) / max(career_totals.get("GP", 1), 1), 1),
            "fg_pct": round((career_totals.get("FG_PCT", 0) or 0) * 100, 1),
            "seasons": len(reg_season),
            "best_season_pts": max(all_seasons_pts) if all_seasons_pts else 0,
            "best_season_reb": max(all_seasons_reb) if all_seasons_reb else 0,
            "best_season_ast": max(all_seasons_ast) if all_seasons_ast else 0,
        },
        "last_game": {
            "date": last_game.get("GAME_DATE", ""),
            "matchup": last_game.get("MATCHUP", ""),
            "result": last_game.get("WL", ""),
            "pts": last_game.get("PTS", 0),
            "reb": last_game.get("REB", 0),
            "ast": last_game.get("AST", 0),
            "stl": last_game.get("STL", 0),
            "blk": last_game.get("BLK", 0),
            "fg_pct": round((last_game.get("FG_PCT", 0) or 0) * 100, 1),
            "min": last_game.get("MIN", 0),
            "score": game_score,
        } if last_game else {},
        "season_history": [
            {
                "season": s.get("SEASON_ID", ""),
                "team": s.get("TEAM_ABBREVIATION", ""),
                "gp": s.get("GP", 0),
                "ppg": round(s.get("PTS", 0) / max(s.get("GP", 1), 1), 1),
                "rpg": round(s.get("REB", 0) / max(s.get("GP", 1), 1), 1),
                "apg": round(s.get("AST", 0) / max(s.get("GP", 1), 1), 1),
            }
            for s in reg_season[-5:]  # Last 5 seasons
        ],
    }

    return result


def main():
    print(f"NBA Stats Fetcher — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 50)

    all_stats = {}
    for name in PLAYER_NAMES:
        data = fetch_player_stats(name)
        if data:
            all_stats[name] = data

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

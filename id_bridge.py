import os
import pandas as pd
from dotenv import load_dotenv
from tqdm import tqdm
import cfbd

"""
DON'T RUN THIS IF YOU CAN AVOID IT YOU WILL USE UP THE API REQUESTS
Uncomment the load_dotenv() line to use the API.
"""


# load_dotenv()
CFBD_TOKEN = os.getenv("CFBD_TOKEN")
if not CFBD_TOKEN:
    raise ValueError("CFBD_TOKEN is not set")

configuration = cfbd.Configuration(
    host="https://api.collegefootballdata.com"
)
configuration = cfbd.Configuration(
    access_token=CFBD_TOKEN
)

df = pd.read_csv("NFL Data/players_ids.csv")

with cfbd.ApiClient(configuration) as api_client:
    players_api = cfbd.PlayersApi(api_client)
    results = []
    for row in tqdm(df.itertuples(index=False), total=len(df), desc="CFBD player search"):
        search_term = row.display_name
        college_name = getattr(row, "college_name", None)
        try:
            players = players_api.search_players(
                search_term=search_term
            )
        except Exception as e:
            print(f"Search failed for {search_term}: {e}")
            results.append(None)
            continue

        if not players:
            results.append(None)
            continue

        # Prefer matching school when possible; fallback to first result
        match = None
        if college_name:
            for p in players:
                p_dict = p.to_dict()
                if p_dict.get("school") == college_name:
                    match = p_dict
                    break
        if match is None:
            match = players[0].to_dict()

        cfbd_id = (
            match.get("id")
            or match.get("athlete_id")
            or match.get("player_id")
        )
        cfbd_name = (
            match.get("name")
            or f"{match.get('first_name', '')} {match.get('last_name', '')}".strip()
            or None
        )
        results.append(cfbd_id)

df["cfbd_id"] = results
df.to_csv("NFL Data/player_ids.csv", index=False)
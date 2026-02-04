import os
import pandas as pd
from dotenv import load_dotenv
from tqdm import tqdm
import cfbd 

load_dotenv()
CFBD_TOKEN = os.getenv("CFBD_TOKEN")
if not CFBD_TOKEN:
    raise ValueError("CFBD_TOKEN is not set")

configuration = cfbd.Configuration(
    host = "https://api.collegefootballdata.com"
)
configuration = cfbd.Configuration(
    access_token = CFBD_TOKEN
)

def fetch_draft_picks(year: int) -> pd.DataFrame:
    with cfbd.ApiClient(configuration) as api_client:
        draft_api = cfbd.DraftApi(api_client)
        try:
            picks = draft_api.get_draft_picks(year=year) 
            # print("The response of DraftApi->get_draft_picks:\n")
            # print(picks)
        except Exception as e:
            print("Exception when calling DraftApi->get_draft_picks: %s\n" % e)
        
    df = pd.DataFrame([p.to_dict() for p in picks])
    df["year"] = year
    return df


def fetch_receiving_stats(year: int) -> pd.DataFrame:
    with cfbd.ApiClient(configuration) as api_client:
        stats_api = cfbd.StatsApi(api_client)
        try:
            receiving = stats_api.get_player_season_stats(year=year)
        except Exception as e:
            print("Exception when calling ReceivingApi->get_receiving_stats: %s\n" % e)
    df = pd.DataFrame([r.to_dict() for r in receiving])
    df["year"] = year
    return df
    

draft_years = list(range(2013,2026)) 
stat_years = list(range(2009,2026)) 


# DRAFT DATA

def run_draft_collection(year):
    draft = fetch_draft_picks(year)
    draft_wr = draft[draft["position"]=="Wide Receiver"].copy()

    draft_wr = draft_wr[
        ["year", "overall", "round", "pick", "name",
        "collegeTeam", "collegeConference", "nflTeam",
        "collegeAthleteId", "nflAthleteId"]
    ]
    print("Drafted WR rows:", len(draft_wr))
    draft_wr.to_csv(f"Data/Raw/draft_wr_{year}.csv", index=False)


# SEASON LONG RECEIVING DATA

def run_receiving_collection(year):
    receiving_stats = fetch_receiving_stats(year)
    receiving_wr = receiving_stats[(receiving_stats["position"]=="WR") & (receiving_stats["category"]=="receiving")].copy()

    print("Receiving WR rows:", len(receiving_wr))
    # receiving_wr.to_csv(f"Data/Raw/receiving_wr_{year}.csv", index=False)
    receiving_stats.to_csv(f"Data/Raw/Test/TEST_receiving_wr_{year}.csv", index=False)


def run


# RUN

# for year in draft_years:
#     run_draft_collection(year)
# for year in stat_years:
run_receiving_collection(2024)

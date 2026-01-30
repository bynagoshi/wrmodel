import pandas as pd

df = pd.read_csv("Data/Raw/Combined/receiving_wr_2009_2025.csv")

# CHECK IF ANY DUPLICATES

dupes = df.duplicated(
    subset=["season", "playerId", "statType"],
    keep=False
)

assert not dupes.any(), "Duplicates detected uh oh"

# TURN FROM LONG TO WIDE

wide = (
    df
    .pivot_table(
        index=["player", "playerId", "season", "team", "conference"],
        columns="statType",
        values="stat",
        aggfunc="first"
    )
    .reset_index()
)

# wide.to_csv("Data/Processed/receiving_wr_2009_2025_wide.csv", index=False)
# wide.to_csv("Data/Processed/receiving_wr_2009_2025_wide.parquet", index=False)



by_player = wide.copy()
by_player["season_rank_desc"] = by_player.groupby("playerId")["season"].rank(method="first", ascending=False)

by_player = by_player[by_player["season_rank_desc"] <= 3].drop(columns="season_rank_desc")
by_player = by_player.sort_values(["player", "playerId", "season"], ascending=[True, True, True]).reset_index(drop=True)

by_player.to_csv("Data/Processed/receiving_wr_2009_2025_by_playerv2.csv", index=False)
# by_player.to_csv("Data/Processed/receiving_wr_2009_2025_by_player.parquet", index=False)


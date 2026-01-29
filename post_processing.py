import pandas as pd

df = pd.read_csv("Data/Raw/receiving_wr_2008_2009.csv")

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
        index=["season", "playerId", "player", "team", "conference"],
        columns="statType",
        values="stat",
        aggfunc="first"
    )
    .reset_index()
)

wide.to_csv("Data/Processed/receiving_wr_2008_2009_wide.csv", index=False)



by_player = (
    wide.pivot_table(
        index=["playerId", "player"],
        columns="season",
        values=["LONG", "REC", "TD", "YDS", "YPR"],
        aggfunc="first"
    )
)

by_player.columns = [f"{stat}_{season}" for stat, season in by_player.columns]
by_player = by_player.reset_index()
print(by_player.head())
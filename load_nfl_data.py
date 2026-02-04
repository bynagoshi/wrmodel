import polars as pl
import nflreadpy as nfl

pbp = nfl.load_pbp(seasons = 2024)
nfl_players = nfl.load_players()

# pbp = nfl.load_pbp(seasons=range(2013, 2025))
# rosters = nfl.load_rosters(seasons=range(2013, 2025))


wr_pbp = (
    pbp
    .filter(
        (pl.col("play_type") == "pass") &
        (pl.col("receiver_player_id").is_not_null())
    )
)
wr_season_stats = (
    wr_pbp
    .group_by(["receiver_player_id", "season"])
    .agg([
        # REC: count completed passes to the receiver
        pl.col("complete_pass").sum().alias("REC"),

        # YDS / TDs
        pl.col("receiving_yards").sum().alias("YDS"),
        # Receiving TDs (PBP uses pass_touchdown for passing plays)
        pl.col("pass_touchdown").sum().alias("TDs"),

        # LONG: longest single reception (max receiving yards on a play)
        pl.col("receiving_yards").max().alias("LONG"),
    ])
    .with_columns([
        # YPR = YDS / REC
        (pl.col("YDS") / pl.col("REC"))
            .fill_nan(0)
            .fill_null(0)
            .alias("YPR")
    ])
    .sort(["receiver_player_id", "season"])
)

nfl_players_ids = (
    nfl_players
    .select(["gsis_id", "nfl_id", "display_name", "college_name", "birth_date"])
    .with_columns(
        pl.col("nfl_id").cast(pl.Int64, strict=False).alias("nfl_id_int")
    )
    .drop("nfl_id")
)

nfl_players_ids = nfl_players_ids.filter(
    (pl.col("birth_date") > "1990-01-01") &
    (pl.col('nfl_id_int').is_not_null())
)

# SEND TO CSV

nfl_players_ids.write_csv("NFL Data/players_ids.csv")

# wr_season_stats.write_csv("Data/NFL Data/nfl_wr_season_stats.csv")
pbp.write_csv("NFL Data/nfl_pbp.csv")
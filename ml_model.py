import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.ensemble import RandomForestRegressor


DATA_PATH = "Data/Processed/combined_wr_2013_2025.csv"
TARGET_COL = "overall"  # draft position (lower is better)


def aggregate_player_stats(df: pd.DataFrame) -> pd.DataFrame:
    # Keep only pre-draft seasons (defensive guard)
    df = df[df["season"] <= (df["year"] - 1)].copy()

    # Ensure numeric stats
    stat_cols = ["REC", "YDS", "TD", "YPR", "LONG"]
    df[stat_cols] = df[stat_cols].apply(pd.to_numeric, errors="coerce")

    # Career aggregates
    agg = (
        df.groupby(["collegeAthleteId", "name", "year", "overall"], as_index=False)
        .agg(
            career_rec=("REC", "sum"),
            career_yds=("YDS", "sum"),
            career_td=("TD", "sum"),
            career_ypr=("YPR", "mean"),
            career_long=("LONG", "max"),
            seasons_played=("season", "nunique"),
            last_season=("season", "max"),
        )
    )

    # Last-season stats
    last_season_stats = (
        df.sort_values("season")
        .groupby(["collegeAthleteId", "name"], as_index=False)
        .tail(1)[["collegeAthleteId", "name", "REC", "YDS", "TD", "YPR", "LONG"]]
        .rename(
            columns={
                "REC": "last_rec",
                "YDS": "last_yds",
                "TD": "last_td",
                "YPR": "last_ypr",
                "LONG": "last_long",
            }
        )
    )

    out = agg.merge(last_season_stats, on=["collegeAthleteId", "name"], how="left")
    return out


def main() -> None:
    df = pd.read_csv(DATA_PATH)
    features_df = aggregate_player_stats(df)

    # Basic feature set
    feature_cols = [
        "career_rec",
        "career_yds",
        "career_td",
        "career_ypr",
        "career_long",
        "seasons_played",
        "last_rec",
        "last_yds",
        "last_td",
        "last_ypr",
        "last_long",
    ]

    # Drop rows missing target
    features_df = features_df.dropna(subset=[TARGET_COL])
    X = features_df[feature_cols].fillna(0)
    y = features_df[TARGET_COL]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestRegressor(
        n_estimators=300,
        random_state=42,
        n_jobs=-1,
    )
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    mae = mean_absolute_error(y_test, preds)
    rmse = mean_squared_error(y_test, preds, squared=False)
    r2 = r2_score(y_test, preds)

    print(f"MAE: {mae:.2f}")
    print(f"RMSE: {rmse:.2f}")
    print(f"R2: {r2:.3f}")


if __name__ == "__main__":
    main()


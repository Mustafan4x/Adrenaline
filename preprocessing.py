"""
UFC Data Preprocessing Pipeline
Handles data cleaning, feature engineering, combat style classification,
and difference matrix creation for matchup prediction.
"""

import os
from datetime import datetime

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")


def classify_combat_style(row: pd.Series) -> str:
    """
    Classify a fighter's combat style based on their stats.
    Categories: Striker, Grappler, Aggressive, Passive, All-Rounder
    """
    slpm = row.get("slpm", 0) or 0
    td_avg = row.get("td_avg", 0) or 0
    sub_avg = row.get("sub_avg", 0) or 0
    str_acc = row.get("str_acc", 0) or 0
    td_acc = row.get("td_acc", 0) or 0
    sapm = row.get("sapm", 0) or 0

    grappling_score = td_avg * 2 + sub_avg * 3 + (td_acc * 2 if td_acc else 0)
    striking_score = slpm * 1.5 + (str_acc * 3 if str_acc else 0)

    # Aggressive: high output on both ends
    if slpm > 4.5 and sapm > 4.0:
        return "Aggressive"

    # Passive: low output
    if slpm < 2.5 and td_avg < 1.0 and sub_avg < 0.5:
        return "Passive"

    # Grappler: wrestling/submission focused
    if grappling_score > striking_score * 1.3:
        return "Grappler"

    # Striker: stand-up focused
    if striking_score > grappling_score * 1.3:
        return "Striker"

    return "All-Rounder"


def compute_age(dob: str, reference_date: str = None) -> float | None:
    """Compute age from date of birth."""
    if pd.isna(dob) or not dob:
        return None
    try:
        birth = datetime.strptime(str(dob), "%Y-%m-%d")
        ref = datetime.strptime(reference_date, "%Y-%m-%d") if reference_date else datetime.now()
        age = (ref - birth).days / 365.25
        return round(age, 1)
    except (ValueError, TypeError):
        return None


def compute_win_streak(fights_df: pd.DataFrame, fighter_name: str) -> int:
    """Compute current win streak for a fighter from fight history."""
    fighter_fights = fights_df[
        (fights_df["fighter_a"] == fighter_name) | (fights_df["fighter_b"] == fighter_name)
    ].copy()

    streak = 0
    for _, fight in fighter_fights.iterrows():
        if fight.get("winner") == fighter_name:
            streak += 1
        else:
            break
    return streak


def compute_recent_form(fights_df: pd.DataFrame, fighter_name: str, n: int = 5) -> dict:
    """Compute stats weighted toward a fighter's last N fights.

    Returns recent win rate, recent finish rate, and a momentum score
    that captures whether the fighter is trending up or down.
    """
    fighter_fights = fights_df[
        (fights_df["fighter_a"] == fighter_name) | (fights_df["fighter_b"] == fighter_name)
    ].copy()

    recent = fighter_fights.head(n)
    if len(recent) == 0:
        return {"recent_win_rate": 0.5, "recent_finish_rate": 0.0, "momentum": 0.0}

    wins = 0
    finishes = 0
    # Weighted momentum: most recent fights count more
    momentum = 0.0
    for i, (_, fight) in enumerate(recent.iterrows()):
        weight = (n - i) / n  # 1.0 for most recent, decreasing
        won = fight.get("winner") == fighter_name
        if won:
            wins += 1
            momentum += weight
            method = str(fight.get("method", "")).strip().upper()
            method_clean = " ".join(method.split())
            if method_clean.startswith("KO") or method_clean.startswith("SUB"):
                finishes += 1
        else:
            momentum -= weight

    total = len(recent)
    return {
        "recent_win_rate": wins / total,
        "recent_finish_rate": finishes / total,
        "momentum": momentum / n,  # normalized to [-1, 1]
    }


def compute_opponent_quality(fights_df: pd.DataFrame, fighters_df: pd.DataFrame, fighter_name: str, n: int = 5) -> float:
    """Compute average win rate of a fighter's recent opponents.

    A fighter who has beaten high win-rate opponents is stronger than one
    who beat low win-rate opponents.
    """
    fighter_fights = fights_df[
        (fights_df["fighter_a"] == fighter_name) | (fights_df["fighter_b"] == fighter_name)
    ].head(n)

    if len(fighter_fights) == 0:
        return 0.5

    opponent_win_rates = []
    for _, fight in fighter_fights.iterrows():
        opponent = fight["fighter_b"] if fight["fighter_a"] == fighter_name else fight["fighter_a"]
        opp_row = fighters_df[fighters_df["name"].str.lower().str.strip() == opponent.lower().strip()]
        if len(opp_row) > 0:
            opp = opp_row.iloc[0]
            total = opp.get("wins", 0) + opp.get("losses", 0) + opp.get("draws", 0)
            if total > 0:
                opponent_win_rates.append(opp["wins"] / total)

    return np.mean(opponent_win_rates) if opponent_win_rates else 0.5


def compute_finish_rates(fights_df: pd.DataFrame, fighter_name: str) -> dict:
    """Compute KO rate, submission rate, and decision rate from fight history."""
    fighter_wins = fights_df[fights_df["winner"] == fighter_name]

    total_wins = len(fighter_wins)
    if total_wins == 0:
        return {"ko_rate": 0.0, "sub_rate": 0.0, "dec_rate": 0.0}

    ko_wins = 0
    sub_wins = 0
    dec_wins = 0
    for _, fight in fighter_wins.iterrows():
        method = " ".join(str(fight.get("method", "")).split()).upper()
        if method.startswith("KO") or method.startswith("TKO"):
            ko_wins += 1
        elif method.startswith("SUB"):
            sub_wins += 1
        else:
            dec_wins += 1

    return {
        "ko_rate": ko_wins / total_wins,
        "sub_rate": sub_wins / total_wins,
        "dec_rate": dec_wins / total_wins,
    }


# Weight class encoding (heavier = higher value, women's divisions offset)
WEIGHT_CLASS_ORDER = {
    "Women's Strawweight": 1, "Women's Flyweight": 2, "Women's Bantamweight": 3,
    "Women's Featherweight": 4, "Flyweight": 5, "Bantamweight": 6,
    "Featherweight": 7, "Lightweight": 8, "Welterweight": 9,
    "Middleweight": 10, "Light Heavyweight": 11, "Heavyweight": 12,
    "Catch Weight": 7,  # default to mid-range
}


def impute_reach(df: pd.DataFrame) -> pd.DataFrame:
    """Impute missing reach data using height correlation."""
    df = df.copy()
    mask = df["reach_cm"].isna() & df["height_cm"].notna()
    if mask.any() and df["reach_cm"].notna().sum() > 10:
        # Reach is typically ~1.04x height
        valid = df[df["reach_cm"].notna() & df["height_cm"].notna()]
        if len(valid) > 0:
            ratio = (valid["reach_cm"] / valid["height_cm"]).median()
            df.loc[mask, "reach_cm"] = df.loc[mask, "height_cm"] * ratio
    # Fill remaining with median
    if df["reach_cm"].isna().any():
        df["reach_cm"] = df["reach_cm"].fillna(df["reach_cm"].median())
    return df


def clean_fighter_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and prepare fighter data."""
    df = df.copy()

    # Compute age
    df["age"] = df["dob"].apply(compute_age)

    # Impute reach
    df = impute_reach(df)

    # Fill missing numeric columns with median
    numeric_cols = ["height_cm", "weight_kg", "reach_cm", "age",
                    "slpm", "str_acc", "sapm", "str_def",
                    "td_avg", "td_acc", "td_def", "sub_avg"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
            df[col] = df[col].fillna(df[col].median())

    # Fill missing record values
    for col in ["wins", "losses", "draws"]:
        if col in df.columns:
            df[col] = df[col].fillna(0).astype(int)

    # Compute derived features
    df["total_fights"] = df["wins"] + df["losses"] + df["draws"]
    df["win_rate"] = df.apply(
        lambda r: r["wins"] / r["total_fights"] if r["total_fights"] > 0 else 0.5, axis=1
    )

    # Classify combat style
    df["combat_style"] = df.apply(classify_combat_style, axis=1)

    return df


def create_feature_vector(fighter: pd.Series) -> dict:
    """Create a feature dictionary for a single fighter."""
    features = {
        "height_cm": fighter.get("height_cm", 0),
        "weight_kg": fighter.get("weight_kg", 0),
        "reach_cm": fighter.get("reach_cm", 0),
        "age": fighter.get("age", 30),
        "wins": fighter.get("wins", 0),
        "losses": fighter.get("losses", 0),
        "draws": fighter.get("draws", 0),
        "total_fights": fighter.get("total_fights", 0),
        "win_rate": fighter.get("win_rate", 0.5),
        "slpm": fighter.get("slpm", 0),
        "str_acc": fighter.get("str_acc", 0),
        "sapm": fighter.get("sapm", 0),
        "str_def": fighter.get("str_def", 0),
        "td_avg": fighter.get("td_avg", 0),
        "td_acc": fighter.get("td_acc", 0),
        "td_def": fighter.get("td_def", 0),
        "sub_avg": fighter.get("sub_avg", 0),
        "win_streak": fighter.get("win_streak", 0),
        # Recent form features
        "recent_win_rate": fighter.get("recent_win_rate", 0.5),
        "recent_finish_rate": fighter.get("recent_finish_rate", 0.0),
        "momentum": fighter.get("momentum", 0.0),
        # Opponent quality
        "opponent_quality": fighter.get("opponent_quality", 0.5),
        # Finish rates
        "ko_rate": fighter.get("ko_rate", 0.0),
        "sub_rate": fighter.get("sub_rate", 0.0),
        "dec_rate": fighter.get("dec_rate", 0.0),
        # Weight class tier
        "weight_class_tier": fighter.get("weight_class_tier", 7),
        # One-hot encoded combat style
        "style_striker": 1 if fighter.get("combat_style") == "Striker" else 0,
        "style_grappler": 1 if fighter.get("combat_style") == "Grappler" else 0,
        "style_aggressive": 1 if fighter.get("combat_style") == "Aggressive" else 0,
        "style_passive": 1 if fighter.get("combat_style") == "Passive" else 0,
        "style_all_rounder": 1 if fighter.get("combat_style") == "All-Rounder" else 0,
    }
    return features


FEATURE_COLUMNS = [
    "height_cm", "weight_kg", "reach_cm", "age",
    "wins", "losses", "draws", "total_fights", "win_rate",
    "slpm", "str_acc", "sapm", "str_def",
    "td_avg", "td_acc", "td_def", "sub_avg",
    "win_streak",
    "recent_win_rate", "recent_finish_rate", "momentum",
    "opponent_quality",
    "ko_rate", "sub_rate", "dec_rate",
    "weight_class_tier",
    "style_striker", "style_grappler", "style_aggressive",
    "style_passive", "style_all_rounder"
]


def create_difference_matrix(fighter_a: pd.Series, fighter_b: pd.Series) -> np.ndarray:
    """
    Create the difference matrix (X_A - X_B) for a matchup.
    Returns a 1D array of feature differences.
    """
    feats_a = create_feature_vector(fighter_a)
    feats_b = create_feature_vector(fighter_b)

    diff = []
    for col in FEATURE_COLUMNS:
        val_a = feats_a.get(col, 0) or 0
        val_b = feats_b.get(col, 0) or 0
        diff.append(float(val_a) - float(val_b))

    return np.array(diff).reshape(1, -1)


def enrich_fighters(fighters_df: pd.DataFrame, fights_df: pd.DataFrame) -> pd.DataFrame:
    """Add derived features (recent form, opponent quality, finish rates) to fighter data."""
    fighters_df = fighters_df.copy()

    # Pre-compute weight class tier from most common weight class in fights
    fighter_weight_classes = {}
    for _, fight in fights_df.iterrows():
        wc = fight.get("weight_class", "")
        for name in [fight.get("fighter_a", ""), fight.get("fighter_b", "")]:
            if name:
                fighter_weight_classes.setdefault(name, []).append(wc)

    for idx, row in fighters_df.iterrows():
        name = row.get("name", "")

        # Recent form
        form = compute_recent_form(fights_df, name)
        fighters_df.at[idx, "recent_win_rate"] = form["recent_win_rate"]
        fighters_df.at[idx, "recent_finish_rate"] = form["recent_finish_rate"]
        fighters_df.at[idx, "momentum"] = form["momentum"]

        # Opponent quality
        fighters_df.at[idx, "opponent_quality"] = compute_opponent_quality(
            fights_df, fighters_df, name
        )

        # Finish rates
        rates = compute_finish_rates(fights_df, name)
        fighters_df.at[idx, "ko_rate"] = rates["ko_rate"]
        fighters_df.at[idx, "sub_rate"] = rates["sub_rate"]
        fighters_df.at[idx, "dec_rate"] = rates["dec_rate"]

        # Weight class tier
        wc_list = fighter_weight_classes.get(name, [])
        if wc_list:
            # Most frequent weight class
            most_common = max(set(wc_list), key=wc_list.count)
            fighters_df.at[idx, "weight_class_tier"] = WEIGHT_CLASS_ORDER.get(most_common, 7)
        else:
            fighters_df.at[idx, "weight_class_tier"] = 7

    return fighters_df


def build_training_data(fighters_df: pd.DataFrame, fights_df: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]:
    """
    Build training data from historical fights.
    Returns X (difference matrices) and y (1 if fighter_a won, 0 if fighter_b won).
    """
    fighters_df = clean_fighter_data(fighters_df)
    fighters_df = enrich_fighters(fighters_df, fights_df)

    # Create a lookup dict
    fighter_lookup = {}
    for _, row in fighters_df.iterrows():
        name = row.get("name", "").strip()
        if name:
            fighter_lookup[name.lower()] = row

    rng = np.random.RandomState(42)

    X_list = []
    y_list = []

    for _, fight in fights_df.iterrows():
        fa_name = str(fight.get("fighter_a", "")).strip().lower()
        fb_name = str(fight.get("fighter_b", "")).strip().lower()
        winner = fight.get("winner")

        if not winner or fa_name not in fighter_lookup or fb_name not in fighter_lookup:
            continue

        fa = fighter_lookup[fa_name]
        fb = fighter_lookup[fb_name]
        winner_lower = str(winner).strip().lower()

        # Randomly swap fighter order to prevent positional bias
        # (UFCStats always lists winner first as fighter_a)
        if rng.random() < 0.5:
            fa, fb = fb, fa
            fa_name, fb_name = fb_name, fa_name

        diff = create_difference_matrix(fa, fb)
        label = 1 if winner_lower == fa_name else 0

        X_list.append(diff.flatten())
        y_list.append(label)

    if not X_list:
        return np.array([]), np.array([])

    X = np.array(X_list)
    y = np.array(y_list)

    return X, y


def get_fighter_by_name(fighters_df: pd.DataFrame, name: str) -> pd.Series | None:
    """Look up a fighter by name (case-insensitive, partial match)."""
    name_lower = name.strip().lower()
    # Exact match first
    exact = fighters_df[fighters_df["name"].str.lower().str.strip() == name_lower]
    if len(exact) > 0:
        return exact.iloc[0]

    # Partial match
    partial = fighters_df[fighters_df["name"].str.lower().str.contains(name_lower, na=False)]
    if len(partial) > 0:
        return partial.iloc[0]

    return None


def get_style_matchup_description(style_a: str, style_b: str) -> str:
    """Get a description of how two styles typically match up."""
    matchups = {
        ("Striker", "Grappler"): "Classic striker vs grappler matchup. The striker needs to keep distance and avoid takedowns. The grappler will try to close distance and take the fight to the ground.",
        ("Striker", "Striker"): "Stand-up war likely. Striking accuracy and defense will be key differentiators.",
        ("Grappler", "Grappler"): "Wrestling-heavy fight expected. The better chain wrestler or submission artist has the edge.",
        ("Aggressive", "Passive"): "Aggressive fighter will push the pace. The counter-striker needs to time shots and avoid getting overwhelmed.",
        ("Aggressive", "Aggressive"): "Fireworks expected! Both fighters will push forward, likely resulting in an exciting but risky fight for both.",
        ("All-Rounder", "Striker"): "The all-rounder can choose where the fight goes. They may try to exploit the striker's takedown defense.",
        ("All-Rounder", "Grappler"): "The all-rounder has options to keep it standing or match grappling. Versatility is the advantage.",
        ("All-Rounder", "All-Rounder"): "Evenly matched in style versatility. This fight will likely be decided by who executes their game plan better.",
    }
    key1 = (style_a, style_b)
    key2 = (style_b, style_a)
    if key1 in matchups:
        return matchups[key1]
    elif key2 in matchups:
        return matchups[key2]
    return f"{style_a} vs {style_b}: Unique style matchup with multiple possible game plans."

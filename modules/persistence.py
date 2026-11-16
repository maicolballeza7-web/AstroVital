from pathlib import Path

import pandas as pd

from .assessment import HealthAssessment


ASSESSMENT_COLUMNS = [
    "recorded_at",
    "source",
    "heart_rate",
    "systolic_bp",
    "diastolic_bp",
    "body_temperature",
    "blood_glucose",
    "sleep_hours",
    "stress_level",
    "physical_activity",
    "mood",
]


def load_assessments(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame(columns=ASSESSMENT_COLUMNS)

    try:
        frame = pd.read_csv(path)
    except (OSError, pd.errors.EmptyDataError, pd.errors.ParserError) as error:
        raise RuntimeError(f"Unable to read assessment history: {error}") from error

    missing_columns = set(ASSESSMENT_COLUMNS) - set(frame.columns)
    if missing_columns:
        raise RuntimeError(
            "Assessment history is missing columns: "
            + ", ".join(sorted(missing_columns))
        )

    frame = frame[ASSESSMENT_COLUMNS].copy()
    frame["recorded_at"] = pd.to_datetime(frame["recorded_at"], errors="coerce", utc=True)
    for column in ASSESSMENT_COLUMNS[2:]:
        frame[column] = pd.to_numeric(frame[column], errors="coerce")
    return frame.dropna(subset=["recorded_at"]).sort_values("recorded_at").reset_index(
        drop=True
    )


def save_assessment(path: Path, assessment: HealthAssessment) -> pd.DataFrame:
    assessment_path = path
    assessment_path.parent.mkdir(parents=True, exist_ok=True)
    history = load_assessments(assessment_path)
    new_row = pd.DataFrame([assessment.with_timestamp().to_record()])
    updated = pd.concat([history, new_row], ignore_index=True)
    updated["recorded_at"] = pd.to_datetime(updated["recorded_at"], utc=True)
    updated = updated[ASSESSMENT_COLUMNS].sort_values("recorded_at").reset_index(drop=True)
    try:
        updated.to_csv(assessment_path, index=False)
    except OSError as error:
        raise RuntimeError(f"Unable to save assessment history: {error}") from error
    return updated

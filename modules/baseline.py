from dataclasses import dataclass

import pandas as pd


BASELINE_FIELDS = [
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


@dataclass(frozen=True)
class BaselineResult:
    values: dict[str, float]
    record_count: int
    minimum_records: int

    @property
    def reliable(self) -> bool:
        return self.record_count >= self.minimum_records


def calculate_personal_baseline(
    history: pd.DataFrame, minimum_records: int = 3
) -> BaselineResult:
    numeric_history = history.copy()
    for field in BASELINE_FIELDS:
        if field not in numeric_history:
            numeric_history[field] = pd.NA
        numeric_history[field] = pd.to_numeric(numeric_history[field], errors="coerce")

    values = {
        field: float(numeric_history[field].dropna().mean())
        for field in BASELINE_FIELDS
        if numeric_history[field].notna().any()
    }
    return BaselineResult(values, len(history), minimum_records)


def compare_to_baseline(
    current: dict[str, float | None], baseline: BaselineResult
) -> dict[str, float]:
    if not baseline.reliable:
        return {}

    deviations: dict[str, float] = {}
    for field, value in current.items():
        reference = baseline.values.get(field)
        if value is not None and reference not in (None, 0):
            deviations[field] = ((float(value) - reference) / abs(reference)) * 100
    return deviations

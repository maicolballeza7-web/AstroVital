from dataclasses import dataclass

import pandas as pd

from .assessment import HealthAssessment, INDICATOR_LABELS
from .baseline import BaselineResult, compare_to_baseline


@dataclass(frozen=True)
class HealthInsight:
    indicator: str
    severity: str
    value: str
    reference: str
    explanation: str
    reason: str
    action: str


def _format_value(value: float | None) -> str:
    return "Not recorded" if value is None else f"{value:.1f}"


def generate_insights(
    history: pd.DataFrame,
    current: HealthAssessment,
    baseline: BaselineResult,
) -> list[HealthInsight]:
    insights: list[HealthInsight] = []
    current_values = {
        field: getattr(current, field)
        for field in INDICATOR_LABELS
    }
    deviations = compare_to_baseline(current_values, baseline)

    if not baseline.reliable:
        insights.append(
            HealthInsight(
                "Personal baseline",
                "INFO",
                f"{baseline.record_count} records",
                f"{baseline.minimum_records} required",
                "The personal reference is not reliable yet.",
                "More consistent user-entered assessments are needed before comparing trends.",
                "Continue recording complete assessments.",
            )
        )
    else:
        for field, deviation in deviations.items():
            if abs(deviation) < 15:
                continue
            direction = "above" if deviation > 0 else "below"
            label = INDICATOR_LABELS[field]
            insights.append(
                HealthInsight(
                    label,
                    "WATCH",
                    _format_value(current_values[field]),
                    f"{baseline.values[field]:.1f} ({deviation:+.1f}%)",
                    f"{label} is {direction} the personal reference.",
                    "This is a deviation from the individual's recent pattern, not a diagnosis.",
                    "Repeat the measurement and review the next assessment.",
                )
            )

    if len(history) >= 3:
        recent = history.sort_values("recorded_at").tail(3)
        for field, label in (
            ("heart_rate", "Heart Rate"),
            ("sleep_hours", "Sleep Hours"),
            ("mood", "Mood"),
        ):
            values = pd.to_numeric(recent[field], errors="coerce").dropna().tolist()
            if len(values) == 3 and (
                values[0] < values[1] < values[2] or values[0] > values[1] > values[2]
            ):
                insights.append(
                    HealthInsight(
                        label,
                        "TREND",
                        _format_value(values[-1]),
                        "Last 3 records",
                        f"{label} shows a consistent directional change.",
                        "A repeated pattern deserves review; it does not establish a medical cause.",
                        "Continue monitoring and discuss persistent changes with the mission medical team.",
                    )
                )

    return insights

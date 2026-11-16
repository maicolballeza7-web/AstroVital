from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True)
class HealthAssessment:
    """One user-entered health assessment.

    Validation bounds protect data quality for this prototype. They are not
    universal clinical reference ranges and do not provide a diagnosis.
    """

    recorded_at: str | None = None
    source: str = "user"
    heart_rate: float | None = None
    systolic_bp: float | None = None
    diastolic_bp: float | None = None
    body_temperature: float | None = None
    blood_glucose: float | None = None
    sleep_hours: float | None = None
    stress_level: float | None = None
    physical_activity: float | None = None
    mood: float | None = None

    def with_timestamp(self) -> "HealthAssessment":
        if self.recorded_at:
            return self
        return HealthAssessment(
            recorded_at=datetime.now(timezone.utc).isoformat(),
            source=self.source,
            heart_rate=self.heart_rate,
            systolic_bp=self.systolic_bp,
            diastolic_bp=self.diastolic_bp,
            body_temperature=self.body_temperature,
            blood_glucose=self.blood_glucose,
            sleep_hours=self.sleep_hours,
            stress_level=self.stress_level,
            physical_activity=self.physical_activity,
            mood=self.mood,
        )

    def to_record(self) -> dict[str, Any]:
        return asdict(self.with_timestamp())


INDICATOR_LABELS = {
    "heart_rate": "Heart Rate",
    "systolic_bp": "Systolic Blood Pressure",
    "diastolic_bp": "Diastolic Blood Pressure",
    "body_temperature": "Body Temperature",
    "blood_glucose": "Blood Glucose",
    "sleep_hours": "Sleep Hours",
    "stress_level": "Stress Level",
    "physical_activity": "Physical Activity",
    "mood": "Mood",
}

VALIDATION_BOUNDS = {
    "heart_rate": (30, 220),
    "systolic_bp": (60, 250),
    "diastolic_bp": (30, 150),
    "body_temperature": (30, 45),
    "blood_glucose": (40, 400),
    "sleep_hours": (0, 24),
    "stress_level": (1, 10),
    "physical_activity": (0, 240),
    "mood": (1, 10),
}


def validate_assessment(assessment: HealthAssessment) -> list[str]:
    errors: list[str] = []
    for field_name, (minimum, maximum) in VALIDATION_BOUNDS.items():
        value = getattr(assessment, field_name)
        if value is not None and not minimum <= value <= maximum:
            label = INDICATOR_LABELS[field_name]
            errors.append(f"{label} must be between {minimum} and {maximum}.")

    if (assessment.systolic_bp is None) != (assessment.diastolic_bp is None):
        errors.append("Systolic and diastolic blood pressure must be entered together.")

    return errors


def missing_indicators(assessment: HealthAssessment) -> list[str]:
    return [
        label
        for field_name, label in INDICATOR_LABELS.items()
        if getattr(assessment, field_name) is None
    ]


def get_health_status(assessment: HealthAssessment) -> str:
    if (
        assessment.heart_rate is not None
        and assessment.heart_rate > 100
        or assessment.sleep_hours is not None
        and assessment.sleep_hours < 6
        or assessment.stress_level is not None
        and assessment.stress_level > 7
    ):
        return "🔴 HIGH RISK"

    if (
        assessment.heart_rate is not None
        and assessment.heart_rate > 90
        or assessment.sleep_hours is not None
        and assessment.sleep_hours < 7
        or assessment.stress_level is not None
        and assessment.stress_level > 5
    ):
        return "🟡 CAUTION"

    return "🟢 OPTIMAL"


def calculate_readiness_score(assessment: HealthAssessment) -> int:
    score = 100

    if assessment.heart_rate is not None:
        if assessment.heart_rate > 100:
            score -= 30
        elif assessment.heart_rate > 90:
            score -= 15

    if assessment.sleep_hours is not None:
        if assessment.sleep_hours < 6:
            score -= 25
        elif assessment.sleep_hours < 7:
            score -= 10

    if assessment.stress_level is not None:
        if assessment.stress_level > 7:
            score -= 25
        elif assessment.stress_level > 5:
            score -= 10

    if assessment.physical_activity is not None and assessment.physical_activity < 15:
        score -= 15
    if assessment.mood is not None and assessment.mood < 4:
        score -= 15

    return max(0, int(score))


def get_recommendation(status: str) -> str:
    recommendations = {
        "🔴 HIGH RISK": "Repeat concerning measurements and contact the mission medical team.",
        "🟡 CAUTION": "Review rest, hydration, and measurement quality; monitor the next reading.",
        "🟢 OPTIMAL": "Continue your routine and record measurements consistently.",
    }
    return recommendations[status]

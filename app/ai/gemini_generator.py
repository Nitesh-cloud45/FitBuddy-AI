from ..config import get_settings
from .gemini_client import generate_text


def demo_plan(
    username: str,
    age: int,
    weight: float,
    goal: str,
    intensity: str,
) -> str:
    return f"""
FITBUDDY 7-DAY FITNESS PLAN
User: {username}
Age: {age}
Weight: {weight} kg
Goal: {goal}
Intensity: {intensity}

DAY 1 — FULL BODY STRENGTH
• Bodyweight Squat — 3 sets × 8–12 reps
• Incline Push-up — 3 sets × 8–12 reps
• Seated Row / Band Row — 3 sets × 10–12 reps

DAY 2 — CARDIO + MOBILITY
• Brisk walk or easy cycling — 20–30 minutes
• Hip mobility — 5 minutes
• Shoulder mobility — 5 minutes

DAY 3 — UPPER BODY
• Dumbbell Press — 3 sets × 8–12 reps
• Lat Pulldown — 3 sets × 8–12 reps
• Light Biceps Curl — 2 sets × 10–15 reps

DAY 4 — RECOVERY
• Easy walk
• Gentle mobility
• Prioritize sleep and hydration

DAY 5 — LOWER BODY + CORE
• Leg Press or Squat — 3 sets × 8–12 reps
• Hip Hinge — 3 sets × 8–12 reps
• Dead Bug — 3 sets × 8 reps per side

DAY 6 — MIXED CONDITIONING
• Easy/moderate cardio
• Step-ups
• Mobility work

DAY 7 — REST
• Complete rest or optional easy activity

GENERAL GUIDELINES
• Start each workout with a gentle warm-up.
• Finish with a cooldown.
• Use controlled movements and appropriate resistance.
• Take rest when needed.
• Stop exercising if you experience pain, dizziness, or unusual symptoms.
"""


def generate_workout_gemini(
    username: str,
    age: int,
    weight: float,
    goal: str,
    intensity: str,
) -> str:
    settings = get_settings()

    if not settings.use_gemini:
        return demo_plan(
            username=username,
            age=age,
            weight=weight,
            goal=goal,
            intensity=intensity,
        )

    prompt = f"""
You are FitBuddy, an AI fitness assistant.

Create a beginner-friendly 7-day fitness plan.

User information:
Name: {username}
Age: {age}
Weight: {weight} kg
Goal: {goal}
Intensity: {intensity}

Requirements:
- Create exactly 7 days.
- Include exercises, sets, reps, or durations.
- Include a warm-up.
- Include a cooldown/recovery section.
- Include at least one rest or recovery day.
- Keep the plan beginner-friendly.
- Do not recommend unsafe exercises.
- Do not recommend extreme dieting.
- Do not recommend dehydration.
- Do not diagnose medical conditions.
- Do not provide medical treatment.
- Tell the user to stop if they experience pain, dizziness,
  or unusual symptoms.
"""

    return generate_text(
        prompt,
        settings.workout_model
    )
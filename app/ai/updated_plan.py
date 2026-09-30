from ..config import get_settings
from .gemini_client import generate_text


def update_workout_plan(
    original_plan: str,
    feedback: str,
    goal: str,
    intensity: str,
) -> str:
    settings = get_settings()

    if not settings.use_gemini:
        return f"""
UPDATED USING USER FEEDBACK

Original fitness goal: {goal}
Intensity: {intensity}

USER FEEDBACK:
{feedback}

UPDATED PLAN:

The plan has been adjusted based on your feedback.

1. Keep the exercises that feel comfortable.
2. Reduce intensity or volume if the previous plan felt too difficult.
3. Take additional recovery time when needed.
4. Continue with warm-ups and cooldowns.
5. Keep at least one recovery/rest day each week.

SAFETY:
Stop exercising if you experience pain, dizziness, or unusual symptoms.

ORIGINAL PLAN:
{original_plan}
"""

    prompt = f"""
You are FitBuddy, an AI fitness assistant.

The user has an existing 7-day fitness plan and has provided feedback.
Create an updated version of the plan based on that feedback.

FITNESS GOAL:
{goal}

INTENSITY:
{intensity}

ORIGINAL PLAN:
{original_plan}

USER FEEDBACK:
{feedback}

Requirements:
- Revise all 7 days of the plan.
- Directly address the user's feedback.
- Keep the plan beginner-friendly.
- Include exercises with sets, reps, or durations.
- Include warm-up guidance.
- Include cooldown/recovery guidance.
- Keep at least one rest or recovery day.
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
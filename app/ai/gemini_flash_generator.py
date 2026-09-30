from ..config import get_settings
from .gemini_client import generate_text


def demo_tip(goal: str) -> str:
    tips = {
        "weight loss": (
            "Focus on balanced meals with vegetables, fruits, whole grains, "
            "and protein-rich foods. Stay hydrated and avoid extreme calorie "
            "restriction. Consistent sleep and regular activity also support "
            "healthy progress."
        ),
        "muscle gain": (
            "Include regular protein-rich foods such as eggs, dairy, beans, "
            "lentils, fish, chicken, or other suitable protein sources. "
            "Combine balanced meals with resistance training and adequate sleep."
        ),
        "general wellness": (
            "Aim for balanced meals containing vegetables, fruits, whole "
            "grains, protein, and healthy fats. Drink enough water and maintain "
            "regular physical activity and sleep."
        ),
        "flexibility": (
            "Support mobility training with balanced meals, enough fluids, "
            "and adequate recovery. Include gentle stretching and avoid forcing "
            "movements into painful ranges."
        ),
    }

    return tips.get(
        goal,
        "Focus on balanced nutrition, hydration, regular activity, and adequate recovery."
    )


def generate_nutrition_tip_with_flash(goal: str) -> str:
    settings = get_settings()

    if not settings.use_gemini:
        return demo_tip(goal)

    prompt = f"""
You are FitBuddy, an AI fitness assistant.

The user's fitness goal is: {goal}

Provide a short nutrition and recovery recommendation.

Requirements:
- Give 2 to 4 sentences.
- Recommend balanced nutrition.
- Mention hydration and recovery where useful.
- Do not recommend extreme dieting.
- Do not recommend fasting or dehydration.
- Do not diagnose medical conditions.
- Do not prescribe medical treatment.
- Keep the advice practical and beginner-friendly.
"""

    return generate_text(
        prompt,
        settings.nutrition_model
    )
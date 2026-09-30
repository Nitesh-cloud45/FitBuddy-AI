from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


Goal = Literal[
    "weight loss",
    "muscle gain",
    "general wellness",
    "flexibility",
]

Intensity = Literal[
    "low",
    "medium",
    "high",
]


class UserInput(BaseModel):
    username: str = Field(
        min_length=2,
        max_length=100
    )

    user_id: str = Field(
        min_length=2,
        max_length=64,
        pattern=r"^[A-Za-z0-9_-]+$"
    )

    age: int = Field(
        ge=18,
        le=100
    )

    weight: float = Field(
        gt=20,
        le=500
    )

    goal: Goal

    intensity: Intensity

    @field_validator("username")
    @classmethod
    def clean_username(cls, value: str):
        value = " ".join(value.split())

        if not value:
            raise ValueError("Name cannot be empty")

        return value


class FeedbackRequest(BaseModel):
    user_id: str = Field(
        min_length=2,
        max_length=64
    )

    feedback: str = Field(
        min_length=3,
        max_length=2000
    )


class UserResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    user_id: str
    username: str
    age: int
    weight: float
    goal: str
    intensity: str


class PlanResponse(BaseModel):
    user: UserResponse
    original_plan: str
    updated_plan: str | None
    nutrition_tip: str
    feedback: str | None
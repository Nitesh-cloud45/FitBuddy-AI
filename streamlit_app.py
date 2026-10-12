
import streamlit as st

st.set_page_config(
    page_title="FitBuddy AI",
    page_icon="💪",
    layout="centered"
)

st.title("💪 FitBuddy AI")
st.subheader("Your fitness journey, powered by AI.")

st.write(
    "Create a structured 7-day workout plan based on "
    "your fitness goals and preferred workout intensity."
)

st.divider()
st.header("Your Details")

with st.form("fitbuddy_form"):
    username = st.text_input("Name", placeholder="Alex")
    user_id = st.text_input("User ID", placeholder="U001")

    col1, col2 = st.columns(2)

    with col1:
        age = st.number_input(
            "Age",
            min_value=18,
            max_value=100,
            value=25
        )

    with col2:
        weight = st.number_input(
            "Weight (kg)",
            min_value=20.0,
            max_value=500.0,
            value=70.0,
            step=0.1
        )

    goal = st.selectbox(
        "Fitness Goal",
        [
            "Weight Loss",
            "Muscle Gain",
            "General Wellness",
            "Flexibility"
        ]
    )

    intensity = st.selectbox(
        "Workout Intensity",
        ["Low", "Medium", "High"],
        index=1
    )

    submitted = st.form_submit_button(
        "Generate 7-Day Plan",
        type="primary",
        use_container_width=True
    )

if submitted:
    if not username.strip() or not user_id.strip():
        st.error("Please enter your name and user ID.")

    else:
        st.success(f"Welcome, {username}!")

        st.write(f"**Age:** {age}")
        st.write(f"**Weight:** {weight} kg")
        st.write(f"**Goal:** {goal}")
        st.write(f"**Intensity:** {intensity}")

        st.header("Your 7-Day Workout Plan")

        if intensity == "Low":
            workouts = [
                "Walking and gentle stretching",
                "Light full-body exercises",
                "Walking and mobility",
                "Active recovery",
                "Gentle strength training",
                "Easy cardio",
                "Rest and stretching"
            ]

        elif intensity == "Medium":
            workouts = [
                "Full-body strength training",
                "Moderate cardio",
                "Lower-body workout",
                "Active recovery and mobility",
                "Upper-body workout",
                "Cardio and core exercises",
                "Rest and stretching"
            ]

        else:
            workouts = [
                "Full-body strength training",
                "Cardio intervals",
                "Lower-body strength training",
                "Active recovery",
                "Upper-body strength training",
                "Conditioning workout",
                "Rest and mobility"
            ]

        for day, workout in enumerate(workouts, start=1):
            with st.container(border=True):
                st.markdown(f"### Day {day}")
                st.write(workout)

        st.header("Nutrition & Recovery Tip")

        tips = {
            "Weight Loss":
                "Focus on balanced meals, sustainable activity, "
                "adequate sleep, and gradual progress.",

            "Muscle Gain":
                "Include protein-rich foods, progressive strength "
                "training, and sufficient recovery.",

            "General Wellness":
                "Stay active, eat balanced meals, drink enough water, "
                "and maintain a consistent sleep schedule.",

            "Flexibility":
                "Practice gentle stretching consistently without "
                "forcing painful movements."
        }

        st.info(tips[goal])

        st.caption(
            "This is a starter workout template, not an AI-generated "
            "or medically personalized prescription. Adjust activities "
            "to your fitness level."
        )

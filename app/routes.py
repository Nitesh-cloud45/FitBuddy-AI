from fastapi import (
    APIRouter,
    Depends,
    Form,
    HTTPException,
    Query,
    Request,
    status,
)

router = APIRouter()

from fastapi.responses import (
    HTMLResponse,
    RedirectResponse,
)

from fastapi.templating import (
    Jinja2Templates,
)

from sqlalchemy import select
from fastapi.responses import (
    HTMLResponse,
    RedirectResponse
)

from fastapi.templating import (
    Jinja2Templates
)

from sqlalchemy import select

from sqlalchemy.orm import Session


from .ai.gemini_flash_generator import (
    generate_nutrition_tip_with_flash
)

from .ai.gemini_generator import (
    generate_workout_gemini
)

from .ai.updated_plan import (
    update_workout_plan
)

from .config import get_settings

from .database import get_db

from .models import (
    Plan,
    User
)

from .schemas import (
    FeedbackRequest,
    UserInput
)


router = APIRouter()


templates = Jinja2Templates(
    directory="templates"
)


def get_plan(
    db: Session,
    user_id: str
):

    return db.scalar(

        select(Plan)

        .where(
            Plan.user_id == user_id
        )

        .order_by(
            Plan.id.desc()
        )
    )


def result_context(
    user,
    plan,
    message=None
):

    return {

        "user": user,

        "plan": plan,

        "message": message
    }


# --------------------------------
# HOME
# --------------------------------

@router.get(
    "/",
    response_class=HTMLResponse
)
def home(request: Request):

    return templates.TemplateResponse(

        request=request,

        name="index.html",

        context={
            "error": None
        }
    )


# --------------------------------
# GENERATE WORKOUT
# --------------------------------

@router.post(
    "/generate-workout",
    response_class=HTMLResponse
)
def generate_workout_form(

    request: Request,

    username: str = Form(...),

    user_id: str = Form(...),

    age: int = Form(...),

    weight: float = Form(...),

    goal: str = Form(...),

    intensity: str = Form(...),

    db: Session = Depends(get_db)

):

    try:

        payload = UserInput(

            username=username,

            user_id=user_id,

            age=age,

            weight=weight,

            goal=goal,

            intensity=intensity
        )

    except Exception as exc:

        return templates.TemplateResponse(

            request=request,

            name="index.html",

            context={
                "error": str(exc)
            },

            status_code=422
        )


    existing = db.scalar(

        select(User)

        .where(
            User.user_id == payload.user_id
        )
    )


    if existing:

        return templates.TemplateResponse(

            request=request,

            name="index.html",

            context={
                "error":
                    f"User ID '{payload.user_id}' "
                    "already exists."
            },

            status_code=409
        )


    try:

        workout = generate_workout_gemini(

            payload.username,

            payload.age,

            payload.weight,

            payload.goal,

            payload.intensity
        )


        tip = generate_nutrition_tip_with_flash(

            payload.goal
        )


    except Exception as exc:

        return templates.TemplateResponse(

            request=request,

            name="index.html",

            context={
                "error":
                    f"AI generation failed: {exc}"
            },

            status_code=502
        )


    user = User(

        **payload.model_dump()
    )


    plan = Plan(

        user_id=payload.user_id,

        original_plan=workout,

        nutrition_tip=tip
    )


    db.add(user)

    db.add(plan)

    db.commit()

    db.refresh(user)

    db.refresh(plan)


    return templates.TemplateResponse(

        request=request,

        name="result.html",

        context=result_context(
            user,
            plan
        )
    )


# --------------------------------
# FEEDBACK
# --------------------------------

@router.post(
    "/submit-feedback",
    response_class=HTMLResponse
)
def submit_feedback_form(

    request: Request,

    user_id: str = Form(...),

    feedback: str = Form(...),

    db: Session = Depends(get_db)

):

    try:

        payload = FeedbackRequest(

            user_id=user_id,

            feedback=feedback
        )

    except Exception as exc:

        raise HTTPException(
            status_code=422,
            detail=str(exc)
        )


    user = db.scalar(

        select(User)

        .where(
            User.user_id == payload.user_id
        )
    )


    plan = get_plan(
        db,
        payload.user_id
    )


    if not user or not plan:

        raise HTTPException(
            status_code=404,
            detail="User or plan not found."
        )


    try:

        updated = update_workout_plan(

            plan.original_plan,

            payload.feedback,

            user.goal,

            user.intensity
        )


    except Exception as exc:

        return templates.TemplateResponse(

            request=request,

            name="result.html",

            context=result_context(

                user,

                plan,

                f"Could not update plan: {exc}"
            ),

            status_code=502
        )


    plan.updated_plan = updated

    plan.feedback = payload.feedback


    db.commit()

    db.refresh(plan)


    return templates.TemplateResponse(

        request=request,

        name="result.html",

        context=result_context(

            user,

            plan,

            "Your plan was updated successfully."
        )
    )


# --------------------------------
# ADMIN PAGE
# --------------------------------

@router.get(
    "/view-all-users",
    response_class=HTMLResponse
)
def view_all_users(

    request: Request,

    key: str = Query(default=""),

    db: Session = Depends(get_db)
):

    settings = get_settings()


    if key != settings.admin_key:

        raise HTTPException(
            status_code=403,
            detail="Invalid admin key."
        )


    users = db.scalars(

        select(User)

        .order_by(
            User.id.desc()
        )
    ).all()


    plans = {

        plan.user_id: plan

        for plan in db.scalars(
            select(Plan)
        ).all()
    }


    return templates.TemplateResponse(

        request=request,

        name="all_users.html",

        context={

            "users": users,

            "plans": plans,

            "admin_key": key
        }
    )


# --------------------------------
# DELETE USER
# --------------------------------

@router.post(
    "/admin/users/{user_id}/delete"
)
def delete_user(

    user_id: str,

    key: str = Form(...),

    db: Session = Depends(get_db)
):

    settings = get_settings()


    if key != settings.admin_key:

        raise HTTPException(
            status_code=403,
            detail="Invalid admin key."
        )


    user = db.scalar(

        select(User)

        .where(
            User.user_id == user_id
        )
    )


    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found."
        )


    plans = db.scalars(

        select(Plan)

        .where(
            Plan.user_id == user_id
        )
    ).all()


    for plan in plans:

        db.delete(plan)


    db.delete(user)

    db.commit()


    return RedirectResponse(

        url=f"/view-all-users?key={key}",

        status_code=status.HTTP_303_SEE_OTHER
    )


# --------------------------------
# API CREATE USER
# --------------------------------

@router.post(
    "/api/users"
)
def api_create_user(

    payload: UserInput,

    db: Session = Depends(get_db)
):

    existing = db.scalar(

        select(User)

        .where(
            User.user_id == payload.user_id
        )
    )


    if existing:

        raise HTTPException(
            status_code=409,
            detail="User ID already exists."
        )


    try:

        workout = generate_workout_gemini(

            payload.username,

            payload.age,

            payload.weight,

            payload.goal,

            payload.intensity
        )


        tip = generate_nutrition_tip_with_flash(

            payload.goal
        )


    except Exception as exc:

        raise HTTPException(

            status_code=502,

            detail=f"AI generation failed: {exc}"
        )


    user = User(
        **payload.model_dump()
    )


    plan = Plan(

        user_id=payload.user_id,

        original_plan=workout,

        nutrition_tip=tip
    )


    db.add(user)

    db.add(plan)

    db.commit()

    db.refresh(user)

    db.refresh(plan)


    return {

        "user": user,

        "original_plan":
            plan.original_plan,

        "updated_plan":
            plan.updated_plan,

        "nutrition_tip":
            plan.nutrition_tip,

        "feedback":
            plan.feedback
    }


# --------------------------------
# API FEEDBACK
# --------------------------------

@router.post(
    "/api/feedback"
)
def api_feedback(

    payload: FeedbackRequest,

    db: Session = Depends(get_db)
):

    user = db.scalar(

        select(User)

        .where(
            User.user_id == payload.user_id
        )
    )


    plan = get_plan(
        db,
        payload.user_id
    )


    if not user or not plan:

        raise HTTPException(
            status_code=404,
            detail="User or plan not found."
        )


    try:

        updated = update_workout_plan(

            plan.original_plan,

            payload.feedback,

            user.goal,

            user.intensity
        )


    except Exception as exc:

        raise HTTPException(

            status_code=502,

            detail=f"AI update failed: {exc}"
        )


    plan.updated_plan = updated

    plan.feedback = payload.feedback


    db.commit()

    db.refresh(plan)


    return {

        "user_id":
            user.user_id,

        "updated_plan":
            plan.updated_plan,

        "feedback":
            plan.feedback
    }


# --------------------------------
# API USERS
# --------------------------------

@router.get(
    "/api/users"
)
def api_users(

    key: str = Query(default=""),

    db: Session = Depends(get_db)
):

    settings = get_settings()


    if key != settings.admin_key:

        raise HTTPException(
            status_code=403,
            detail="Invalid admin key."
        )


    users = db.scalars(

        select(User)

        .order_by(
            User.id.desc()
        )
    ).all()


    result = []


    for user in users:

        plan = get_plan(
            db,
            user.user_id
        )


        result.append({

            "user": user,

            "original_plan":
                plan.original_plan
                if plan else None,

            "updated_plan":
                plan.updated_plan
                if plan else None,

            "feedback":
                plan.feedback
                if plan else None
        })


    return result
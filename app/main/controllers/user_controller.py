from datetime import timedelta, datetime
from typing import Any

from fastapi import APIRouter, Depends, Body, HTTPException
from sqlalchemy.orm import Session

from app.main.core.dependencies import get_db, TokenRequired
from app.main import schemas, crud, models
from app.main.core.i18n import __
from app.main.core.security import create_access_token, generate_code, get_password_hash
from app.main.core.config import Config
from app.main.core import mail

router = APIRouter(prefix="", tags=["authentication"])

@router.post("/register", response_model=schemas.Msg)
async def register(
    db: Session = Depends(get_db),
    *,
    user_in: schemas.UserCreate,
    current_user: models.User = Depends(TokenRequired(roles =["ADMIN"]))

):
    if current_user.is_active == False:
        raise HTTPException(status_code=403, detail=__("account-not-active"))
    if current_user.is_deleted == True:
        raise HTTPException(status_code=403, detail=__("account-deleted"))
    exist_phone = crud.user.get_user_by_phone_number(db,phone_number=user_in.phone_number)
    if exist_phone:
        raise HTTPException(status_code=400, detail=__(key="phone-number-already-exists"))
    exist_email = crud.user.get_user_by_email(db, email=user_in.email)
    if exist_email:
        raise HTTPException(status_code=400, detail=__(key="email-already-exists"))
    crud.user.create_user(db=db,user_in=user_in)
    return schemas.Msg(message=__(key="user-created-successfully"))

@router.post("/login",response_model=schemas.UserAuthentication)
async def login(
        db: Session = Depends(get_db),
        *,
        user_in: schemas.UserLogin
) -> Any:
    """
    Sign in with phone number and password
    """
    user = crud.user.authenticate(
        db=db,
        email=user_in.email,
        password=user_in.password
    )
    if not user:
        raise HTTPException(status_code=400, detail=__("auth-login-failed"))
    
    if user.is_active==False:
        raise HTTPException(status_code=400, detail=__("account-not-active"))
    if user.is_deleted==True:
        raise HTTPException(status_code=400, detail=__("account-deleted"))

    access_token_expires = timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "user": user,
        "token": {
            "access_token": create_access_token(
                user.uuid, expires_delta=access_token_expires
            ),
            "token_type": "bearer",
        }
    }

@router.post("/password-recovery/{email}", response_model=schemas.Msg)
def recover_password(email: str, db: Session = Depends(get_db)) -> Any:
    user = crud.user.get_user_by_email(db, email=email)
    if not user:
        raise HTTPException(status_code=400, detail=__("user-not-found"))
    
    # Générer un code de réinitialisation
    code = generate_code(6)  # Code de réinitialisation à 6 chiffres
    print(f"Code de réinitialisation pour {email}: {code}")

    # Enregistrer le code et la date d'envoi dans la base de données
    user.reset_password_code = code
    user.reset_code_sent_at = datetime.utcnow()
    
    # Sauvegarder dans la base de données
    db.commit()
    db.refresh(user)

    # Envoie du code par email via Mailtrap
    mail.send_reset_password_email(email, code, user.first_name)

    return schemas.Msg(message=__(key="recover-password-email-success"))

@router.post("/reset-password/", response_model=schemas.Msg)
def reset_password(
    code: str = Body(...),
    email: str = Body(...),
    new_password: str = Body(...),
    db: Session = Depends(get_db),
) -> Any:
    """
    Reset password
    """

    # Get related user by email
    user = crud.user.get_user_by_email(db=db, email=email)
    if not user:
        raise HTTPException(status_code=400, detail=__("user-not-found"))
    
    # Check if the reset code is correct
    if user.reset_password_code != code:
        raise HTTPException(status_code=400, detail=__("invalid-code"))

    # Check if the code has expired (24 hours)
    if user.reset_code_sent_at and datetime.utcnow() - user.reset_code_sent_at > timedelta(hours=24):
        raise HTTPException(status_code=400, detail=__("code-expired"))
    # Hash the new password
    hashed_password = get_password_hash(new_password)
    user.password_hash = hashed_password

    # Clear the reset code after password reset
    user.reset_password_code = None
    user.reset_code_sent_at = None

    # Save the new password in the database
    db.commit()
    db.refresh(user)

    return schemas.Msg(message=__(key="password-update-success"))


@router.get("/me", summary="Get current user", response_model=schemas.UserDetail)
def get_current_user(
        current_user: models.User = Depends(TokenRequired()),
        db: Session = Depends(get_db),
) -> models.User:
    """
    Get current user
    """
    return current_user

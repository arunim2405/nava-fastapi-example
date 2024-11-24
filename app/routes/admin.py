from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import sessionmaker
from jose import JWTError, jwt
from .. import schemas, db, utils, models
from sqlalchemy.orm import Session

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.post("/login")
def admin_login(payload: schemas.LoginRequest, master_db: Session = Depends(db.get_master_db)):
    # Retrieve organization dynamic DB URL
    org = master_db.query(models.MasterDatabase).filter_by(organization_name=payload.organization_name).first()
    if not org:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found")

    # Connect to dynamic DB and verify admin credentials
    dynamic_session = sessionmaker(bind=db.create_engine(org.dynamic_db_url))()
    admin_user = dynamic_session.query(models.AdminUser).filter_by(email=payload.email).first()
    if not admin_user or not utils.verify_password(payload.password, admin_user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    # Generate JWT Token
    access_token = utils.create_access_token(data={"sub": payload.email})
    return {"access_token": access_token, "token_type": "bearer"}

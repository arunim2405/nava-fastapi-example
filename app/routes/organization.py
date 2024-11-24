from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, models, db, utils

router = APIRouter(prefix="/org", tags=["Organization"])

@router.post("/create", status_code=201)
def create_organization(payload: schemas.CreateOrganizationRequest, master_db: Session = Depends(db.get_master_db)):
    org_name = payload.organization_name
    dynamic_db_url = f"sqlite:///./{org_name}.db"

    # Create Dynamic DB
    dynamic_engine = db.create_engine(dynamic_db_url)
    models.Base.metadata.create_all(bind=dynamic_engine)

    # Hash admin password
    hashed_password = utils.hash_password(payload.password)

    # Add admin user to the dynamic DB
    dynamic_session = db.sessionmaker(bind=dynamic_engine)()
    dynamic_session.add(models.AdminUser(email=payload.email, password=hashed_password, organization_name=org_name))
    dynamic_session.commit()

    # Store Dynamic DB info in Master DB
    master_db.add(models.MasterDatabase(organization_name=org_name, dynamic_db_url=dynamic_db_url))
    master_db.commit()

    return {"message": "Organization created successfully"}

@router.get("/get", response_model=schemas.OrganizationResponse)
def get_organization(organization_name: str, master_db: Session = Depends(db.get_master_db)):
    org = master_db.query(models.MasterDatabase).filter_by(organization_name=organization_name).first()
    if not org:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found")
    return org
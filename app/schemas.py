from pydantic import BaseModel


class CreateOrganizationRequest(BaseModel):
    email: str
    password: str
    organization_name: str


class LoginRequest(BaseModel):
    email: str
    password: str
    organization_name: str


class OrganizationResponse(BaseModel):
    organization_name: str
    dynamic_db_url: str

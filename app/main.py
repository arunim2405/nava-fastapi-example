from fastapi import FastAPI
from .routes import organization, admin

app = FastAPI(title="Organization Management API")

app.include_router(organization.router)
app.include_router(admin.router)
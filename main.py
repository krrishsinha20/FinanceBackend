from fastapi import FastAPI
from database import engine, Base
from routes import auth, users, records, dashboard

# create all tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Finance Data Processing and Access Control API",
    description="""
    A backend system for managing financial records with role-based access control.
    
    ## Roles
    - **Viewer** - Can view records and basic summary
    - **Analyst** - Can view records, summary, category wise and monthly trends
    - **Admin** - Full access including create, update, delete records and manage users
    
    ## How to use
    1. Register a user via /auth/register
    2. Login via Authorise button in the right with your **username as your gmail** and password while ignoring and keeping    the client_id and client_secret as empty
    3. Access endpoints based on your role
    """,
    version="1.0.0"
)

# include all routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(records.router)
app.include_router(dashboard.router)

@app.get("/", tags=["Root"])
def root():
    return {
        "message": "Finance API is running",
        "docs": "/docs",
        "version": "1.0.0"
    }
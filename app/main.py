# Import FastAPI, your Base from database, and your router from routes
from fastapi import FastAPI
from app.database import Base, engine
from app.routes import router

# Create the FastAPI app with a title and description
app = FastAPI(title="txguard", description="A reliable way to rate the trust of merchants.")
# Call Base.metadata.create_all(engine) to create your database tables on startup
Base.metadata.create_all(bind=engine)

# Register your router with app.include_router(router)
app.include_router(router)

# Add a /health endpoint that just returns {"status": "ok"}
@app.get("/health")
def health():
    return {"status": "ok"}

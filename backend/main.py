import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import course, lecturer, classes, dss

app = FastAPI(title="DSS-IT4341 API", version="1.0.0")

raw_origins = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173")
origins = [origin.strip() for origin in raw_origins.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(course.router, prefix="/api/courses", tags=["Courses"])
app.include_router(lecturer.router, prefix="/api/lecturers", tags=["Lecturers"])
app.include_router(classes.router, prefix="/api/classes", tags=["Classes"])
app.include_router(dss.router)

@app.get("/")
def root():
    return {"message": "DSS-IT4341 Backend is running"}
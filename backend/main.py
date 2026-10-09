from fastapi import FastAPI
from database.connection import engine, Base
from routers import course, lecturer, classes, dss # Import thêm dss

Base.metadata.create_all(bind=engine)

app = FastAPI(title="SoICT Scheduler API")

app.include_router(course.router)
app.include_router(lecturer.router)
app.include_router(classes.router)
app.include_router(dss.router) # Đăng ký API DSS

@app.get("/")
def root():
    return {"message": "Hệ thống DSS SoICT đã sẵn sàng!"}
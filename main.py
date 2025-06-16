from fastapi import FastAPI, APIRouter, HTTPException, Depends, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from config import collection
from database.schemas import all_tasks
from database.models import Todo
from bson.objectid import ObjectId
from datetime import datetime

app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router = APIRouter()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = datetime.now()
    response = await call_next(request)
    duration = (datetime.now() - start_time).total_seconds()
    print(f"{request.method} {request.url.path} completed in {duration}s")
    return response

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": f"Internal Server Error: {str(exc)}"}
    )

@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_todos():
    data = collection.find({"is_deleted": False})
    return all_tasks(data)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_task(new_task: Todo):
    try:
        resp = collection.insert_one(dict(new_task))
        return {"message": "Task created", "id": str(resp.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Some error occurred: {e}")

@router.put("/{task_id}", status_code=status.HTTP_200_OK)
async def update_task(task_id: str, updated_task: Todo):
    try:
        id = ObjectId(task_id)
        existing_doc = collection.find_one({"_id": id, "is_deleted": False})
        if not existing_doc:
            raise HTTPException(status_code=404, detail="Task does not exist")
        updated_task.updated_at = datetime.timestamp(datetime.now())
        collection.update_one({"_id": id}, {"$set": dict(updated_task)})
        return {"message": "Task updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Some error occurred: {e}")

@router.delete("/{task_id}", status_code=status.HTTP_200_OK)
async def delete_task(task_id: str):
    try:
        id = ObjectId(task_id)
        existing_doc = collection.find_one({"_id": id, "is_deleted": False})
        if not existing_doc:
            raise HTTPException(status_code=404, detail="Task does not exist")
        collection.update_one({"_id": id}, {"$set": {"is_deleted": True}})
        return {"message": "Task deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Some error occurred: {e}")

app.include_router(router)
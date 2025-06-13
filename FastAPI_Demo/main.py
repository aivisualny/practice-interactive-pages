from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="할 일 관리 API", description="간단한 할 일 관리 API입니다.")

# 할 일 모델 정의
class Todo(BaseModel):
    id: Optional[int] = None
    title: str
    completed: bool = False

# 임시 데이터베이스 (메모리에 저장)
todos = []
current_id = 1

@app.get("/")
async def root():
    return {"message": "할 일 관리 API에 오신 것을 환영합니다!"}

@app.get("/todos", response_model=List[Todo])
async def get_todos():
    return todos

@app.post("/todos", response_model=Todo)
async def create_todo(todo: Todo):
    global current_id
    todo.id = current_id
    current_id += 1
    todos.append(todo)
    return todo

@app.get("/todos/{todo_id}", response_model=Todo)
async def get_todo(todo_id: int):
    for todo in todos:
        if todo.id == todo_id:
            return todo
    raise HTTPException(status_code=404, detail="할 일을 찾을 수 없습니다")

@app.put("/todos/{todo_id}", response_model=Todo)
async def update_todo(todo_id: int, updated_todo: Todo):
    for i, todo in enumerate(todos):
        if todo.id == todo_id:
            updated_todo.id = todo_id
            todos[i] = updated_todo
            return updated_todo
    raise HTTPException(status_code=404, detail="할 일을 찾을 수 없습니다")

@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int):
    for i, todo in enumerate(todos):
        if todo.id == todo_id:
            todos.pop(i)
            return {"message": "할 일이 삭제되었습니다"}
    raise HTTPException(status_code=404, detail="할 일을 찾을 수 없습니다") 
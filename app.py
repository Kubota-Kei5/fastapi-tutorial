from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict
from firestore import db

app = FastAPI()

# CORSミドルウェアを追加
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")


class UserData(BaseModel):
    first: str = Field(..., max_length=50, description="First name of the user")
    last: str = Field(..., max_length=50, description="Last name of the user")
    born: int = Field(..., ge=1000, le=3000, description="Birth year")

# すべてのユーザーを取得
@app.get("/")
def get_users():
    users_ref = db.collection("users")
    docs = users_ref.stream()
    results = {}
    for doc in docs:
        results[doc.id] = doc.to_dict()
    return results


# 特定のユーザーを取得
@app.get("/{user_id}")
def get_user(user_id: str):
    doc_ref = db.collection("users").document(user_id)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict()
    else:
        return {"error": "User not found"}

# ユーザーを追加
@app.post("/")
def create_user(data: Dict[str, UserData]):
    if not data:
        return {"error": "No data provided"}
    
    # 最初のキー(=ドキュメントID)と値(=ドキュメント内容)を取得
    doc_name = list(data.keys())[0]     # 例: "alovelace"
    doc_value = data[doc_name]          # 例: {"born":1815, "first":"Ada", "last":"Lovelace"}

    doc_ref = db.collection("users").document(doc_name)
    doc_ref.set(doc_value)

    return {
        "message": f"User '{doc_name}' created successfully.",
        "data": doc_value
    }

@app.delete("/{user_id}")
def delete_user(user_id: str):
    doc_ref = db.collection("users").document(user_id)
    doc_ref.delete()
    return {"message": f"User '{user_id}' deleted successfully."}

@app.put("/{user_id}")
def update_user(user_id: str, user: UserData):
    doc_ref = db.collection("users").document(user_id)
    doc_ref.update(user.model_dump()) # Fieldで必須項目に指定しているためmodel_dump()の引数は不要
    return {"message": f"User '{user_id}' updated successfully."}
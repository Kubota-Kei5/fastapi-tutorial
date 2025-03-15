from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from firestore import db
from typing import Dict

app = FastAPI()

# CORSミドルウェアを追加
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 本番環境では適切なオリジンを指定してください
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")


# class Item(BaseModel):
#     name: str
#     price: float
#     is_offer: Union[bool, None] = None

users_ref = db.collection("users")
docs = users_ref.stream()

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
def createUser(data: Dict):
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

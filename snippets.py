from firestore import db
import json
# doc_ref = db.collection("users").document("alovelace")
# doc_ref.set({"first": "Ada", "last": "Lovelace", "born": 1815})

# doc_ref = db.collection("users").document("aturing")
# doc_ref.set({"first": "Alan", "middle": "Mathison", "last": "Turing", "born": 1912})

# users_ref = db.collection("users")
# docs = users_ref.get()

# for doc in docs:
#     print(doc.to_dict().get("born"))
#     # print(f"{doc.id} => {doc.to_dict()}")

users_ref = db.collection("users").document("alovelace")
doc = users_ref.get()

if doc.exists:
    # DocumentSnapshot を辞書型に変換
    data_dict = doc.to_dict()
    # JSON 文字列に変換して出力
    print(json.dumps(data_dict, ensure_ascii=False, indent=2))
else:
    print("Document does not exist")
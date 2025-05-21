# Transformers 관련 import
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import TextClassificationPipeline

# MongoDB 관련 import
from module.db.db_connection import get_collection

# 모델 설정
model_name = "beomi/korean-hatespeech-classifier"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)
pipe = TextClassificationPipeline(model=model, tokenizer=tokenizer, top_k=None)

# offensive_score를 컬렉션에 업데이트하는 함수
def update_offensive_scores():
    collection = get_collection()

    for doc in collection.find():
        text = doc.get("comment")
        if not text:
            continue

        if doc.get("OFF") is True:
            result = pipe(text)[0]
            raw_score = next((item["score"] for item in result if item["label"] == "Offensive"), 0.0)
            offensive_score = round(raw_score, 4)  
        else:
            offensive_score = 0.0  # OFF가 false인 경우는 무조건 0점

        collection.update_one(
            {"_id": doc["_id"]},
            {"$set": {"offensive_score": offensive_score}}
        )

    print("offensive_score 필드 업데이트 완료")

if __name__ == "__main__":
    update_offensive_scores()

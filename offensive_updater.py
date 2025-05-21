# Transformers 관련 import
from transformers import AutoTokenizer, AutoModelForSequenceClassification # 모델 및 토크나이저 로드용 import
from transformers import TextClassificationPipeline # 텍스트 분류 파이프라인 생성용 import 

# MongoDB 관련 import
from module.db.db_connection import get_collection # MongoDB 컬렉션 연결

# 모델 설정
model_name = "beomi/korean-hatespeech-classifier" # 사용할 한국어 혐오 발언 분류 모델 이름 설정
tokenizer = AutoTokenizer.from_pretrained(model_name) # 모델에 맞는 토크나이저 로드
model = AutoModelForSequenceClassification.from_pretrained(model_name) # 분류용 사전학습 모델 로드
pipe = TextClassificationPipeline(model=model, tokenizer=tokenizer, top_k=None) # 텍스트 분류 파이프라인 구성 (모든 라벨 확률 반환)

# offensive_score 업데이트
def update_offensive_scores():
    collection = get_collection() # MongoDB 컬렉션 객체 가져오기

    for doc in collection.find(): # 컬렉션의 모든 문서 반복
        text = doc.get("comment") # 댓글 텍스트(comment) 필드 추출
        if not text: # 댓글이 없거나 비어있는 경우
            continue # 건너뜀

        # 문서가 공격성(OFF)으로 분류된 경우
        if doc.get("OFF") is True: 
            result = pipe(text)[0] # 텍스트 분류 모델 실행 후 결과 리스트 중 첫 번째 항목 추출
            # Offensive 라벨의 점수 추출 (없으면 0.0)
            raw_score = next((item["score"] for item in result if item["label"] == "Offensive"), 0.0)
            offensive_score = round(raw_score, 4)  # 점수를 소수점 4자리로 반올림
        # 문서가 공격성(OFF)으로 분류되지 않은 경우
        else:
            offensive_score = 0.0  # 공격성 점수는 0으로 설정

        collection.update_one(
            {"_id": doc["_id"]}, # 현재 문서를 _id 기준으로 탐색
            {"$set": {"offensive_score": offensive_score}} # offensive_score 필드 업데이트
        )

    print("offensive_score 필드 업데이트 완료")

if __name__ == "__main__": 
    update_offensive_scores() # offensive_score 업데이트

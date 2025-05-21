# MongoDB 관련 import
from pymongo import MongoClient  # MongoDB 클라이언트 객체 import

# Transformers 관련 import
from transformers import AutoTokenizer, AutoModelForSequenceClassification  # 사전학습된 토크나이저 및 분류 모델 로딩
from transformers import TextClassificationPipeline  # 텍스트 분류 파이프라인 구성



# MongoDB 연결 및 데이터베이스 선택
def get_collection():
    mongo_client = MongoClient("mongodb://localhost:27017/")  # 로컬 MongoDB 서버에 연결
    mongo_db = mongo_client["news_comment"]  # 사용할 데이터베이스
    collection = mongo_db["kold_v1"]  # 뉴스 댓글과 공격성 관련 정보를 저장하는 컬렉션
    return collection # 컬렉션 객체 반환
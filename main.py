# 기본 PyTorch 관련 import
import torch # tensor 계산 등 기본 기능
import torch.nn as nn # 신경망 모델 정의용 모듈
from torch.utils.data import Dataset, DataLoader # 데이터셋 및 배치 로더 관련 기능

# Transformers 모델 관련 import
from transformers import AutoModel, AutoTokenizer
from torch.optim import AdamW

# 데이터 처리 관련 import
import pandas as pd # 데이터프레임 처리용
import json # JSON 파일 로딩용

# Google Colab 관련 import
from google.colab import drive  # Google Colab에서 드라이브 마운트용

# 기타 유틸리티 관련 import
import os # 파일 경로 및 디렉토리 생성용
from datetime import datetime # 시간 정보
from tqdm.notebook import tqdm # 학습 진행 표시용

# ------------------------------ #
# 모델 관련 설정
# ------------------------------ #
MODEL_NAME = "monologg/koelectra-base-discriminator" # 사용할 사전학습 KoELECTRA 모델
MAX_LEN = 128 # 토큰 최대 길이
BATCH_SIZE = 8 # 학습 배치 사이즈

# ------------------------------ #
# 라벨 매핑 생성
# ------------------------------ #
def generate_label_mappings(
    data # 원본 KOLD JSON 데이터 리스트
):
    # 타겟 유형
    tgt_types = sorted(set(item.get("TGT") or "none" for item in data)) # 고유 타겟 유형 수집
    tgt_type_to_id = {v: i for i, v in enumerate(tgt_types)} # type → id 매핑
    id_to_tgt_type = {i: v for v, i in tgt_type_to_id.items()} # type → id 매핑
    
    # 타겟 그룹
    tgt_grps = sorted(set(item.get("GRP") or "none" for item in data)) # 고유 그룹 수집
    tgt_group_to_id = {v: i for i, v in enumerate(tgt_grps)} # group → id 매핑
    id_to_tgt_group = {i: v for v, i in tgt_group_to_id.items()} # id → group 역매핑
    
    # 각종 매핑 딕셔너리 반환
    return tgt_type_to_id, id_to_tgt_type, tgt_group_to_id, id_to_tgt_group

# ------------------------------ #
# 데이터셋 정의
# ------------------------------ #
class KOLDDataset(
    Dataset # PyTorch의 기본 Dataset 클래스
):
    # 클래스 초기화
    def __init__(
        self,
        data, # 원본 KOLD JSON 데이터 리스트
        target_type_to_id, # type → id 매핑
        target_group_to_id # group → id 매핑
    ):
        self.data = data # 전체 데이터 저장
        self.target_type_to_id = target_type_to_id # 타겟 유형용 매핑 저장
        self.target_group_to_id = target_group_to_id # 타겟 그룹용 매핑 저장
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME) # KoELECTRA 토크나이저 불러오기
    
    # 클래스 길이 반환
    def __len__(
        self
    ):
        return len(self.data) # 데이터 전체 길이 반환
    
    # 하나의 학습 샘플을 토크나이즈하고 라벨과 함께 반환
    def __getitem__(
        self,  
        idx # 가져올 데이터 인덱스
    ):
        item = self.data[idx] # 해당 인덱스의 데이터 추출
        encoding = self.tokenizer( # KoELECTRA 토크나이저로 입력 문장 토큰화
            item["comment"], # 댓글 본문
            truncation = True, # MAX_LEN보다 길면 잘라냄
            padding = "max_length", # 부족하면 패딩 추가
            max_length = MAX_LEN, # 최대 토큰 길이
            return_tensors = "pt" # PyTorch 텐서 형식 변환
        )
        
        input_ids = encoding["input_ids"].squeeze(0) # 입력 토큰 ID 시퀀스 (batch 차원 제거)
        attention_mask = encoding["attention_mask"].squeeze(0) # 패딩 마스크 (1: 실제 토큰, 0: 패딩)
        
        label_offensive = torch.tensor(int(item["OFF"]), dtype=torch.float) # 공격성 여부 (True/False → float)
        label_target_type = torch.tensor(self.target_type_to_id.get(item["TGT"], 0), dtype=torch.long) # 타겟 유형 ID (없으면 0)
        label_target_group = torch.tensor(self.target_group_to_id.get(item["GRP"], 0), dtype=torch.long) # 타겟 그룹 ID (없으면 0)
        
        return {
            "input_ids": input_ids, # 토크나이즈된 입력 ID 시퀀스
            "attention_mask": attention_mask, # 패딩 여부를 나타내는 마스크
            "label_offensive": label_offensive, # 공격성 여부 라벨
            "label_target_type": label_target_type, # 타겟 유형 라벨 (group, individual 등)
            "label_target_group": label_target_group # 타겟 그룹 라벨 (others-feminist 등)
        }
        
# ------------------------------ #
# 모델 정의
# ------------------------------ #
class KOLDMultiTaskModel(
    nn.Module # PyTorch의 신경망 모듈 기본 클래스
):
    # 클래스 초기화 
    def __init__(
        self,
        num_target_types, # 타겟 유형 분류 클래스 수
        num_target_groups # 타겟 그룹 분류 클래스 수
    ): 
        super().__init__() # nn.Module 초기화
        self.backbone = AutoModel.from_pretrained(MODEL_NAME) # KoELECTRA 백본 모델 로드
        hidden_size = self.backbone.config.hidden_size # 백본 출력 차원
        self.dropout = nn.Dropout(0.1) # 드롭아웃 적용
        
        self.cls_offensive = nn.Linear(hidden_size, 1) # 공격성 여부 이진 분류용 출력 레이어
        self.cls_target_type = nn.Linear(hidden_size, num_target_types) # 타겟 유형 분류용 출력 레이어
        self.cls_target_group = nn.Linear(hidden_size, num_target_groups) # 타겟 그룹 분류용 출력 레이어
        
    # 순전파 (입력을 받아 각 태스크별 예측값 반환)
    def forward(
        self,
        input_ids, # 입력 토큰 ID 시퀀스 (배치)
        attention_mask # 패딩 여부를 나타내는 마스크 (배치)
    ):
        # KoELECTRA 모델의 출력 계산
        outputs = self.backbone( 
            input_ids = input_ids, 
            attention_mask = attention_mask
        )
        
        pooled = outputs.last_hidden_state[:, 0] # [CLS] 토큰 임베딩 추출
        pooled = self.dropout(pooled) # 드롭아웃 적용
        
        offensive = self.cls_offensive(pooled).squeeze(-1) # 공격성 여부 (이진 출력)
        target_type = self.cls_target_type(pooled) # 타겟 유형 분류 결과
        target_group = self.cls_target_group(pooled) # 타겟 그룹 분류 결과
        
        # 세 가지 태스크 예측값 반환
        return offensive, target_type, target_group

from tqdm.notebook import tqdm # Colab 환경에 맞춰 notebook용 tqdm 사용

# ------------------------------ #
# 학습 루프
# ------------------------------ #
def train(
    model, # 학습할 모델 (KOLDMultiTaskModel 인스턴스)
    dataloader, # 학습용 DataLoader (KOLDDataset 배치 제공)
    optimizer, # 최적화 함수 (예: AdamW)
    loss_fns, # 손실 함수 딕셔너리 (BCE, CE 등)
    device # 연산에 사용할 장치 (cuda 또는 cpu)
):
    model.train() # 모델을 학습 모드로 설정 (Dropout, BatchNorm 등 활성화)
    
    total_loss = 0 # 전체 손실 누적
    correct_off = 0 # 공격성 예측 정확도 계산용
    correct_type = 0 # 타겟 유형 정확도 계산용
    correct_group = 0 # 타겟 그룹 정확도 계산용
    total = 0 # 전체 샘플 수

    progress_bar = tqdm(dataloader, desc="학습 진행중") # 배치 진행률 표시용 tqdm

    for batch in progress_bar: # 미니배치 단위로 반복
        optimizer.zero_grad() # 이전 gradient 초기화
        
        input_ids = batch["input_ids"].to(device) # 입력 토큰 ID를 디바이스로 이동 
        attention_mask = batch["attention_mask"].to(device) # 패딩 마스크를 디바이스로 이동
        label_offensive = batch["label_offensive"].to(device) # 공격성 여부 정답 라벨
        label_target_type = batch["label_target_type"].to(device) # 타겟 유형 정답 라벨
        label_target_group = batch["label_target_group"].to(device) # 타겟 그룹 정답 라벨
        
        # 모델 예측 수행
        pred_offensive, pred_target_type, pred_target_group = model(input_ids, attention_mask)
        
        loss_off = loss_fns["bce"](pred_offensive, label_offensive) # 공격성 여부에 대한 BCE 손실 계산
        loss_type = loss_fns["ce"](pred_target_type, label_target_type) # 타겟 유형에 대한 CE 손실 계산
        loss_group = loss_fns["ce"](pred_target_group, label_target_group) # 타겟 그룹에 대한 CE 손실 계산
        
        loss = loss_off + loss_type + loss_group # 총 손실 = 세 태스크 손실의 합
        loss.backward() # 역전파로 그래디언트 계산
        optimizer.step() # 모델 파라미터 업데이트

        total_loss += loss.item() # 손실 누적

        # 공격성 정확도 계산
        pred_binary = (torch.sigmoid(pred_offensive) > 0.5).float() # sigmoid를 통한 이진 확률 (0.5 초과 → 1)
        correct_off += (pred_binary == label_offensive).sum().item() # 예측과 정답 비교 후 맞춘 개수 누적

        # 타겟 유형 정확도 계산
        pred_type_cls = torch.argmax(pred_target_type, dim=1) # 가장 높은 확률의 클래스 선택
        correct_type += (pred_type_cls == label_target_type).sum().item() # 예측과 정답 비교 후 맞춘 개수 누적

        # 타겟 그룹 정확도 계산 
        pred_group_cls = torch.argmax(pred_target_group, dim=1) # 가장 높은 확률의 클래스 선택
        correct_group += (pred_group_cls == label_target_group).sum().item() # 예측과 정답 비교 후 맞춘 개수 누적

        total += label_offensive.size(0) # 전체 샘플 수 누적

        # 현재 배치 손실을 tqdm에 표시
        progress_bar.set_postfix(loss=f"{loss.item():.4f}")

    avg_loss = total_loss / len(dataloader) # 평균 손실
    acc_off = correct_off / total # 공격성 정확도
    acc_type = correct_type / total # 타겟 유형 정확도
    acc_group = correct_group / total # 타겟 그룹 정확도

    # 손실값과 각 정확도 값 출력
    print(f"평균 손실: {avg_loss:.4f}, 공격성 정확도: {acc_off:.4f}, 유형 정확도: {acc_type:.4f}, 그룹 정확도: {acc_group:.4f}")

        
# ------------------------------ #
# 데이터 로딩
# ------------------------------ #
def load_data(
    json_path # KOLD JSON 파일 경로
):
    with open(json_path, "r", encoding="utf-8") as f: # 파일 열기 (UTF-8 인코딩)
        raw_data = json.load(f) # JSON 내용 파싱
    return raw_data # 파싱된 데이터 리스트 반환

# ------------------------------ #
# 실행 
# ------------------------------ #
if __name__ == "__main__":
    json_path = "kold_v1.json" # 실제 사용할 KOLD 데이터 JSON 파일 경로
    raw_data = load_data(json_path) # 데이터 로딩
    
    # 라벨 매핑 딕셔너리 생성
    TARGET_TYPE_TO_ID, ID_TO_TGT_TYPE, TARGET_GROUP_TO_ID, ID_TO_TGT_GROUP = generate_label_mappings(raw_data)
    
    dataset = KOLDDataset(raw_data, TARGET_TYPE_TO_ID, TARGET_GROUP_TO_ID) # 학습용 데이터셋 생성
    dataloader = DataLoader(dataset, batch_size = BATCH_SIZE, shuffle = True) # 배치 단위로 데이터 로딩
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu") # GPU 사용 가능 시 CUDA 사용
    model = KOLDMultiTaskModel(len(TARGET_TYPE_TO_ID), len(TARGET_GROUP_TO_ID)).to(device) # 모델 초기화 및 디바이스 이용
    
    # 체크포인트 저장 경로 설정
    save_dir = "/content/drive/MyDrive/kold_checkpoints" # Google Drive 저장 경로
    os.makedirs(save_dir, exist_ok = True) # 폴더가 없으면 생성

    optimizer = AdamW(model.parameters(), lr=5e-5) # Adamw 옵티마이저 설정
    loss_fns = {
        "bce": nn.BCEWithLogitsLoss(), # 공격성 여부 이진 분류 손실
        "ce": nn.CrossEntropyLoss() # 다중 클래스 분류 손실 (타겟 유형 & 그룹)
    }

    # 몇 번째 에폭부터 시작할지 설정
    START_EPOCH = 0  # 예: 끊겼던 경우, 마지막 에폭 번호로 바꾸기

    # 체크포인트가 존재하면 모델 로드
    resume_path = os.path.join(save_dir, f"kold_epoch{START_EPOCH}.pt")
    if os.path.exists(resume_path):
        model.load_state_dict(torch.load(resume_path)) # 저장된 모델 로드
        print(f"{resume_path}에서 모델 로드 완료") # 로드 완료 출력

    # 에폭(epoch) 단위 학습
    for epoch in range(START_EPOCH, 3):  # 시작 에폭부터 반복
        print(f"{epoch+1}번째 에폭 시작") # 현재 에폭 번호 출력
        train(model, dataloader, optimizer, loss_fns, device) # 모델 학습 수행
        
        # 체크포인트 저장
        checkpoint_path = os.path.join(save_dir, f"kold_epoch{epoch+1}.pt") # 저장 경로 지정
        torch.save(model.state_dict(), checkpoint_path) # 모델 가중치 저장
        print(f"{checkpoint_path} 위치에 체크포인트 저장됨") # 저장 완료 메시지 출력
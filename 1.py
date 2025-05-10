import pickle

ENCODER_PATH = 'D:/cubo/cubo/label_encoder.pkl'

with open(ENCODER_PATH, 'rb') as f:
    label_encoder = pickle.load(f)

# 라벨 리스트 출력
print("라벨 목록:", list(label_encoder.classes_))

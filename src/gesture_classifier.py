import numpy as np
import csv, os, pickle
import sklearn.ensemble
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

DATA_DIR  = "data/gestures"
MODEL_PATH = "models/gesture_model.pkl"
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs("models", exist_ok=True)

# ── Recording ──────────────────────────────────────────────────────────────
def record_gesture(gesture_name, landmarks, samples_so_far):
    """Append one sample to the CSV for this gesture."""
    path = os.path.join(DATA_DIR, f"{gesture_name}.csv")
    with open(path, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(landmarks.tolist())
    return samples_so_far + 1

# ── Training ───────────────────────────────────────────────────────────────
def train_model():
    X, y = [], []
    for fname in os.listdir(DATA_DIR):
        if not fname.endswith(".csv"):
            continue
        label = fname.replace(".csv", "")
        with open(os.path.join(DATA_DIR, fname)) as f:
            for row in csv.reader(f):
                if row:
                    X.append([float(v) for v in row])
                    y.append(label)

    if len(set(y)) < 2:
        print("Need at least 2 gesture classes to train.")
        return None

    le = LabelEncoder()
    y_enc = le.fit_transform(y)
    X_train, X_test, y_train, y_test = train_test_split(X, y_enc, test_size=0.2, random_state=42)

    model = sklearn.ensemble.RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    acc = model.score(X_test, y_test)
    print(f"Model accuracy: {acc*100:.1f}%")

    with open(MODEL_PATH, "wb") as f:
        pickle.dump({"model": model, "encoder": le}, f)
    print(f"Model saved to {MODEL_PATH}")
    return model

# ── Inference ──────────────────────────────────────────────────────────────
class GestureClassifier:
    def __init__(self, confidence_threshold=0.45):
        self.threshold = confidence_threshold
        self.model = None
        self.encoder = None
        self._load()

    def _load(self):
        if os.path.exists(MODEL_PATH):
            with open(MODEL_PATH, "rb") as f:
                data = pickle.load(f)
            self.model = data["model"]
            self.encoder = data["encoder"]

    def predict(self, landmarks, use_threshold=True):
        if self.model is None or len(landmarks) == 0:
            return None, 0.0
        probs = self.model.predict_proba([landmarks])[0]
        best  = np.argmax(probs)
        conf  = probs[best]
        if not use_threshold or conf >= self.threshold:
            return self.encoder.inverse_transform([best])[0], float(conf)
        return None, float(conf)
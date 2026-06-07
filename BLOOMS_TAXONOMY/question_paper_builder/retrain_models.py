"""
Retrains marks model and Bloom's level model and saves them to dataset/
Run from: BLOOMS_TAXONOMY/question_paper_builder/
"""
import pickle
import pandas as pd
from pathlib import Path
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, accuracy_score

TESTING_DIR = Path(__file__).resolve().parent.parent / "testing"
DATASET_DIR = Path(__file__).resolve().parent / "dataset"

# ── 1. Marks model (LinearRegression) ──────────────────────────────────────
print("Training marks model...")
data = pd.read_csv(TESTING_DIR / "ML_QUESTION_Sheet1_final.csv")

X_train, X_test, y_train, y_test = train_test_split(
    data['question'], data['marks'], test_size=0.2, random_state=42
)

vectorizer = CountVectorizer()
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

marks_model = LinearRegression()
marks_model.fit(X_train_vec, y_train)

mae = mean_absolute_error(y_test, marks_model.predict(X_test_vec))
print(f"  Marks model MAE: {mae:.4f}")

with open(DATASET_DIR / "model.pkl", "wb") as f:
    pickle.dump(marks_model, f)
with open(DATASET_DIR / "vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)
print("  Saved model.pkl and vectorizer.pkl")

# ── 2. Bloom's level model (RandomForestClassifier) ────────────────────────
print("Training Bloom's level model...")
blooms_data = pd.read_csv(TESTING_DIR / "blooms_output.csv")

# blooms_level column may have list-as-string like "['understand', 'apply']"
# Use first level only for classification
blooms_data['blooms_level'] = (
    blooms_data['blooms_level']
    .astype(str)
    .str.replace(r"[\[\]']", "", regex=True)
    .str.split(",")
    .str[0]
    .str.strip()
)
blooms_data = blooms_data[blooms_data['blooms_level'] != ""]

X_b = blooms_data['question']
y_b = blooms_data['blooms_level']

X_b_train, X_b_test, y_b_train, y_b_test = train_test_split(
    X_b, y_b, test_size=0.2, random_state=42
)

blooms_vectorizer = CountVectorizer()
X_b_train_vec = blooms_vectorizer.fit_transform(X_b_train)
X_b_test_vec = blooms_vectorizer.transform(X_b_test)

blooms_model = RandomForestClassifier(random_state=42)
blooms_model.fit(X_b_train_vec, y_b_train)

acc = accuracy_score(y_b_test, blooms_model.predict(X_b_test_vec))
print(f"  Bloom's model accuracy: {acc:.4f}")

with open(DATASET_DIR / "blooms_level.pkl", "wb") as f:
    pickle.dump(blooms_model, f)
with open(DATASET_DIR / "blooms_vector.pkl", "wb") as f:
    pickle.dump(blooms_vectorizer, f)
print("  Saved blooms_level.pkl and blooms_vector.pkl")

print("\nAll models retrained and saved successfully!")

"""
Pet Health AI - Model Training Script
=====================================
Loads the symptom knowledge base and produces a trained model artifact.

This script:
1. Loads the training data CSV
2. Creates a symptom feature vector for each case
3. Trains a classification model (Naive Bayes / Decision Tree)
4. Evaluates accuracy using cross-validation
5. Saves the trained model and vectorizer to disk for production use

Usage:
    python manage.py shell
    >>> exec(open('PetHealthAI/knowledge_base/train_model.py').read())

Dependencies (optional - falls back to rule-based engine if not installed):
    pip install scikit-learn pandas numpy joblib
"""

import os
import csv
import sys

# Optional imports - gracefully degrades if not installed
SKLEARN_AVAILABLE = False
try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.naive_bayes import MultinomialNB
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.model_selection import cross_val_score, train_test_split
    from sklearn.metrics import classification_report, accuracy_score
    from sklearn.pipeline import Pipeline
    SKLEARN_AVAILABLE = True
    print("[OK] scikit-learn available")
except ImportError:
    print("[INFO] scikit-learn not installed - using rule-based engine")
    print("[INFO] Install with: pip install scikit-learn pandas numpy joblib")
    sys.exit(0)

# ------------------------------------------------------------------
#  Load Training Data
# ------------------------------------------------------------------

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(SCRIPT_DIR, 'training_data.csv')

print(f"\n[LOADING] Training data from: {CSV_PATH}")

cases = []
with open(CSV_PATH, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        cases.append(row)

print(f"[LOADED] {len(cases)} training cases")

# ------------------------------------------------------------------
#  Build Feature Vectors
# ------------------------------------------------------------------

def normalize(text: str) -> str:
    import re
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

X_text = [normalize(c['symptoms_text']) for c in cases]
y_labels = [c['predicted_illness'] for c in cases]
y_severity = [c['severity_override'] for c in cases]
y_animal = [c['animal_type'] for c in cases]

# ------------------------------------------------------------------
#  Train Illness Classifier
# ------------------------------------------------------------------

print("\n[ TRAINING ] Symptom-to-Illness Classifier...")

X_train, X_test, y_train, y_test = train_test_split(
    X_text, y_labels, test_size=0.2, random_state=42, stratify=y_labels
)

illness_pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(
        max_features=500,
        ngram_range=(1, 2),
        min_df=1,
        max_df=0.95,
    )),
    ('clf', MultinomialNB(alpha=0.1)),
])

illness_pipeline.fit(X_train, y_train)
y_pred = illness_pipeline.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print(f"[ACCURACY] Illness Classification: {accuracy:.2%}")

# Cross-validation
cv_scores = cross_val_score(illness_pipeline, X_text, y_labels, cv=5)
print(f"[CV SCORES] 5-fold: {cv_scores.mean():.2%} ± {cv_scores.std():.2%}")

print("\n[CLASSIFICATION REPORT]")
print(classification_report(y_test, y_pred))

# ------------------------------------------------------------------
#  Train Severity Classifier
# ------------------------------------------------------------------

print("\n[TRAINING] Severity Classifier...")

severity_pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(max_features=300, ngram_range=(1, 2), min_df=1)),
    ('clf', DecisionTreeClassifier(max_depth=5, random_state=42)),
])

X_sev_train, X_sev_test, y_sev_train, y_sev_test = train_test_split(
    X_text, y_severity, test_size=0.2, random_state=42
)
severity_pipeline.fit(X_sev_train, y_sev_train)
sev_pred = severity_pipeline.predict(X_sev_test)
sev_accuracy = accuracy_score(y_sev_test, sev_pred)
print(f"[ACCURACY] Severity Classification: {sev_accuracy:.2%}")

# ------------------------------------------------------------------
#  Save Models
# ------------------------------------------------------------------

MODELS_DIR = os.path.join(SCRIPT_DIR)
ILLNESS_MODEL_PATH = os.path.join(MODELS_DIR, 'illness_model.pkl')
SEVERITY_MODEL_PATH = os.path.join(MODELS_DIR, 'severity_model.pkl')
VECTORIZER_PATH = os.path.join(MODELS_DIR, 'tfidf_vectorizer.pkl')

try:
    import joblib

    joblib.dump(illness_pipeline, ILLNESS_MODEL_PATH)
    joblib.dump(severity_pipeline, SEVERITY_MODEL_PATH)
    joblib.dump(illness_pipeline.named_steps['tfidf'], VECTORIZER_PATH)

    print(f"\n[SAVED] Illness model: {ILLNESS_MODEL_PATH}")
    print(f"[SAVED] Severity model: {SEVERITY_MODEL_PATH}")
    print(f"[SAVED] TF-IDF vectorizer: {VECTORIZER_PATH}")

    # Quick validation
    sample_text = "vomiting bloody stool lethargy puppy not vaccinated"
    pred = illness_pipeline.predict([sample_text])[0]
    print(f"\n[SAMPLE] Input: '{sample_text}'")
    print(f"[PREDICTION] Predicted illness: {pred}")

except ImportError:
    print("\n[SKIP] joblib not installed - cannot save model")
    print("[INFO] Install with: pip install joblib")

print("\n[COMPLETE] Training finished successfully!\n")

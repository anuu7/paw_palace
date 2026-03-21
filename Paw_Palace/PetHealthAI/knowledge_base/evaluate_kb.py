"""
Pet Health AI - Knowledge Base Evaluation Script
================================================
Tests the expert system engine against the training dataset to measure
precision, recall, and F1 score for each condition.

Usage:
    python manage.py shell
    >>> exec(open('PetHealthAI/knowledge_base/evaluate_kb.py').read())
"""

import os
import sys
import csv

# Add project root to path for Django shell
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.path.join(BASE_DIR, 'Paw_Palace'))

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Paw_Palace.settings')
django.setup()

from PetHealthAI.engine import diagnose
from collections import defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(SCRIPT_DIR, 'training_data.csv')

print("=" * 70)
print("  PET HEALTH AI - EXPERT SYSTEM EVALUATION REPORT")
print("=" * 70)

# Load cases
cases = []
with open(CSV_PATH, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        cases.append(row)

print(f"\nLoaded {len(cases)} test cases\n")

# Track results per illness
results = defaultdict(lambda: {'tp': 0, 'fp': 0, 'fn': 0})

total_correct = 0
total_high_confidence_correct = 0

for i, case in enumerate(cases):
    animal = case['animal_type']
    age = int(float(case['pet_age']))
    symptoms = case['symptoms_text']
    expected = case['predicted_illness']

    result = diagnose(
        pet_name='TestPet',
        pet_age=age,
        animal_type=animal,
        symptoms_text=symptoms,
    )

    predicted = result['primary_diagnosis']['illness']
    confidence = result['primary_diagnosis']['confidence']

    is_correct = predicted.strip().lower() == expected.strip().lower()
    if is_correct:
        total_correct += 1
        results[expected]['tp'] += 1
        if confidence >= 0.7:
            total_high_confidence_correct += 1
    else:
        results[expected]['fn'] += 1
        # Add false positives for the predicted illness
        results[predicted]['fp'] += 1

    # Progress indicator
    if (i + 1) % 50 == 0:
        print(f"  Processed {i+1}/{len(cases)} cases...")

# Calculate metrics
print("\n" + "-" * 70)
print(f"{'Condition':<35} {'TP':>6} {'FP':>6} {'FN':>6} {'Prec':>8} {'Recall':>8}")
print("-" * 70)

total_tp = total_fp = total_fn = 0

for illness, counts in sorted(results.items()):
    tp = counts['tp']
    fp = counts['fp']
    fn = counts['fn']
    total_tp += tp
    total_fp += fp
    total_fn += fn

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0

    status = "✓" if precision >= 0.7 else "⚠" if precision >= 0.4 else "✗"
    print(f"{status} {illness:<33} {tp:>6} {fp:>6} {fn:>6} {precision:>7.1%} {recall:>7.1%}")

print("-" * 70)

overall_precision = total_tp / (total_tp + total_fp) if (total_tp + total_fp) > 0 else 0
overall_recall = total_tp / (total_tp + total_fn) if (total_tp + total_fn) > 0 else 0
overall_f1 = 2 * overall_precision * overall_recall / (overall_precision + overall_recall) if (overall_precision + overall_recall) > 0 else 0

print(f"\n{'OVERALL METRICS':}")
print(f"  Accuracy:                   {total_correct}/{len(cases)} = {total_correct/len(cases):.2%}")
print(f"  High-confidence accuracy:   {total_high_confidence_correct}/{len(cases)} = {total_high_confidence_correct/len(cases):.2%}")
print(f"  Precision:                  {overall_precision:.2%}")
print(f"  Recall:                     {overall_recall:.2%}")
print(f"  F1 Score:                   {overall_f1:.2%}")

# Confidence distribution
confidences = []
for case in cases:
    result = diagnose(
        pet_name='TestPet',
        pet_age=int(float(case['pet_age'])),
        animal_type=case['animal_type'],
        symptoms_text=case['symptoms_text'],
    )
    confidences.append(result['primary_diagnosis']['confidence'])

high_conf = sum(1 for c in confidences if c >= 0.7)
med_conf = sum(1 for c in confidences if 0.4 <= c < 0.7)
low_conf = sum(1 for c in confidences if c < 0.4)

print(f"\n{'CONFIDENCE DISTRIBUTION':}")
print(f"  High confidence (≥70%):    {high_conf} ({high_conf/len(confidences):.1%})")
print(f"  Medium confidence (40-70%): {med_conf} ({med_conf/len(confidences):.1%})")
print(f"  Low confidence (<40%):      {low_conf} ({low_conf/len(confidences):.1%})")

print("\n" + "=" * 70)
print("  EVALUATION COMPLETE")
print("=" * 70 + "\n")

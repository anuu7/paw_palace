"""
Pet Health AI - Diagnostic Expert System Engine
==============================================
A weighted keyword-matching inference engine that:
1. Extracts keywords from the user's free-text symptom description
2. Matches them against the knowledge base per animal type
3. Produces ranked diagnoses with confidence scores
4. Returns differential diagnoses, severity, and recommended actions

Architecture:
  User Input (pet info + symptoms text)
       ↓
  NLP Keyword Extraction (normalize + tokenize)
       ↓
  Knowledge Base Lookup (per animal type)
       ↓
  Weighted Scoring Algorithm
       ↓
  Confidence Normalization
       ↓
  Diagnosis Ranking + Differential List
       ↓
  Recommended Actions + Severity Assessment
"""

import re
from typing import Any

from .knowledge_base.symptoms import DISEASE_KNOWLEDGE_BASE, GENERAL_SYMPTOMS


# ------------------------------------------------------------------
#  NLP / Keyword Extraction
# ------------------------------------------------------------------

def normalize_text(text: str) -> str:
    """Lowercase and strip non-alphanumeric characters for matching."""
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def extract_keywords(raw_text: str) -> set[str]:
    """
    Extract individual words and common bigrams from the free-text input.
    Returns a set of normalized keyword tokens.
    """
    text = normalize_text(raw_text)
    tokens = text.split()

    # Build bigrams (two-word phrases) for better matching
    bigrams = {f"{tokens[i]} {tokens[i+1]}" for i in range(len(tokens) - 1)}

    return set(tokens) | bigrams


def extract_negations(raw_text: str) -> set[str]:
    """
    Detect negated symptom phrases so we don't false-match.
    E.g. 'no vomiting' should not count 'vomiting' as present.
    """
    text = normalize_text(raw_text)
    negated = set()

    negation_words = {'no', 'not', 'without', 'never', "doesn't", "dont", "isn't",
                      "isnt", "wasn't", "wasnt", "doesn't", "doesnt", "hasn't",
                      "hasnt", "haven't", "havent", "never", "neither", "nor"}

    # Detect "no X" patterns
    words = text.split()
    for i, word in enumerate(words):
        if word in negation_words and i + 1 < len(words):
            negated.add(words[i + 1])

    return negated


# ------------------------------------------------------------------
#  Scoring Algorithm
# ------------------------------------------------------------------

def compute_diagnosis_score(
    keywords: set[str],
    negated: set[str],
    disease: dict,
) -> float:
    """
    Calculate a weighted score for a single disease given matched keywords.

    Score = sum(symptom_weight for each matched symptom that isn't negated)
    We also apply a "coverage bonus" for diseases where many symptoms match.
    """
    score = 0.0
    matched_symptoms = []

    for symptom, weight in disease["symptoms"]:
        symptom_lower = symptom.lower()
        if symptom_lower in negated:
            continue  # Skip negated symptoms

        if symptom_lower in keywords:
            score += weight
            matched_symptoms.append(symptom)

    # Coverage bonus: if we matched >60% of a disease's symptoms, add a bonus
    coverage_ratio = len(matched_symptoms) / len(disease["symptoms"])
    if coverage_ratio >= 0.6:
        score += 0.5  # Significant bonus for high coverage

    return score, matched_symptoms


def assess_severity(
    confidence_score: float,
    raw_severity: str,
    age: int,
    animal_type: str,
) -> str:
    """
    Combine the knowledge-base severity with the AI confidence score and
    age/animal context to produce a final severity assessment.
    """
    severity_map = {"low": 1, "moderate": 2, "high": 3, "critical": 4}
    base = severity_map.get(raw_severity.lower(), 2)

    # Escalate if confidence is very high
    if confidence_score >= 0.8:
        base = min(base + 1, 4)
    elif confidence_score < 0.3:
        base = max(base - 1, 1)

    # Puppies/kittens and senior pets get severity bump
    if animal_type in ("dog", "cat") and age < 1:
        base = min(base + 1, 4)
    if animal_type in ("dog", "cat") and age > 8:
        base = min(base + 1, 4)

    reverse_map = {1: "low", 2: "moderate", 3: "high", 4: "critical"}
    return reverse_map[base]


def calculate_confidence(normalized_score: float, matched_count: int) -> float:
    """
    Convert the raw weighted score to a 0.0-1.0 confidence value.
    Uses a logistic-like curve to avoid overly inflated scores.
    """
    # sigmoid-like normalization
    import math
    confidence = normalized_score / (normalized_score + 3.0)
    confidence = max(0.0, min(1.0, confidence))

    # Boost for having many distinct symptom matches
    if matched_count >= 4:
        confidence = min(1.0, confidence + 0.05)

    return round(confidence, 2)


# ------------------------------------------------------------------
#  Main Diagnosis Engine
# ------------------------------------------------------------------

def diagnose(
    pet_name: str,
    pet_age: int,
    animal_type: str,
    symptoms_text: str,
) -> dict[str, Any]:
    """
    Core public API.

    Takes pet details and a free-text symptom description,
    runs the expert system, and returns a structured result dict:

    {
        "pet_name": str,
        "animal_type": str,
        "matched_symptoms": [str, ...],
        "primary_diagnosis": {
            "illness": str,
            "confidence": float (0.0-1.0),
            "severity": str,
            "description": str,
            "matched_symptoms": [str, ...],
            "recommended_actions": [str, ...],
        },
        "differential_diagnoses": [
            {"illness": str, "confidence": float, "severity": str}, ...
        ],
        "general_health_tips": [str, ...],
        "matched_count": int,
        "knowledge_base": str,
    }
    """
    animal_type = animal_type.lower().strip()
    kb = DISEASE_KNOWLEDGE_BASE.get(animal_type, [])

    if not kb:
        return _empty_result(pet_name, animal_type, symptoms_text)

    keywords = extract_keywords(symptoms_text)
    negated = extract_negations(symptoms_text)

    # --- Score every disease ---
    scored = []
    for disease in kb:
        score, matched = compute_diagnosis_score(keywords, negated, disease)
        if matched:
            scored.append((score, len(matched), disease, matched))

    if not scored:
        return _no_match_result(pet_name, animal_type, symptoms_text, keywords)

    # --- Sort by score descending ---
    scored.sort(key=lambda x: (-x[0], -x[1]))

    top_score, top_matched_count, top_disease, top_matched = scored[0]

    # --- Normalize confidence for top result ---
    confidence = calculate_confidence(top_score, top_matched_count)
    severity = assess_severity(confidence, top_disease["severity"], pet_age, animal_type)

    # --- Build differential diagnoses (top 3 less likely) ---
    differentials = []
    for score, matched_count, disease, matched in scored[1:4]:
        diff_conf = calculate_confidence(score, matched_count)
        diff_sev = assess_severity(diff_conf, disease["severity"], pet_age, animal_type)
        differentials.append({
            "illness": disease["illness"],
            "confidence": diff_conf,
            "severity": diff_sev,
            "matched_symptoms": matched,
        })

    # --- Gather all matched symptom keywords across all diseases ---
    all_matched = list(set(top_matched))
    for _, _, _, matched in scored[1:]:
        all_matched = list(set(all_matched + matched))

    # --- General health tips based on animal type ---
    tips = _get_general_tips(animal_type)

    return {
        "pet_name": pet_name,
        "animal_type": animal_type,
        "matched_symptoms": all_matched,
        "primary_diagnosis": {
            "illness": top_disease["illness"],
            "confidence": confidence,
            "severity": severity,
            "description": top_disease.get("description", ""),
            "matched_symptoms": top_matched,
            "recommended_actions": top_disease["actions"],
        },
        "differential_diagnoses": differentials,
        "general_health_tips": tips,
        "matched_count": len(all_matched),
        "knowledge_base": f"{len(kb)} conditions evaluated",
        "symptoms_analyzed": len(keywords),
    }


# ------------------------------------------------------------------
#  Helper Result Builders
# ------------------------------------------------------------------

def _empty_result(pet_name, animal_type, symptoms_text):
    return {
        "pet_name": pet_name,
        "animal_type": animal_type,
        "matched_symptoms": [],
        "primary_diagnosis": {
            "illness": "No data available",
            "confidence": 0.0,
            "severity": "unknown",
            "description": f"We don't have symptom data for '{animal_type}' yet. "
                           "Please consult a veterinarian directly.",
            "matched_symptoms": [],
            "recommended_actions": [
                "Please consult a veterinarian for proper diagnosis",
                "Document all symptoms and their duration",
                "Note any changes in behavior, appetite, or bathroom habits",
            ],
        },
        "differential_diagnoses": [],
        "general_health_tips": _get_general_tips(animal_type),
        "matched_count": 0,
        "knowledge_base": "0 conditions evaluated",
        "symptoms_analyzed": 0,
    }


def _no_match_result(pet_name, animal_type, symptoms_text, keywords):
    return {
        "pet_name": pet_name,
        "animal_type": animal_type,
        "matched_symptoms": list(keywords),
        "primary_diagnosis": {
            "illness": "Insufficient symptoms matched",
            "confidence": 0.1,
            "severity": "unknown",
            "description": "The symptoms you described don't match enough known conditions "
                           "in our knowledge base for confident diagnosis. "
                           "Please provide more specific symptoms or consult a veterinarian.",
            "matched_symptoms": list(keywords),
            "recommended_actions": [
                "Try describing symptoms more specifically (e.g., 'vomiting after eating')",
                "Note when symptoms started and their frequency",
                "Consult a veterinarian for professional examination",
                "Keep a symptom diary to track changes over time",
            ],
        },
        "differential_diagnoses": [],
        "general_health_tips": _get_general_tips(animal_type),
        "matched_count": 0,
        "knowledge_base": "0 conditions matched",
        "symptoms_analyzed": len(keywords),
    }


def _get_general_tips(animal_type: str) -> list[str]:
    tips_map = {
        "dog": [
            "Keep vaccinations up to date throughout your dog's life",
            "Use flea, tick, and heartworm prevention year-round",
            "Feed a balanced, age-appropriate diet",
            "Provide daily exercise appropriate for breed and age",
            "Regular dental check-ups and teeth cleaning",
            "Schedule annual veterinary wellness exams",
        ],
        "cat": [
            "Keep indoor cats mentally stimulated with toys and climbing spaces",
            "Maintain a clean litter box - scoop daily, full change weekly",
            "Provide fresh water daily - consider a water fountain",
            "Feed measured portions to prevent obesity",
            "Annual vet check-ups even for indoor cats",
            "Regular brushing reduces hairballs and strengthens bond",
        ],
        "bird": [
            "Ensure cage is cleaned weekly with disinfectant",
            "Provide varied diet: pellets, seeds, vegetables, fruits",
            "Allow supervised out-of-cage time daily",
            "Maintain stable room temperature (65-80°F)",
            "Avoid non-stick cookware fumes (toxic to birds)",
            "Annual avian vet check-ups are essential",
        ],
        "rabbit": [
            "Unlimited hay (Timothy grass hay) should be 80% of diet",
            "Avoid cedar and pine shavings - use paper-based bedding",
            "Spay/neuter to prevent cancer and behavioral issues",
            "Provide safe exercise time outside the cage daily",
            "Keep vaccinations current (RHDV in applicable regions)",
            "Check teeth monthly - they grow continuously",
        ],
        "hamster": [
            "Cage should be at least 450 sq inches of floor space",
            "Use dust-free, paper-based bedding (avoid cedar/pine)",
            "Provide an exercise wheel (solid surface, appropriate size)",
            "Clean cage weekly - spot clean daily",
            "Hamsters are nocturnal - respect their sleep schedule",
            "Provide chew toys to maintain dental health",
        ],
        "fish": [
            "Test water parameters weekly (ammonia, nitrite, nitrate, pH)",
            "Perform 25% water change weekly",
            "Do not overfeed - remove uneaten food after 2 minutes",
            "Match fish species for compatibility before adding new fish",
            "Quarantine new fish for 2-4 weeks before adding to tank",
            "Replace filter media monthly (rinse in old tank water)",
        ],
        "reptile": [
            "Provide species-specific UVB lighting (10-12 hours/day)",
            "Maintain proper temperature gradient in enclosure",
            "Feed a species-appropriate diet (research thoroughly)",
            "Provide hiding spots on both warm and cool sides",
            "Monitor humidity levels appropriate for your species",
            "Annual veterinary check-up with reptile-experienced vet",
        ],
    }
    return tips_map.get(
        animal_type.lower(),
        [
            "Schedule regular veterinary wellness check-ups",
            "Maintain a species-appropriate diet",
            "Keep living environment clean and stress-free",
            "Monitor for behavioral changes and address them promptly",
        ]
    )

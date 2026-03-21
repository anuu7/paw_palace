from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from Paw.models import Petuser
from .forms import DiagnosisForm, DiagnosisFeedbackForm
from .models import DiagnosisRecord, DiagnosisFeedback
from .engine import diagnose


def _get_user(request):
    """
    Extract and validate the logged-in Petuser from the session.
    Returns (user, None) on success, or (None, redirect_response) on failure.
    Uses the same session key ('id') as Paw's login system.
    """
    username = request.session.get('id')
    if not username:
        return None, redirect('log')
    try:
        return Petuser.objects.get(username=username), None
    except Petuser.DoesNotExist:
        messages.error(request, "Session expired. Please log in again.")
        return None, redirect('log')


# ------------------------------------------------------------------
#  AI Diagnosis Entry Point
# ------------------------------------------------------------------

def ai_diagnosis(request):
    """
    Main view: displays the diagnosis input form.
    Only accessible to logged-in users (Petuser).
    """
    user, error = _get_user(request)
    if error:
        return error

    form = DiagnosisForm()

    if request.method == 'POST':
        form = DiagnosisForm(request.POST)
        if form.is_valid():
            result = diagnose(
                pet_name=form.cleaned_data['pet_name'],
                pet_age=form.cleaned_data['pet_age'],
                animal_type=form.cleaned_data['animal_type'],
                symptoms_text=form.cleaned_data['symptoms_description'],
            )

            record = DiagnosisRecord.objects.create(
                user=user,
                pet_name=form.cleaned_data['pet_name'],
                pet_age=form.cleaned_data['pet_age'],
                animal_type=form.cleaned_data['animal_type'],
                symptoms_description=form.cleaned_data['symptoms_description'],
                symptoms_matched=result['matched_symptoms'],
                predicted_illness=result['primary_diagnosis']['illness'],
                confidence_score=result['primary_diagnosis']['confidence'],
                severity=result['primary_diagnosis']['severity'],
                recommended_actions=result['primary_diagnosis']['recommended_actions'],
                differential_diagnoses=result['differential_diagnoses'],
            )

            request.session['last_diagnosis_id'] = record.id

            messages.success(
                request,
                f"Diagnosis complete for {result['pet_name']}! "
                f"Primary prediction: {result['primary_diagnosis']['illness']} "
                f"({result['primary_diagnosis']['confidence']*100:.0f}% confidence)"
            )

            return redirect('ai_diagnosis_result', record_id=record.id)
        else:
            messages.error(request, "Please correct the errors below.")

    pet_param = request.GET.get('pet')
    if pet_param:
        form.initial['pet_name'] = pet_param

    return render(request, 'ai_diagnosis/ai_diagnosis.html', {
        'form': form,
        'user': user,
    })


# ------------------------------------------------------------------
#  Diagnosis Results View
# ------------------------------------------------------------------

def ai_diagnosis_result(request, record_id):
    """
    Displays the diagnosis result with detailed findings,
    recommended actions, and differential diagnoses.
    """
    user, error = _get_user(request)
    if error:
        return error

    record = get_object_or_404(DiagnosisRecord, pk=record_id, user=user)

    confidence_pct = round(record.confidence_score * 100)

    severity_colors = {
        'low': '#28a745',
        'moderate': '#ffc107',
        'high': '#fd7e14',
        'critical': '#dc3545',
    }
    severity_color = severity_colors.get(record.severity, '#6c757d')

    if record.confidence_score >= 0.7:
        confidence_color = '#28a745'
        confidence_label = 'High Confidence'
    elif record.confidence_score >= 0.4:
        confidence_color = '#ffc107'
        confidence_label = 'Moderate Confidence'
    else:
        confidence_color = '#dc3545'
        confidence_label = 'Low Confidence'

    context = {
        'record': record,
        'user': user,
        'confidence_pct': confidence_pct,
        'confidence_color': confidence_color,
        'confidence_label': confidence_label,
        'severity_color': severity_color,
        'all_symptoms': record.symptoms_matched if isinstance(record.symptoms_matched, list) else [],
        'recommended_actions': record.recommended_actions if isinstance(record.recommended_actions, list) else [],
        'differentials': record.differential_diagnoses if isinstance(record.differential_diagnoses, list) else [],
    }

    return render(request, 'ai_diagnosis/ai_diagnosis_result.html', context)


# ------------------------------------------------------------------
#  Diagnosis History View
# ------------------------------------------------------------------

def ai_diagnosis_history(request):
    """
    Shows the logged-in user's past diagnosis records.
    """
    user, error = _get_user(request)
    if error:
        return error

    records = DiagnosisRecord.objects.filter(user=user).order_by('-created_at')[:50]

    return render(request, 'ai_diagnosis/ai_diagnosis_history.html', {
        'records': records,
        'user': user,
        'total_records': records.count(),
    })


# ------------------------------------------------------------------
#  Diagnosis Feedback View
# ------------------------------------------------------------------

def ai_diagnosis_feedback(request, record_id):
    """
    Allows users to submit feedback on a diagnosis for continuous learning.
    """
    user, error = _get_user(request)
    if error:
        return error

    record = get_object_or_404(DiagnosisRecord, pk=record_id, user=user)
    existing_feedback = DiagnosisFeedback.objects.filter(diagnosis=record).first()

    if request.method == 'POST':
        form = DiagnosisFeedbackForm(request.POST)
        if form.is_valid():
            if existing_feedback:
                existing_feedback.accuracy_rating = form.cleaned_data['accuracy_rating']
                existing_feedback.veterinarian_diagnosis = form.cleaned_data['veterinarian_diagnosis']
                existing_feedback.notes = form.cleaned_data['notes']
                existing_feedback.save()
                messages.success(request, "Feedback updated successfully!")
            else:
                DiagnosisFeedback.objects.create(
                    diagnosis=record,
                    accuracy_rating=form.cleaned_data['accuracy_rating'],
                    veterinarian_diagnosis=form.cleaned_data['veterinarian_diagnosis'],
                    notes=form.cleaned_data['notes'],
                )
                messages.success(request, "Thank you for your feedback! It helps improve our AI.")
            return redirect('ai_diagnosis_history')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = DiagnosisFeedbackForm()

    return render(request, 'ai_diagnosis/ai_diagnosis_feedback.html', {
        'form': form,
        'record': record,
        'existing_feedback': existing_feedback,
        'user': user,
    })


# ------------------------------------------------------------------
#  Health Tips Page
# ------------------------------------------------------------------

def ai_health_tips(request):
    """
    General pet health tips organized by animal type.
    """
    user, error = _get_user(request)
    if error:
        return error

    from .engine import _get_general_tips

    animal_types = [
        ('dog', 'Dog', '🐕'),
        ('cat', 'Cat', '🐈'),
        ('bird', 'Bird', '🐦'),
        ('rabbit', 'Rabbit', '🐇'),
        ('hamster', 'Hamster', '🐹'),
        ('fish', 'Fish', '🐟'),
        ('reptile', 'Reptile', '🦎'),
    ]

    tips_by_animal = {
        atype: _get_general_tips(atype) for atype, _, _ in animal_types
    }

    return render(request, 'ai_diagnosis/ai_health_tips.html', {
        'animal_types': animal_types,
        'tips_by_animal': tips_by_animal,
        'user': user,
    })

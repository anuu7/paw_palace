from django.db import models
from Paw.models import Petuser


class DiagnosisRecord(models.Model):
    """Stores each AI diagnosis request and result for a logged-in user."""

    ANIMAL_TYPES = [
        ('dog', 'Dog'),
        ('cat', 'Cat'),
        ('bird', 'Bird'),
        ('rabbit', 'Rabbit'),
        ('hamster', 'Hamster'),
        ('fish', 'Fish'),
        ('reptile', 'Reptile'),
    ]

    SEVERITY_CHOICES = [
        ('low', 'Low'),
        ('moderate', 'Moderate'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]

    user = models.ForeignKey(
        Petuser,
        on_delete=models.CASCADE,
        related_name='diagnosis_records',
        null=True,
        blank=True,
        help_text="The user who requested this diagnosis"
    )
    shop = models.ForeignKey(
        'Paw.Petshop',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='diagnosis_records',
        help_text="The shop that requested this diagnosis"
    )
    account_type = models.CharField(
        max_length=20,
        default='user',
        help_text="'user' for pet owners, 'shop' for shop owners"
    )
    pet_name = models.CharField(
        max_length=100,
        help_text="Name of the pet being diagnosed"
    )
    pet_age = models.PositiveIntegerField(
        help_text="Age of the pet in years"
    )
    animal_type = models.CharField(
        max_length=20,
        choices=ANIMAL_TYPES,
        help_text="Type of animal"
    )
    symptoms_description = models.TextField(
        help_text="Free-text description of symptoms provided by user"
    )
    symptoms_matched = models.JSONField(
        default=list,
        help_text="List of matched symptom keywords from the AI engine"
    )
    predicted_illness = models.CharField(
        max_length=200,
        help_text="Primary predicted illness"
    )
    confidence_score = models.FloatField(
        help_text="AI confidence score (0.0 - 1.0)"
    )
    severity = models.CharField(
        max_length=10,
        choices=SEVERITY_CHOICES,
        help_text="Assessed severity level"
    )
    recommended_actions = models.JSONField(
        default=list,
        help_text="List of recommended actions from the AI"
    )
    differential_diagnoses = models.JSONField(
        default=list,
        help_text="Alternative possible diagnoses with scores"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Diagnosis Record'
        verbose_name_plural = 'Diagnosis Records'

    def __str__(self):
        return f"{self.pet_name} ({self.animal_type}) - {self.predicted_illness} [{self.created_at.strftime('%Y-%m-%d %H:%M')}]"


class DiagnosisFeedback(models.Model):
    """Stores user feedback on diagnosis accuracy for continuous learning."""

    FEEDBACK_CHOICES = [
        ('accurate', 'Accurate'),
        ('partially_accurate', 'Partially Accurate'),
        ('inaccurate', 'Inaccurate'),
        ('unknown', 'Unknown'),
    ]

    diagnosis = models.OneToOneField(
        DiagnosisRecord,
        on_delete=models.CASCADE,
        related_name='feedback'
    )
    accuracy_rating = models.CharField(
        max_length=20,
        choices=FEEDBACK_CHOICES,
        help_text="How accurate the diagnosis was"
    )
    veterinarian_diagnosis = models.TextField(
        blank=True,
        help_text="Actual diagnosis from a vet (if available)"
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback for Diagnosis #{self.diagnosis_id}: {self.accuracy_rating}"

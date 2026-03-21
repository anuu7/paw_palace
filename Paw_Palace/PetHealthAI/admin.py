from django.contrib import admin
from .models import DiagnosisRecord, DiagnosisFeedback


@admin.register(DiagnosisRecord)
class DiagnosisRecordAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'user', 'pet_name', 'animal_type', 'pet_age',
        'predicted_illness', 'confidence_score', 'severity', 'created_at'
    ]
    list_filter = ['animal_type', 'severity', 'created_at']
    search_fields = ['pet_name', 'predicted_illness', 'user__username']
    ordering = ['-created_at']
    readonly_fields = [
        'user', 'pet_name', 'pet_age', 'animal_type',
        'symptoms_description', 'symptoms_matched', 'predicted_illness',
        'confidence_score', 'severity', 'recommended_actions',
        'differential_diagnoses', 'created_at'
    ]
    fieldsets = (
        ('Pet Information', {
            'fields': ('user', 'pet_name', 'pet_age', 'animal_type')
        }),
        ('User Input', {
            'fields': ('symptoms_description',)
        }),
        ('AI Diagnosis Result', {
            'fields': (
                'predicted_illness', 'confidence_score', 'severity',
                'symptoms_matched', 'recommended_actions',
                'differential_diagnoses',
            )
        }),
        ('Metadata', {
            'fields': ('created_at',)
        }),
    )


@admin.register(DiagnosisFeedback)
class DiagnosisFeedbackAdmin(admin.ModelAdmin):
    list_display = ['id', 'diagnosis', 'accuracy_rating', 'created_at']
    list_filter = ['accuracy_rating', 'created_at']
    search_fields = ['diagnosis__predicted_illness', 'veterinarian_diagnosis']
    ordering = ['-created_at']

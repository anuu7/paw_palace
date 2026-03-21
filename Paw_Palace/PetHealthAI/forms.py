from django import forms

from .models import DiagnosisRecord, DiagnosisFeedback


class DiagnosisForm(forms.ModelForm):
    """
    Form for users to input pet information and describe symptoms.
    """

    ANIMAL_TYPE_CHOICES = [
        ('', 'Select animal type'),
        ('dog', 'Dog'),
        ('cat', 'Cat'),
        ('bird', 'Bird'),
        ('rabbit', 'Rabbit'),
        ('hamster', 'Hamster'),
        ('fish', 'Fish'),
        ('reptile', 'Reptile'),
    ]

    pet_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "Enter your pet's name (e.g., Buddy)",
            'aria-label': 'Pet Name',
        }),
        help_text="The name of your pet"
    )

    pet_age = forms.IntegerField(
        required=True,
        min_value=0,
        max_value=50,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': "Age in years",
            'min': '0',
            'max': '50',
            'aria-label': 'Pet Age',
        }),
        help_text="Pet's age in years (0 for newborns)"
    )

    animal_type = forms.ChoiceField(
        required=True,
        choices=ANIMAL_TYPE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select',
            'aria-label': 'Animal Type',
        }),
        help_text="Type of your pet"
    )

    symptoms_description = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 6,
            'placeholder': (
                "Describe ALL symptoms you have observed in detail. Include:\n"
                "• What you see (vomiting, diarrhea, limping, etc.)\n"
                "• When symptoms started\n"
                "• How often they occur\n"
                "• Any changes in behavior or appetite\n"
                "• Recent events (new food, environment changes)\n\n"
                "Example: 'My dog has been vomiting for 2 days, seems lethargic, "
                "won't eat his food, and had a small amount of blood in his stool this morning.'"
            ),
            'aria-label': 'Symptoms Description',
        }),
        help_text="Describe symptoms in detail - the more information, the better the prediction"
    )

    class Meta:
        model = DiagnosisRecord
        fields = ['pet_name', 'pet_age', 'animal_type', 'symptoms_description']

    def clean_symptoms_description(self):
        data = self.cleaned_data['symptoms_description']
        if len(data.strip()) < 20:
            raise forms.ValidationError(
                "Please provide a more detailed description of symptoms "
                "(at least 20 characters). The AI needs more context to make "
                "an accurate prediction."
            )
        return data.strip()

    def clean_animal_type(self):
        data = self.cleaned_data['animal_type']
        if not data:
            raise forms.ValidationError("Please select your pet's animal type.")
        return data


class DiagnosisFeedbackForm(forms.ModelForm):
    """
    Form for users to provide feedback on a diagnosis.
    """

    ACCURACY_CHOICES = [
        ('', 'Select accuracy rating'),
        ('accurate', 'Accurate - Diagnosis was correct'),
        ('partially_accurate', 'Partially Accurate - Close but not exact'),
        ('inaccurate', 'Inaccurate - Did not match'),
        ('unknown', "Unknown - Couldn't verify"),
    ]

    accuracy_rating = forms.ChoiceField(
        required=True,
        choices=ACCURACY_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select',
        }),
    )

    veterinarian_diagnosis = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': "What did the veterinarian diagnose? (optional)",
        }),
        help_text="What was the actual diagnosis from a vet?"
    )

    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': "Any additional notes or feedback? (optional)",
        }),
        help_text="Any additional feedback"
    )

    class Meta:
        model = DiagnosisFeedback
        fields = ['accuracy_rating', 'veterinarian_diagnosis', 'notes']

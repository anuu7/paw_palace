from django.urls import path
from . import views

urlpatterns = [
    path('ai-diagnosis', views.ai_diagnosis, name='ai_diagnosis'),
    path('ai-diagnosis/result/<int:record_id>', views.ai_diagnosis_result, name='ai_diagnosis_result'),
    path('ai-diagnosis/history', views.ai_diagnosis_history, name='ai_diagnosis_history'),
    path('ai-diagnosis/feedback/<int:record_id>', views.ai_diagnosis_feedback, name='ai_diagnosis_feedback'),
    path('ai-health-tips', views.ai_health_tips, name='ai_health_tips'),
]

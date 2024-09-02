from django.urls import path
import models_api.whispers_api.views as views

urlpatterns = [
    path('transcribe/', views.Transcribe.as_view()),
]
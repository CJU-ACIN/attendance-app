from django import forms
from survey.models import Survey

class SurveyForm(forms.ModelForm):
    class Meta:
        model = Survey
        fields = ('course_id', 'question1', 'question2', 'question3')
        widgets = {
            'course_id': forms.Select(attrs={'class': 'form-select'}),
            'question1': forms.TextInput(attrs={'class': 'form-control'}),
            'question2': forms.TextInput(attrs={'class': 'form-control'}),
            'question3': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'course_id': '분반 선택',
            'question1': '질문 1',
            'question2': '질문 2',
            'question3': '질문 3',
        }

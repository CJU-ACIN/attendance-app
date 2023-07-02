from django import forms
from survey.models import Survey, SurveyReply

class SurveyForm(forms.ModelForm):
    class Meta:
        model = Survey
        fields = ('question1', 'question2', 'question3')
        widgets = {
            'course_id': forms.Select(attrs={'class': 'form-select'}),
            'question1': forms.TextInput(attrs={'class': 'form-control'}),
            'question2': forms.TextInput(attrs={'class': 'form-control'}),
            'question3': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'question1': '질문 1',
            'question2': '질문 2',
            'question3': '질문 3',
        }

class SurveyReplyForm(forms.ModelForm):
    class Meta:
        model = SurveyReply
        fields = ('reply1', 'reply2', 'reply3')

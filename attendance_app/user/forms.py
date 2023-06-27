from django import forms
from django.contrib.auth.models import User

from user.models import Student
from user.models import Division


# Forms
class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='비밀번호', help_text='')

    class Meta:
        model = User
        fields = ['username', 'password']
        labels = {
            'username': '사용자명',
            'password': '비밀번호',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = ''  # 도움말 텍스트 비움

class ClientForm(forms.ModelForm):
    GENDER_CHOICES = (
        ('M', '남자'),
        ('F', '여자'),
        ('O', '기타'),
    )

    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}), label='생년월일')
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}), label='성별')
    division = forms.ModelChoiceField(queryset=Division.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}), label='분반')

    class Meta:
        model = Student
        fields = ['name', 'birth_date', 'gender', 'division']
        labels = {
            'name': '이름',
            'birth_date': '생년월일',
            'gender': '성별',
            'division': '학과',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

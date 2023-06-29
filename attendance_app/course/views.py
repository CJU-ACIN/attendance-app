from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404

from course.models import Course
from user.models import Division

from course.forms import CourseForm
from survey.forms import SurveyForm


# Create your views here.
def course_list(request, pk):
    division = Division.objects.get(pk=pk)
    course = Course.objects.filter(division_name_id=pk)
    
    context = {
        'course': course,
        'division': division,
        
        }
    return render(request, 'course/course_list.html', context)


# 강좌 추가
def create_course(request):
    if request.method == 'POST':
        course_form = CourseForm(request.POST)
        survey_form = SurveyForm(request.POST)
        
        if course_form.is_valid() and survey_form.is_valid():
            # 코스 저장
            course = course_form.save()
            survey = survey_form.save(commit=False)
            
            survey.course_id_id = course.id
            survey_form.save()
  
            return redirect('user:division_list')  # 적절한 URL로 리다이렉트


    else:
        course_form = CourseForm()
        survey_form = SurveyForm()

    context = {
        'course_form': course_form,
        'survey_form': survey_form,
    }
    
    return render(request, 'course/create_course.html', context)


# 강좌 상세 페이지
def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    context = {'course': course}
    return render(request, 'course/course_detail.html', context)


# 강좌 수정
def edit_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('course:course_detail', pk=course.pk)
        
    else:
        form = CourseForm(instance=course)
    context = {'form': form, 'course':course}
    return render(request, 'course/edit_course.html', context)


# 강좌 삭제
def delete_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        course.delete()
        return redirect('course:course_list')  # Replace 'home' with the appropriate URL name
    
    context = {'course': course}
    return render(request, 'course/delete_course.html', context)
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.views.generic.edit import CreateView
from .models import Student
from .forms import StudentForm
from django.contrib import messages
from django.views.generic import TemplateView, ListView, CreateView, DetailView, UpdateView, DeleteView

# def home(request):
#     return HttpResponse("Hello World!")

def home_page(request):
    return render(request, 'fscohort/home.html')

class HomeView(TemplateView):
    template_name = 'fscohort/home.html'

def student_list(request):
    students = Student.objects.all()
    
    context = {
        'students' : students
    }

    return render(request, 'fscohort/student_list.html', context)

class StudentList(ListView):
    model = Student
    # template_name  # default app/student_list.html
    context_object_name = 'students'
    paginate_by = 1

def student_add(request):
    form = StudentForm()
    if request.method == 'POST':
        print(request.POST)
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student succesfully created ...')
            return redirect("list")
    context = {
        'form': form,
    }
    return render(request, 'fscohort/student_add.html', context)

class StudentCreate(CreateView):
    model = Student
    # fields = ('first_name')
    form_class = StudentForm
    template_name = 'fscohort/student_add.html'
    success_url = reverse_lazy('list')

def student_detail(request, id):
    student = Student.objects.get(id=id)
    context = {
        'student' : student
    }
    return render(request, 'fscohort/student_detail.html', context)

class StudentDetail(DetailView):
    model = Student

def student_update(request, id):
    student = get_object_or_404(Student, id=id)
    form = StudentForm(request.POST or None, instance=student)
    # if request.method == 'POST':
    #     form = StudentForm(request.POST, instance=student)
    if form.is_valid():
        form.save()
        return redirect("list")
    context = {
        'student': student,
        'form': form
    }
    return render(request, 'fscohort/student_update.html', context)

class StudentUpdate(UpdateView):
    model=Student
    form_class = StudentForm
    template_name = 'fscohort/student_update.html'  # app/student_form.html
    success_url = reverse_lazy('list') 

def student_delete(request, id):
    student = get_object_or_404(Student, id=id)
    if request.method == 'POST':
        student.delete()
        return redirect("list")

    context = {
        "student": student
    }

    return render(request, 'fscohort/student_delete.html', context)

class StudentDelete(DeleteView):
    model = Student
    template_name = 'fscohort/student_delete.html'  # default app/student_confirm_delete.html
    success_url = reverse_lazy('list')

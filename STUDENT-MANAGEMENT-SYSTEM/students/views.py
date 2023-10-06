from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render

from .models import Student
from .forms import StudentForm

# Create your views here.
def index(request):
  return render(request, 'students/index.html', {'students':Student.objects.all()})

def view_student(request, id):
  student = Student.objects.get(pk=id)
  return HttpResponseRedirect(reverse('index'))

def add(request):
  if request.method == 'POST':
    form = StudentForm(request.POST)
    if form.is_valid():
      new_student_number = form.cleaned_data['student_number']
      new_first_name = form.cleaned_data['first_name']
      new_last_name = form.cleaned_data['last_name']
      new_email = form.cleaned_data['email']
      new_field_of_study = form.cleaned_data['field_of_study']
      new_gpa = form.cleaned_data['gpa']

      new_student = Student(
        student_number = new_student_number,
        first_name = new_first_name,
        last_name = new_last_name,
        email = new_email,
        field_of_study = new_field_of_study,
        gpa = new_gpa,
      )
      new_student.save()
      return render(request, 'students/add.html',{'form': StudentForm(), 'success': True})
  else:
    form = StudentForm()
    return render(request, 'students/add.html',{'form': StudentForm()})
      
def edit(request, id):
  if request.method == 'POST':
    student = Student.objects.get(pk=id)
    form = StudentForm(request.POST, instance=student)
    if form.is_valid():
      form.save()
      return render(request, 'students/edit.html',{
        'form': form,
        'success': True
      })
  else:
    student = Student.objects.get(pk=id)
    form = StudentForm(instance=student)
    return render(request, 'students/edit.html', {
      'form': form
    })
  
def delete(request, id):
  if request.method == 'POST':
    student = Student.objects.get(pk=id)
    student.delete()
    return HttpResponseRedirect(reverse('index'))

from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

def generate_pdf(request, id):
    student = Student.objects.get(pk=id)
    template_path = 'students/pdf_template.html'
    context = {'student': student}

    # Create a Django response object with appropriate PDF headers
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{student.first_name}_{student.last_name}_info.pdf"'

    # Render the HTML template
    template = get_template(template_path)
    html = template.render(context)

    # Create the PDF
    pisa_status = pisa.CreatePDF(html, dest=response, encoding='utf-8')
    if pisa_status.err:
        return HttpResponse('Error generating PDF', content_type='text/plain')

    return response

  

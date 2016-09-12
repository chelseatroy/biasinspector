from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from .regression import predict_salaries
from .models import Employee
from .forms import EmployeeDataForm
import pandas as pd
from io import StringIO

def salaries(request):
    form = EmployeeDataForm()
    return render(request, 'salaries/salaries.html', {'form': form})

def enter_data(request):
    form = EmployeeDataForm(request.POST)
    if form.is_valid():
        employee_info = StringIO(form.cleaned_data['employee_info'])

        employee_data = pd.read_csv(employee_info)
        print employee_data

        employees = []

        employee_data.apply(
            employees.append(save_employee_from_row),
            axis=1
        )

        salary_model = predict_salaries(employees)
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('salaries:display_coefficients')) #, args=(salary_model.gender_coeff, etc))) #,

def display_coefficients(request):
    return render(request, 'salaries/employee_results.html') #, {'gender_coefficient': gender, 'ethnicity_coefficient': ethnicity}

def save_employee_from_row(employee_row):
    employee = Employee()
    employee.id = employee_row[0]
    employee.ethnicity = employee_row[1]
    employee.gender = employee_row[2]
    employee.age = employee_row[3]
    employee.years_experience = employee_row[4]
    employee.role = employee_row[5]
    return employee

# 2,red,f,12,2,engineer
# 2,green,g,14,4,designer
# 2,red,f,13,5,engineer
# 2,blue,f,12,1,developer
# 2,red,g,17,4,developer
# 2,green,f,12,4,engineer
# 2,red,g,11,2,designer
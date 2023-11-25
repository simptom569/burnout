from django.shortcuts import render
from .recognition import burnout


def main(request):
    employees_burnout = burnout.get_burnout_employees()
    context = {
        'employees_burnout': employees_burnout,
    }

    return render(request, 'main/main.html', context=context)
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import get_user_model
from .forms import ScheduleForm
from .models import Schedule, Address
from django.forms import modelformset_factory
from datetime import datetime, timedelta
from django.utils import timezone
from collections import defaultdict
from django.views.generic import TemplateView
from django.utils.translation import gettext_lazy as _
from django.http import JsonResponse
import json

User = get_user_model()

def is_staff(user):
    return user.is_staff

@login_required
def my_profile(request):
    user = request.user

    # Определяем текущую неделю
    today = datetime.today().date()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)

    # Получаем дату начала и конца недели из GET-параметров, если они есть
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    if start_date_str and end_date_str:
        try:
            start_of_week = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_of_week = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        except ValueError:
            pass  # Оставляем значения по умолчанию, если даты не в правильном формате

    # Фильтруем расписание по пользователю и дате
    schedules = Schedule.objects.filter(user=user, date__range=[start_of_week, end_of_week]).order_by('date')

    # Подсчитываем общее количество часов
    total_hours = 0
    for schedule in schedules:
        if schedule.start_time and schedule.end_time:
            start_time = datetime.combine(datetime.today(), schedule.start_time)
            end_time = datetime.combine(datetime.today(), schedule.end_time)
            total_hours += (end_time - start_time).seconds / 3600

    # Даты для кнопок предыдущей и следующей недели
    prev_week_start = start_of_week - timedelta(days=7)
    prev_week_end = end_of_week - timedelta(days=7)
    next_week_start = start_of_week + timedelta(days=7)
    next_week_end = end_of_week + timedelta(days=7)

    interval_dates = f'{start_of_week.strftime("%d.%m.%Y")} - {end_of_week.strftime("%d.%m.%Y")}'

    context = {
        'user': user,
        'schedules': schedules,
        'total_hours': total_hours,
        'start_of_week': start_of_week,
        'end_of_week': end_of_week,
        'prev_week_start': prev_week_start,
        'prev_week_end': prev_week_end,
        'next_week_start': next_week_start,
        'next_week_end': next_week_end,
        'interval_dates': interval_dates,
    }
    return render(request, 'graf/my_profile.html', context)


@login_required
@user_passes_test(is_staff)
def profile_list(request):
    users = User.objects.all()
    return render(request, 'graf/profile_list.html', {'users': users})


@login_required
@user_passes_test(is_staff)
def profile_detail(request, user_id):
    user = get_object_or_404(User, pk=user_id)

    # Определяем текущую неделю
    today = datetime.today().date()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)

    # Получаем дату начала и конца недели из GET-параметров, если они есть
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    if start_date_str and end_date_str:
        try:
            start_of_week = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_of_week = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        except ValueError:
            pass  # Оставляем значения по умолчанию, если даты не в правильном формате

    # Фильтруем расписание по пользователю и дате, сортируем по дате
    schedules = Schedule.objects.filter(user=user, date__range=[start_of_week, end_of_week]).order_by('date')

    # Подсчитываем общее количество часов
    total_hours = 0
    for schedule in schedules:
        if schedule.start_time and schedule.end_time:
            start_time = datetime.combine(datetime.today(), schedule.start_time)
            end_time = datetime.combine(datetime.today(), schedule.end_time)
            total_hours += (end_time - start_time).seconds / 3600

    # Даты для кнопок предыдущей и следующей недели
    prev_week_start = start_of_week - timedelta(days=7)
    prev_week_end = end_of_week - timedelta(days=7)
    next_week_start = start_of_week + timedelta(days=7)
    next_week_end = end_of_week + timedelta(days=7)

    context = {
        'user': user,
        'schedules': schedules,
        'total_hours': total_hours,
        'start_of_week': start_of_week,
        'end_of_week': end_of_week,
        'prev_week_start': prev_week_start,
        'prev_week_end': prev_week_end,
        'next_week_start': next_week_start,
        'next_week_end': next_week_end,
    }
    return render(request, 'graf/profile_detail.html', context)


@login_required
@user_passes_test(is_staff)
def create_weekly_schedule(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    ScheduleFormSet = modelformset_factory(Schedule, form=ScheduleForm, extra=7)

    if request.method == 'POST':
        formset = ScheduleFormSet(request.POST, queryset=Schedule.objects.none())
        if formset.is_valid():
            schedules = formset.save(commit=False)
            for schedule in schedules:
                schedule.user = user
                if not schedule.address:
                    schedule.address = "Выходной"
                schedule.save()
            return redirect('graf:profile_detail', user_id=user.id)
    else:
        formset = ScheduleFormSet(queryset=Schedule.objects.none())

    return render(request, 'graf/create_weekly_schedule.html', {'formset': formset, 'user': user})

@login_required
@user_passes_test(is_staff)
def edit_schedule(request, pk):
    schedule = get_object_or_404(Schedule, pk=pk)
    if request.method == 'POST':
        form = ScheduleForm(request.POST, instance=schedule)
        if form.is_valid():
            form.save()
            return redirect('graf:profile_detail', user_id=schedule.user.id)
    else:
        form = ScheduleForm(instance=schedule)
    return render(request, 'graf/edit_schedule.html', {'form': form, 'schedule': schedule})

@login_required
@user_passes_test(is_staff)
def delete_schedule(request, pk):
    schedule = get_object_or_404(Schedule, pk=pk)
    user_id = schedule.user.id
    if request.method == 'POST':
        schedule.delete()
        return redirect('graf:profile_detail', user_id=user_id)
    return render(request, 'graf/delete_schedule.html', {'schedule': schedule})

@login_required
@user_passes_test(lambda u: u.is_staff)
def all_addresses_schedule(request):
    # Получаем текущую дату
    today = timezone.now().date()
    
    # Вычисляем начало и конец текущей недели
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    
    # Проверяем, есть ли параметры start_date и end_date в GET запросе
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')
    
    # Если параметры start_date и end_date заданы, пытаемся преобразовать их в даты
    if start_date_str and end_date_str:
        try:
            start_of_week = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_of_week = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        except ValueError:
            pass  # Оставляем значения по умолчанию, если даты не в правильном формате

    # Даты для кнопок предыдущей и следующей недели
    prev_week_start = start_of_week - timedelta(days=7)
    prev_week_end = end_of_week - timedelta(days=7)
    next_week_start = start_of_week + timedelta(days=7)
    next_week_end = end_of_week + timedelta(days=7)
    
    # Получаем все адреса
    addresses = Address.objects.all()
    
    # Создаем словарь для хранения расписаний по адресам и пользователям
    schedules_by_address = defaultdict(lambda: defaultdict(dict))
    
    # Фильтруем расписания по адресам и заданному диапазону дат
    schedules = Schedule.objects.filter(address__in=addresses, date__range=[start_of_week, end_of_week])
    
    # Заполняем словарь расписаний
    for schedule in schedules:
        day_of_week = schedule.date.strftime('%A')
        address_name = schedule.address.name
        user_name = schedule.user.get_full_name()
        schedules_by_address[address_name][user_name][day_of_week] = {
            'start_time': schedule.start_time.strftime('%H:%M') if schedule.start_time else '-',
            'end_time': schedule.end_time.strftime('%H:%M') if schedule.end_time else '-',
        }
    
    # Преобразуем данные в формат JSON
    schedules_json = json.dumps(schedules_by_address)
    
    # Вычисляем даты для отображения интервала текущей недели
    interval_dates = f'{start_of_week.strftime("%d.%m.%Y")} - {end_of_week.strftime("%d.%m.%Y")}'
    
    # Получаем всех пользователей и их общее количество часов на текущую неделю
    users = User.objects.all()
    users_hours = {}
    for user in users:
        user_schedules = Schedule.objects.filter(user=user, date__range=[start_of_week, end_of_week])
        total_hours = 0
        for schedule in user_schedules:
            if schedule.start_time and schedule.end_time:
                start_time = datetime.combine(datetime.today(), schedule.start_time)
                end_time = datetime.combine(datetime.today(), schedule.end_time)
                total_hours += (end_time - start_time).seconds / 3600
        users_hours[user.get_full_name()] = total_hours
    
    # Отображаем шаблон с расписанием
    return render(request, 'graf/all_addresses_schedule.html', {
        'schedules_json': schedules_json,
        'interval_dates': interval_dates,
        'start_of_week': start_of_week,
        'end_of_week': end_of_week,
        'prev_week_start': prev_week_start,
        'prev_week_end': prev_week_end,
        'next_week_start': next_week_start,
        'next_week_end': next_week_end,
        'users_hours': users_hours,
    })
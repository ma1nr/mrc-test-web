from django.shortcuts import render, get_object_or_404
from .models import Schedule, Group, Teacher, Subject
from datetime import datetime, time, timedelta
import locale

LESSON_TIMES = [
    {'num': 1, 'start': time(8, 0), 'end': time(9, 40), 'name': '1 пара'},
    {'num': 2, 'start': time(9, 50), 'end': time(11, 30), 'name': '2 пара'},
    {'num': 3, 'start': time(11, 50), 'end': time(13, 30), 'name': '3 пара'},
    {'num': 4, 'start': time(13, 40), 'end': time(15, 20), 'name': '4 пара'},
    {'num': 5, 'start': time(15, 40), 'end': time(17, 20), 'name': '5 пара'},
    {'num': 6, 'start': time(17, 30), 'end': time(19, 10), 'name': '6 пара'},
    {'num': 7, 'start': time(19, 20), 'end': time(21, 0), 'name': '7 пара'},
]

DAYS_FULL = {
    'Пн': 'Понедельник',
    'Вт': 'Вторник',
    'Ср': 'Среда',
    'Чт': 'Четверг',
    'Пт': 'Пятница',
    'Сб': 'Суббота',
}

DAYS_MAPPING = {
    'Понедельник': 'Пн',
    'Вторник': 'Вт',
    'Среда': 'Ср',
    'Четверг': 'Чт',
    'Пятница': 'Пт',
    'Суббота': 'Сб',
}


def schedule_view(request):
    try:
        locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
    except:
        locale.setlocale(locale.LC_TIME, 'Russian_Russia.1251')

    today = datetime.now() + timedelta(hours=3)
    now_time = today.time()

    group_id_raw = request.GET.get("group")
    date_mode = request.GET.get("date_mode", "today")
    custom_date = request.GET.get("custom_date")

    selected_group = int(group_id_raw) if group_id_raw and group_id_raw.isdigit() else None

    DEFAULT_GROUP_ID = 19

    if selected_group is None:
        selected_group = DEFAULT_GROUP_ID

    if date_mode == "today":
        selected_date = today
    elif date_mode == "tomorrow":
        selected_date = today + timedelta(days=1)
    elif date_mode == "custom" and custom_date:
        selected_date = datetime.strptime(custom_date, "%Y-%m-%d")
    else:
        selected_date = today

    selected_day = DAYS_MAPPING.get(selected_date.strftime('%A').capitalize(), "Пн")
    selected_day_full = DAYS_FULL[selected_day]

    groups = Group.objects.all()

    schedule_qs = Schedule.objects.filter(day_of_week=selected_day)
    if selected_group:
        schedule_qs = schedule_qs.filter(group_id=selected_group)

    schedule_qs = schedule_qs.order_by("time")

    duration_order = {'half1': 0, 'full': 1, 'half2': 2}

    schedule_table = []
    for lesson_time in LESSON_TIMES:
        slot_lessons = [
            s for s in schedule_qs
            if lesson_time['start'] <= s.time < lesson_time['end']
        ]
        slot_lessons.sort(key=lambda s: duration_order.get(s.duration, 1))

        is_now = (date_mode == "today") and (lesson_time['start'] <= now_time < lesson_time['end'])

        schedule_table.append({
            'lesson_num': lesson_time['num'],
            'lesson_name': lesson_time['name'],
            'time_range': f"{lesson_time['start'].strftime('%H:%M')} - {lesson_time['end'].strftime('%H:%M')}",
            'lessons': slot_lessons,
            'is_now': is_now,
        })

    selected_group_obj = Group.objects.filter(id=selected_group).first() if selected_group else None

    return render(request, "schedule/schedule.html", {
        "groups": groups,
        "schedule_table": schedule_table,
        "selected_group": selected_group,
        "selected_group_obj": selected_group_obj,
        "selected_day": selected_day,
        "selected_day_full": selected_day_full,
        "date_mode": date_mode,
        "custom_date": custom_date,
        "today_date": selected_date.strftime("%d.%m.%Y"),
    })


def teachers_list(request):
    teachers = Teacher.objects.all().order_by('name')
    return render(request, 'schedule/teachers.html', {'teachers': teachers})


def subjects_list(request):
    subjects = Subject.objects.all().order_by('title')
    return render(request, 'schedule/subjects.html', {'subjects': subjects})


def groups_list(request):
    groups = Group.objects.all().order_by('name')
    return render(request, 'schedule/groups.html', {'groups': groups})

def group_detail(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    schedule = Schedule.objects.filter(group=group).order_by('day_of_week', 'time')

    schedule_by_day = {}
    for s in schedule:
        day = s.get_day_of_week_display()
        schedule_by_day.setdefault(day, []).append(s)

    return render(request, 'schedule/group_detail.html', {
        'group': group,
        'schedule_by_day': schedule_by_day,
    })


def subject_detail(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    groups = Group.objects.filter(schedule__subject=subject).distinct()

    return render(request, 'schedule/subject_detail.html', {
        'subject': subject,
        'groups': groups,
    })


def teacher_detail(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    schedule = Schedule.objects.filter(teacher=teacher).order_by('day_of_week', 'time')

    schedule_by_day = {}
    for s in schedule:
        day = s.get_day_of_week_display()
        schedule_by_day.setdefault(day, []).append(s)

    return render(request, 'schedule/teacher_detail.html', {
        'teacher': teacher,
        'schedule_by_day': schedule_by_day,
    })

def matrix_view(request):

    try:
        locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
    except:
        locale.setlocale(locale.LC_TIME, 'Russian_Russia.1251')

    today = datetime.now() + timedelta(hours=3)

    date_mode = request.GET.get("date_mode", "today")
    custom_date = request.GET.get("custom_date")

    if date_mode == "today":
        selected_date = today
    elif date_mode == "tomorrow":
        selected_date = today + timedelta(days=1)
    elif date_mode == "custom" and custom_date:
        selected_date = datetime.strptime(custom_date, "%Y-%m-%d")
    else:
        selected_date = today

    selected_day = DAYS_MAPPING.get(selected_date.strftime('%A').capitalize(), "Пн")

    groups = Group.objects.all().order_by('name')
    schedule_qs = Schedule.objects.filter(day_of_week=selected_day).order_by('time')

    duration_order = {'half1': 0, 'full': 1, 'half2': 2}

    matrix = []

    for group in groups:
        row = {'group': group, 'slots': []}

        group_lessons = schedule_qs.filter(group=group)

        for lt in LESSON_TIMES:
            cell_lessons = [
                s for s in group_lessons
                if lt['start'] <= s.time < lt['end']
            ]
            cell_lessons.sort(key=lambda s: duration_order.get(s.duration, 1))

            row['slots'].append({
                'num': lt['num'],
                'start': lt['start'],
                'end': lt['end'],
                'name': lt['name'],
                'lessons': cell_lessons,
            })

        matrix.append(row)

    return render(request, 'schedule/matrix.html', {
        'matrix': matrix,
        'date_mode': date_mode,
        'custom_date': custom_date,
        'selected_date': selected_date.strftime("%d.%m.%Y"),
        'selected_day': selected_day,
        'selected_day_full': DAYS_FULL[selected_day],
    })





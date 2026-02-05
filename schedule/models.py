from django.db import models


class Teacher(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Subject(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Group(models.Model):
    name = models.CharField(max_length=50)
    specialty = models.CharField(max_length=255, blank=True)
    curator = models.ForeignKey(
        Teacher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='curated_groups'
    )

    def __str__(self):
        return self.name


class Schedule(models.Model):
    DAYS = [
        ('Пн', 'Понедельник'),
        ('Вт', 'Вторник'),
        ('Ср', 'Среда'),
        ('Чт', 'Четверг'),
        ('Пт', 'Пятница'),
        ('Сб', 'Суббота'),
    ]

    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    day_of_week = models.CharField(max_length=10, choices=DAYS)

    duration = models.CharField(
        max_length=10,
        choices=[
            ('half1', '1 половина'),
            ('half2', '2 половина'),
            ('full', 'Полная пара'),
        ],
        default='full'
    )

    time = models.TimeField()

    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)

    classroom_number = models.CharField(max_length=20, verbose_name="Номер аудитории", blank=True)
    classroom_floor = models.IntegerField(verbose_name="Этаж", blank=True, null=True)
    building = models.CharField(max_length=50, verbose_name="Корпус", blank=True)

    def __str__(self):
        return f"{self.group} - {self.subject} ({self.day_of_week})"

    def get_classroom_full(self):
        parts = []
        if self.building:
            parts.append(f"Корпус {self.building}")
        if self.classroom_number:
            parts.append(f"ауд. {self.classroom_number}")
        if self.classroom_floor:
            parts.append(f"{self.classroom_floor} этаж")
        return ", ".join(parts) if parts else "Не указана"

    class Meta:
        ordering = ['day_of_week', 'time']

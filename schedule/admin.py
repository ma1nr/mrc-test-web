from django.contrib import admin
from .models import Teacher, Subject, Group, Schedule

try:
    admin.site.unregister(Teacher)
    admin.site.unregister(Subject)
    admin.site.unregister(Group)
    admin.site.unregister(Schedule)
except admin.sites.NotRegistered:
    pass

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    search_fields = ('title',)


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):

    list_display = ('group', 'subject', 'teacher', 'day_of_week', 'time',
                    'building', 'classroom_number', 'classroom_floor')
    list_filter = ('day_of_week', 'group', 'building')
    search_fields = ('group__name', 'subject__title', 'teacher__name', 'classroom_number')

    def classroom_info(self, obj):
        return obj.get_classroom_full()

    classroom_info.short_description = 'Аудитория'
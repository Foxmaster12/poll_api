from django.contrib import admin
from .models import *


class AnswerInline(admin.TabularInline):
    extra = 1
    model = Choice


class QuestionAdmin(admin.ModelAdmin):

    inlines = [
        AnswerInline,
    ]


class PollAdmin(admin.ModelAdmin):
    readonly_fields = ("poll_start", )


admin.site.register(Poll, PollAdmin)
admin.site.register(Question, QuestionAdmin)

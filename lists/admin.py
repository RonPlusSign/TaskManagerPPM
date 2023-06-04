from django.contrib import admin

from lists.models import *

admin.site.register(TaskList)
admin.site.register(Task)
admin.site.register(TaskComment)

from django.contrib import admin

from checker.models import KeywordsChecker, Projects
from simple_history.admin import SimpleHistoryAdmin

class KeywordHistoryAdmin(SimpleHistoryAdmin):
    list_display = ["keyword", "position",]
    history_list_display = ["position", "change", "best"]
    # search_fields = ['name', 'user__username']

# Register your models here.
admin.site.register(Projects)
# admin.site.register(Domain)
admin.site.register(KeywordsChecker, KeywordHistoryAdmin)

# class ProjectsInline(admin.TabularInline):
#     model = Domain


# class DomainAdmin(admin.ModelAdmin):
#     inlines = [ProjectsInline]

# admin.site.register(Poll, )

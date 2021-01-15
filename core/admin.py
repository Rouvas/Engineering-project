from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from core.admin_actions import users_disable, users_enable
from core.models import User, Organization, WorkPlace, Post, Person, WorkTime

from import_export.admin import ImportExportModelAdmin


class UserAdmin(DefaultUserAdmin):
    list_display = ('email', 'name', 'is_active', 'is_superuser', 'is_staff', 'token_field')
    list_filter = ('is_active', 'is_superuser', 'is_staff', )

    search_fields = ('email', 'name')
    ordering = ('id',)

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2'),
        }),
    )
    fieldsets = (
        (None, {'fields': ('email', 'name', 'password')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', )}),
    )

    actions = [users_disable, users_enable]

    def token_field(self, obj):
        return obj.auth_tokens.first()
    token_field.short_description = 'REST-токен'


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('owner', 'name', 'phone', 'person_count')

    def person_count(self, obj):
        return obj.persons.count()
    person_count.short_description = 'Сотрудников'


class WorkPlaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'organization', 'person_count')
    list_filter = ('organization', )

    def person_count(self, obj):
        return obj.persons.count()
    person_count.short_description = 'Сотрудников'


class PostAdmin(admin.ModelAdmin):
    list_display = ('name', 'organization', 'work_place')
    list_filter = ('organization', 'work_place')


class PersonAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'post', 'status', 'phone_href')
    list_filter = ('organization', 'work_place', 'post', 'status', )
    search_fields = ('first_name', 'last_name', 'middle_name', 'phone', 'email', 'comment')

    def phone_href(self, obj):
        return format_html(
            '<a href="tel:{}">{}</a>',
            obj.phone,
            obj.phone,
        )

    phone_href.short_description = 'Телефон'


class WorkTimeAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('person', 'start_from', 'ended_at')
    list_filter = ('person', 'start_from', 'ended_at')


admin.site.register(User, UserAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(WorkPlace, WorkPlaceAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(WorkTime, WorkTimeAdmin)

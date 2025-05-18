from django.contrib import admin

# Register your models here.
admin.site.site_header = "Talana Trivia Admin"
admin.site.site_title = "Talana Trivia Admin Portal"
admin.site.index_title = "Welcome to the Talana Trivia Admin Portal"
from .models import User, Question, Option, Trivia, UserAnswer
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'role', 'mmr')
    list_filter = ('role',)
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'role')}),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role')}
        ),
    )
    search_fields = ('username',)
    ordering = ('username',)


    
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'difficulty')
    search_fields = ('text',)
    list_filter = ('difficulty',)
    ordering = ('difficulty',)

class OptionAdmin(admin.ModelAdmin):
    list_display = ('text', 'is_correct', 'question')
    search_fields = ('text',)
    list_filter = ('is_correct',)
    ordering = ('is_correct',)

class TriviaAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    ordering = ('name',)


class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ('user', 'trivia', 'question', 'selected_option', 'is_correct')
    search_fields = ('user__username', 'trivia__name', 'question__text')
    list_filter = ('is_correct',)
    ordering = ('user', 'trivia')


admin.site.register(User, UserAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Option, OptionAdmin)
admin.site.register(Trivia, TriviaAdmin)
admin.site.register(UserAnswer, UserAnswerAdmin)

from django.contrib import admin
from .models import (
	Category, Project, Donation, Update, ProjectReport, UpdateImage, Follow, BankDetail, Bank, PasswordReset,
	SuccessStory, EnquiryContact, WithdrawRequest
)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created')
    prepopulated_fields = {'slug': ['name']}
    list_filter = ['name']
    search_fields = ('name',)
    list_per_page = 20

admin.site.register(Category, CategoryAdmin)


class ProjectAdmin(admin.ModelAdmin):
	list_display = ('title', 'goal', 'is_approved', 'is_featured', 'created')
	prepopulated_fields = {'slug': ['title']}
	list_filter = ['title', 'created']
	search_fields = ('author__first_name', 'author__last_name', 'title')
	list_editable = ('is_approved', 'is_featured')
	list_per_page = 20

admin.site.register(Project, ProjectAdmin)


class DonationAdmin(admin.ModelAdmin):
	list_display = ('project', 'name', 'amount', 'date')
	list_filter = ['project', 'date', 'is_approved']
	search_fields = ('name__first_name', 'name__last_name', 'amount')
	list_per_page = 20


admin.site.register(Donation, DonationAdmin)

admin.site.register(PasswordReset)


class ProjectUpdateAdmin(admin.ModelAdmin):
	list_display = ('date', 'project', 'title', 'is_approved')
	list_filter = ['date', 'project', 'is_approved']
	search_fields = ('title',)
	list_per_page = 20
	list_editable = ('is_approved',)
	list_display_links = ('project', 'title',)

admin.site.register(Update, ProjectUpdateAdmin)


class ProjectReportAdmin(admin.ModelAdmin):
	list_display = ('date', 'author', 'project', 'title')
	list_filter = ['date', 'project', 'author']
	search_fields = ('author__first_name','author__last_name' 'title')
	list_per_page = 20

admin.site.register(ProjectReport, ProjectReportAdmin)


class UpdateImagesAdmin(admin.ModelAdmin):
	list_display = ('update', 'image', 'date')
	list_filter = ['date']
	list_per_page = 20

admin.site.register(UpdateImage, UpdateImagesAdmin)


class FollowerAdmin(admin.ModelAdmin):
	list_display = ('project', 'follower', 'created')
	list_filter = ['project', 'created']
	list_per_page = 20

admin.site.register(Follow, FollowerAdmin)


class BankDetailAdmin(admin.ModelAdmin):
	list_display = ('user', 'bank')
	list_filter = ['bank']
	list_per_page = 20

admin.site.register(BankDetail, BankDetailAdmin)


admin.site.register(Bank)


class SuccessStoryAdmin(admin.ModelAdmin):
	list_display = ('project', 'is_approved', 'is_featured', 'created')
	list_filter = ['is_approved', 'created']
	list_per_page = 20
	list_editable = ('is_approved', 'is_featured')

admin.site.register(SuccessStory, SuccessStoryAdmin)


class EnquiryAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'f_name', 'l_name')
    search_fields = ('email', 'f_name', 'l_name', 'f_name', 'l_name')
    list_display_links = ('id', 'email',)

admin.site.register(EnquiryContact, EnquiryAdmin)


class WithdrawRequestAdmin(admin.ModelAdmin):
	list_display = ('id', 'user', 'project', 'amount')
	search_fields = ('project', 'amount')
	list_per_page = 20
	list_display_links = ('project',)

admin.site.register(WithdrawRequest, WithdrawRequestAdmin)



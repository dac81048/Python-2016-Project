from django.contrib import admin
from .models import *

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id','first_name','last_name','address','email','password','mobile_number','user_type','wish_to_be_worker')

class AdminAdmin(admin.ModelAdmin):
    list_display = ('id','first_name','last_name','email','password','mobile_number','user_type')

class WorkerAdmin(admin.ModelAdmin):
    list_display = ('id','worker','status')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','category_name')

class JobAdmin(admin.ModelAdmin):
    list_display = ('id','job_description','worker_id','job_status')

class EstimationAdmin(admin.ModelAdmin):
    list_display = ('id','total_cost')

class Services_RequestAdmin(admin.ModelAdmin):
    list_display = ('id','service_request','service_dateTime')

class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('id','job_datetime','total_cost')

class QueryAdmin(admin.ModelAdmin):
    list_display = ('id','query_dateTime','query_description','status')

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('id','feedback_description')

admin.site.register(Customer,CustomerAdmin)
admin.site.register(Admin,AdminAdmin)
admin.site.register(Worker,WorkerAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Job,JobAdmin)
admin.site.register(Estimation,EstimationAdmin)
admin.site.register(Services_Request,Services_RequestAdmin)
admin.site.register(Invoice,InvoiceAdmin)
admin.site.register(Query,QueryAdmin)
admin.site.register(Feedback,FeedbackAdmin)

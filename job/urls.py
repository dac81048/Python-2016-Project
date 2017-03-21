from django.contrib.auth.views import login,logout,password_reset,password_reset_done
from django.conf.urls import url
from . import views

# ,password_reset_confirm,password_reset_complete
# #for use of job:view_name
app_name='job'

urlpatterns = [
    url(r'^index/', views.index , name="index"),
    url(r'^$', views.LogInView.as_view() , name="login"),
    url(r'^(?P<email>[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,4})/(?P<confirmation_code>[0-9]+)$', views.LogInView.as_view() , name="LogIn"),
    url(r'^login/', views.LogInView.as_view() , name="login"),
    # url(r'^login/password_recovery/$',views.CustomePasswordRecovery.as_view(), name = 'password_recovery'),
    url(r'^services/', views.ServiceRequestView.as_view() , name="services"),
    url(r'^signup/', views.SignUp.as_view() , name="signup"),
    url(r'^timesheet/', views.calender , name="timesheet"),


    # url(r'^reset-password/$',password_reset, name="reset_password"),
    # url(r'^reset-password/done/$',password_reset_done, name = "reset_password_done"),
    # url(r'^reset-password/confirm/(?P<uidb64>[0-9A-Za-z]+)/(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm', name='password_reset_confirm'),
    # url(r'^reset_password/complete/$',password_reset_complete, name = "password_reset_complete"),

    # (r'^resetpassword/$', 'django.contrib.auth.views.password_reset', name="reset_password"),
    # (r'^resetpassword/passwordsent/$', 'django.contrib.auth.views.password_reset_done', name='password_reset_done'),
    # (r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>,+)/$', 'django.contrib.auth.views.password_reset_confirm', name="password_reset_confirm"),
    # (r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete', name="password_reset_complete"),
    url(r'^forget_password/', views.Forget_passwordView.as_view(), name="forget_password"),
    url(r'^otp/', views.OtpView.as_view(), name="otp"),
    url(r'^reset_password/', views.Reset_passwordView.as_view(), name="reset_password"),

    url(r'^logout/', views.logout , name="logout"),
    url(r'^query/', views.QueryView.as_view() , name="query"),
    url(r'^feedback/', views.FeedbackView.as_view() , name="feedback"),
    url(r'^invoice/', views.invoice_all , name="invoice"),
    url(r'^profile/', views.profile , name="profile"),
    url(r'^(?P<job_id>[0-9]+)/invoices/$', views.invoice_single , name="invoices"),
    url(r'^service/$', views.services , name="service"),
    url(r'^(?P<cust_id>[0-9]+)/add_worker/$', views.add_worker.as_view(), name="add_worker"),
    url(r'^(?P<cust_id>[0-9]+)/reject_worker/$', views.reject_worker, name="reject_worker"),
    url(r'^(?P<job_id>[0-9]+)/accept_job/$', views.accept_job, name="accept_job"),
    url(r'^(?P<job_id>[0-9]+)/reject_job/$', views.reject_job, name="reject_job"),
    url(r'^updated_job/$', views.updated_job_approvel, name="updated_job"),
    url(r'^(?P<job_id>[0-9]+)/admin_report_submit/$', views.admin_report_submit, name="admin_report_submit"),
    url(r'^(?P<job_id>[0-9]+)/submit_job/$', views.submit_job.as_view(), name="submit_job"),
    url(r'^(?P<job_id>[0-9]+)/report_job/$', views.report_job.as_view(), name="report_job"),
    url(r'^queries/$', views.queries , name="queries"),
    url(r'^approvel/$', views.job_approvel , name="approvel"),
    url(r'^my_job/$', views.worker_jobs , name="my_job"),
    url(r'^tobeworker/$', views.to_be_worker , name="tobeworker"),
    url(r'^wishes_worker/$', views.wishes_worker , name="wishes_worker"),
    url(r'^custquery/$', views.CustQuery , name="custquery"),
    url(r'^admin_job_report/$', views.admin_job_report , name="admin_job_report"),
    url(r'^worker/$',views.WorkerView,name="worker"),
    url(r'^customer/$',views.CustomerView,name="customer"),
    url(r'^(?P<cust_id>[0-9]+)/customer_data/$',views.customer_data,name="customer_data"),
    url(r'^(?P<ser_id>[0-9]+)/newjob/$',views.NewJob.as_view(),name="newjob"),
    url(r'^(?P<que_id>[0-9]+)/responsequery/$',views.ResponseQuery.as_view(),name="responsequery"),
    url(r'^(?P<ser_id>[0-9]+)/estimate/$',views.Estimate.as_view(),name="estimate"),
    url(r'^job/$',views.JobView,name="job"),
]

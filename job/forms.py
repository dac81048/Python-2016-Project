from django import forms
from .models import *

class AddCustomer(forms.ModelForm):
	password=forms.CharField(widget=forms.PasswordInput)
	confirm_password=forms.CharField(widget=forms.PasswordInput)
	class Meta:
		model = Customer
		fields= ['first_name','last_name','mobile_number','email','address','profile_pic','password','confirm_password']

class Add_Customer(forms.ModelForm):
	password=forms.CharField(widget=forms.PasswordInput)
	class Meta:
		model = Customer
		fields= ['email','password']

class ServiceRequestForm(forms.ModelForm):
	class Meta:
		model=Services_Request
		fields= ['service_request','customer_id']

class QueryForm(forms.ModelForm):
	class Meta:
		model=Query
		fields= ['query_description','customer_id']

class FeedbackForm(forms.ModelForm):
	class Meta:
		model=Feedback
		fields= ['feedback_description','customer_id']

class Newjob(forms.ModelForm):
	class Meta:
		model=Job
		fields=['worker_id','customer_id','service_id','Estimate_id','job_start_datetime','job_description','location']

class Response(forms.ModelForm):
	class Meta:
		model=Query
		fields=['query_response','customer_id','status']


class estimate(forms.ModelForm):
	class Meta:
		model=Estimation
		fields=['service_id','customer_id','trasportation_charge','visit_charge','extra_cost']

class AddWorker(forms.ModelForm):
	class Meta:
		model=Worker
		fields=['worker','category_id']

class submit_job(forms.ModelForm):
	password=forms.CharField(widget=forms.PasswordInput)
	class Meta:
		model = Customer
		fields= ['password']

class report_job(forms.ModelForm):
	class Meta:
		model = Job
		fields= ['job_report']

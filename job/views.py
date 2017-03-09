from django.shortcuts import render
from django.views import generic,View
from django.views.generic import CreateView,UpdateView
from django.contrib.auth import authenticate,login
from .forms import *
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.core.mail import EmailMultiAlternatives
from django.contrib import messages
import datetime

def missed_job():
	all_jobs_missed=Job.objects.all()
	for job in all_jobs_missed:
			if job.job_start_datetime<datetime.date.today() and job.job_status=="pending":
					job.job_status="missed"
					job.save()

def index(request):
		if 'logs' in request.session:
			missed_job()
			all_queries=Query.objects.filter(status="pending")
			if 'Admin' in request.session['dash']:
				all_pending_jobs=Job.objects.filter(job_status="pending").order_by('job_start_datetime')
				all_ongoing_jobs=all_pending_jobs.filter(job_start_datetime=datetime.date.today()).order_by('job_start_datetime')
				all_completed_jobs=Job.objects.filter(job_status="completed").order_by('job_start_datetime')
				tomorrows_job = Job.objects.filter(job_start_datetime=datetime.date.today() + datetime.timedelta(days=1)).order_by('job_start_datetime')

			if 'Worker' in request.session['dash']:
				worker_id = Worker.objects.get(worker = request.session['id'])
				worker_data = Job.objects.filter(worker_id=worker_id)
				all_pending_jobs=worker_data.filter(job_status="pending").order_by('job_start_datetime')
				all_ongoing_jobs=all_pending_jobs.filter(job_start_datetime=datetime.date.today()).order_by('job_start_datetime')
				all_completed_jobs=worker_data.filter(job_status="completed").order_by('job_start_datetime')
				tomorrows_job = worker_data.filter(job_start_datetime=datetime.date.today() + datetime.timedelta(days=1)).order_by('job_start_datetime')

			if 'Customer' in request.session['dash']:
				customer_id = Customer.objects.get(id = request.session['id'])
				customer_data = Job.objects.filter(customer_id=customer_id)

				all_pending_jobs=customer_data.filter(job_status="pending").order_by('job_start_datetime')
				all_ongoing_jobs=all_pending_jobs.filter(job_start_datetime=datetime.date.today()).order_by('job_start_datetime')
				all_completed_jobs=customer_data.filter(job_status="completed").order_by('job_start_datetime')
				tomorrows_job = customer_data.filter(job_start_datetime=datetime.date.today() + datetime.timedelta(days=1)).order_by('job_start_datetime')

			return render(request,'job/index.html',{'all_queries':all_queries,'count':all_queries.count(),'all_pending_jobs':all_pending_jobs,'today_job_count':all_ongoing_jobs.count(),'all_ongoing_jobs':all_ongoing_jobs,'tomorrows_job':tomorrows_job,'tomorrows_job_count':tomorrows_job.count(),'all_completed_jobs':all_completed_jobs})
		else:
			return HttpResponseRedirect('/login')

#customer wishes to be a worker
def to_be_worker(request):
		if 'logs' in request.session:
			cust=Customer.objects.get(id=request.session['id'])
			cust.wish_to_be_worker=True
			cust.save()
			return render(request,'job/wish.html',{'cust':cust,})
		else:
			return HttpResponseRedirect('/index')

def view_data(request,job_id):
	if 'logs' in request.session:
		job=Job.objects.get(id=job_id)
		return render(request,'job/result.html',{'jobs':job,})
	else:
		return HttpResponseRedirect('/login')

def view_job(request,job_id):
	if 'logs' in request.session:
		job=Job.objects.get(id=job_id)
		return render(request,'job/view_job.html',{'jobs':job,})
	else:
		return HttpResponseRedirect('/login')

def invoice_all(request):
	invoice = Invoice.objects.all()
	missed_job()
	if 'logs' in request.session:
		return render(request,'job/invoice_all.html',{'invoice':invoice,})
	else:
		return HttpResponseRedirect('/login')

def invoice_single(request,job_id):
	if 'logs' in request.session:
		job=Job.objects.get(id=job_id)
		return render(request,'job/result.html',{'jobs':job,})
	else:
		return HttpResponseRedirect('/login')

#list of all wishes
def wishes_worker(request):
		if 'logs' in request.session:
			missed_job()
			all_cust=Customer.objects.filter(wish_to_be_worker=True)
			cust=all_cust.filter(user_type="Customer")
			return render(request,'job/wishes.html',{'cust':cust,})
		else:
			return HttpResponseRedirect('/login')

def job_approvel(request):
		if 'logs' in request.session:
			all_jobs=Job.objects.filter(customer_id=request.session['id'])
			all_jobs=all_jobs.filter(customer_approvel=False)
			return render(request,'job/cust_approvel.html',{'all_jobs':all_jobs,})
		else:
			return HttpResponseRedirect('/login')

def updated_job_approvel(request):
		if 'logs' in request.session:
			request.session['url']="update_job"
			all_jobs=Job.objects.all()
			all_jobs=all_jobs.filter(report_customer_approvel=False)
			return render(request,'job/report_approvel.html',{'all_jobs':all_jobs,})
		else:
			return HttpResponseRedirect('/login')

def accept_job(request,job_id):
		if 'logs' in request.session:
			job=Job.objects.get(id=job_id)
			job.customer_approvel=True
			job.report_customer_approvel=True
			job.save()
			return HttpResponseRedirect('/approvel')
		else:
			return HttpResponseRedirect('/login')


def reject_job(request,job_id):
		if 'logs' in request.session:
			job=Job.objects.get(id=job_id)
			service=Services_Request.objects.get(id=job.service_id.id)
			service.job_created=False
			job.delete()
			service.save()
			return HttpResponseRedirect('/approvel')
		else:
			return HttpResponseRedirect('/login')

class submit_job(CreateView,View):
	form_class = submit_job
	template_name='job/submit_job.html'

	def get(self,request,job_id):
		form=self.form_class(None)
		job=Job.objects.get(id=job_id)
		if 'logs' in request.session:
			if job.job_start_datetime <= datetime.date.today():
				return render(request,self.template_name,{'form':form})
			else:
				messages.warning(request,'Job is not Scheduled Yet.')
				return HttpResponseRedirect('/my_job')
		else:
			return HttpResponseRedirect('/login')

	def post(self,request,job_id):
		form=self.form_class(request.POST)
		if form.is_valid():
			user=form.save(commit=False)
			job=Job.objects.get(id=job_id)
			cust=Customer.objects.get(id=job.customer_id.id)
			password=form.cleaned_data['password']
			if password == cust.password:
				job.job_status="completed"
				job.job_end_datetime=timezone.now()
				job.save()
				invoice=Invoice()
				invoice.service_id=job.service_id
				invoice.customer_id=job.customer_id
				invoice.job_id=job
				invoice.job_datetime=job.job_end_datetime
				invoice.trasportation_charge=job.Estimate_id.trasportation_charge
				invoice.visit_charge=job.Estimate_id.visit_charge
				invoice.extra_cost=job.Estimate_id.extra_cost
				invoice.total_cost=job.Estimate_id.total_cost
				invoice.save()
				return HttpResponseRedirect('/my_job')
			return render(request,self.template_name,{'form':form})
		return render(request,self.template_name,{'form':form})


#report job by worker
class report_job(CreateView,View):
	form_class = report_job
	template_name='job/report_job.html'

	def get(self,request,job_id):
		form=self.form_class(None)
		job=Job.objects.get(id=job_id)
		job_report=job.job_report
		if 'logs' in request.session:
			if job.job_start_datetime <= datetime.date.today():
				return render(request,self.template_name,{'form':form,'job_report':job_report})
			else:
				messages.warning(request,'Job is not Scheduled Yet.')
				return HttpResponseRedirect('/my_job')
		else:
			return HttpResponseRedirect('/login')

	def post(self,request,job_id):
		form=self.form_class(request.POST)
		if form.is_valid():
			user=form.save(commit=False)
			job=Job.objects.get(id=job_id)
			job.job_report=form.cleaned_data['job_report']
			job.report_customer_approvel=False
			job.save()
			return HttpResponseRedirect('/my_job')
		return render(request,self.template_name,{'form':form})


def reject_worker(request,cust_id):
		if 'logs' in request.session:
			cust=Customer.objects.get(id=cust_id)
			cust.wish_to_be_worker=False
			cust.save()
			return HttpResponseRedirect('/wishes_worker')
		else:
			return HttpResponseRedirect('/login')

def profile(request):
	if 'logs' in request.session:
		cust=Customer.objects.get(id=request.session['id'])
		return render(request,'job/profile.html',{'user':cust})
	else:
		return HttpResponseRedirect('/login')

#add a worker from requests
class add_worker(CreateView,View):
	form_class = AddWorker
	template_name='job/add_worker.html'

	def get(self,request,cust_id):
		form=self.form_class(None)
		cat=Category.objects.all()
		cust=Customer.objects.get(id=cust_id)
		if 'logs' in request.session:
			return render(request,self.template_name,{'form':form,'cust':cust,'cat':cat})
		else:
			return HttpResponseRedirect('/login')

	def post(self,request,cust_id):
			form=self.form_class(request.POST)
		#if form.is_valid():
			user=form.save(commit=False)
			cust=Customer.objects.get(id=cust_id)
			category_id=form.cleaned_data['category_id']
			worker=form.cleaned_data['worker']
			cust.user_type="Worker"
			cust.save()
			user.save()
			if user is not None:
				return HttpResponseRedirect('/worker')
		#return render(request,self.template_name,{'form':form})

def services(request):
	temp=request.POST.get('srch')
	request.session['url']='services'
	all_services=Services_Request.objects.filter(job_created=False)
	if temp:
		temp1=Customer.objects.filter(first_name__startswith=temp)
		if temp1:
			for serch in range(0,len(temp1)):
				all_se = all_services.filter(customer_id=temp1[serch].id)
				context={'all_services':all_se,}
		else:
			context = {}
	else:
		context={'all_services':all_services,}

	if 'logs' in request.session:
		return render(request,'job/service_all.html',context)
	else:
		return HttpResponseRedirect('/login')


#admin job reports
def admin_job_report(request):
	if 'logs' in request.session:
		request.session['url']="report"
		all_jobs=Job.objects.all()
		all_jobs=all_jobs.filter(report_customer_approvel=False)
		context={'all_jobs':all_jobs,}
		return render(request,'job/admin_job_report.html',context)

	else:
		return HttpResponseRedirect('/login')

def admin_report_submit(request,job_id):
	if 'logs' in request.session:
			job=Job.objects.get(id=job_id)
			job.save()
			return HttpResponseRedirect('/job')
	else:
		return HttpResponseRedirect('/login')


#all queries Admin side
def queries(request):
	temp=request.POST.get('srch')
	#all_queries={}
	all_queries=Query.objects.all()
	if temp:
		all_queries=all_queries.filter(query_description__contains=temp)
	context={'all_queries':all_queries,}
	if 'logs' in request.session:
		return render(request,'job/query_all.html',context)
	else:
		return HttpResponseRedirect('/login')

#job of single user
def worker_jobs(request):
	temp=request.POST.get('srch')
	work=Worker.objects.get(worker=request.session['id'])
	all_jobs=Job.objects.filter(worker_id=work.id)
	all_jobs=all_jobs.filter(job_status="pending")
	all_jobs=all_jobs.filter(customer_approvel=True)
	if temp:
		all_jobs=all_jobs.filter(status=temp)
	context={'all_jobs':all_jobs,}
	if 'logs' in request.session:
		return render(request,'job/worker_job.html',context)
	else:
		return HttpResponseRedirect('/login')

def WorkerView(request):
	temp=request.POST.get('srch')
	all_workers=Worker.objects.all()
	if temp:
		all_workers=all_workers.filter(status__startswith=temp)
	return render(request,'job/worker_all.html',{'all_workers':all_workers})
	if 'logs' in request.session:
		return render(request,'job/worker_all.html',context)
	else:
		return HttpResponseRedirect('/login')

def CustomerView(request):
	temp=request.POST.get('srch')
	all_customers={}
	if temp:
			all_customers=Customer.objects.filter(first_name__startswith=temp)
	else:
		all_customers=Customer.objects.filter(user_type="Customer")
	context={'all_customers':all_customers}
	if 'logs' in request.session:
		return render(request,'job/customer_all.html',context)
	else:
		return HttpResponseRedirect('/login')

def JobView(request):
	temp=request.POST.get('srch')
	all_jobs=Job.objects.filter(customer_approvel=True)
	if temp:
			all_jobs=all_jobs.filter(job_status__startswith=temp)
	context={'all_jobs':all_jobs,}
	if 'logs' in request.session:
		return render(request,'job/job_all.html',context)
	else:
		return HttpResponseRedirect('/login')

def CustQuery(request):
	temp=request.POST.get('srch')
	all_query=Query.objects.filter(customer_id=request.session['id'])
	if temp:
			all_query=all_query.objects.filter(query_description__contains=temp)
	context={'all_query':all_query,}
	if 'logs' in request.session:
		return render(request,'job/customer_query.html',context)
	else:
		return HttpResponseRedirect('/login')

class QueryView(View):
	form_class = QueryForm
	template_name='job/query.html'

	def get(self,request):
		form=self.form_class(None)
		cust=Customer.objects.get(first_name=request.session['logs']).id
		if 'logs' in request.session:
			return render(request,self.template_name,{'form':form,'cust':cust})
		else:
			return HttpResponseRedirect('/login')

	def post(self,request):
		form=self.form_class(request.POST)
		if form.is_valid():
			user=form.save(commit=False)
			query_description=form.cleaned_data['query_description']
			customer_id=form.cleaned_data['customer_id']
			#customer_id=Customer.objects.get(first_name=request.session['logs'])
			user.save()
			if user is not None:
				return HttpResponseRedirect('/custquery')
		return render(request,self.template_name,{'form':form})

class FeedbackView(View):
	form_class=FeedbackForm
	template_name='job/feedback.html'

	def get(self,request):
		form=self.form_class(None)
		cust=Customer.objects.get(first_name=request.session['logs']).id
		if 'logs' in request.session:
			return render(request,self.template_name,{'form':form,'cust':cust})
		else:
			return HttpResponseRedirect('/login')

	def post(self,request):
		form=self.form_class(request.POST)
		if form.is_valid():

			user=form.save(commit=False)
			#cleaned(normalized) data
			feedback_description=form.cleaned_data['feedback_description']
			customer_id=form.cleaned_data['customer_id']
			user.save()
		return render(request,self.template_name,{'form':form})

class ServiceRequestView(View):
    form_class=ServiceRequestForm
    template_name='job/service_request.html'

    def get(self,request):
        form=self.form_class(None)
        cust=Customer.objects.get(first_name=request.session['logs']).id
        if 'logs' in request.session:
        	return render(request,self.template_name,{'form':form,'cust':cust})
        else:
        	return HttpResponseRedirect('/login')

    def post(self,request):
        form=self.form_class(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            service_request=form.cleaned_data['service_request']
            customer_id=form.cleaned_data['customer_id']
            #recipient=Customer.objects.get(id=request.session['id'])
            # notify.send(Customer.objects.get(id=request.session['id']),recipient=recipient, verb='you succefully post a request')            
            user.save()
        return render(request,self.template_name,{'form':form})

def logout(request):
	try:
		del request.session['logs']
		del request.session['profile']
		return HttpResponseRedirect('/login')
	except:
		return HttpResponseRedirect('/login')

class NewJob(CreateView, View):
	form_class = Newjob
	template_name = 'job/create_job.html'
	def get(self,request,ser_id):
		try:
			form = self.form_class(None)
			all_workers=Worker.objects.all()
			all_services=Services_Request.objects.get(id=ser_id)
			all_customers=Customer.objects.get(id=all_services.customer_id.id)
			all_estimate=Estimation.objects.get(service_id=all_services.id)
			location=Customer.objects.get(id=all_services.customer_id.id).address
			all_estimation=Estimation.objects.all()
			return render(request, self.template_name,{'form':form,'all_workers':all_workers,'all_customers':all_customers,'all_services':all_services,'all_estimation':all_estimation,'location':location,'all_estimate':all_estimate})
		except:
			messages.warning(request,'Create Estimation First.')
			return render(request, self.template_name)

	def post(self,request,ser_id):
		form = self.form_class(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			worker_id = form.cleaned_data['worker_id']
			customer_id =form.cleaned_data['customer_id']
			cust=Customer.objects.get(id=customer_id.id)
			service_id=form.cleaned_data['service_id']
			Estimate_id=form.cleaned_data['Estimate_id']
			job_start_date=form.cleaned_data['job_start_datetime']
			location =form.cleaned_data['location']
			job_description = form.cleaned_data['job_description']
			service=Services_Request.objects.get(id=service_id.id)
			service.job_created=True
			temp=Job.objects.filter(worker_id=worker_id)
			temp=temp.filter(job_status="pending")
			if temp:
				for t in temp:
					if job_start_datetime==t.job_start_datetime:
							messages.warning(request,'Worker is busy.')
							return render(request, self.template_name)
			service.save()
			user.save()
			return HttpResponseRedirect('/job')
		return render(request, self.template_name,{'form':form})

class ResponseQuery(UpdateView, View):
    form_class = Response
    template_name = 'job/response_query.html'

    def get(self,request,que_id):
        form = self.form_class(None)
        queries=Query.objects.get(id=que_id)
        all_customers=Customer.objects.get(id=queries.customer_id.id)
        return render(request, self.template_name,{'form':form,'queries':queries,'all_customers':all_customers})

    def post(self,request,que_id):
        form = self.form_class(request.POST)
        if form.is_valid():
        	queries=Query.objects.get(id=que_id)
        	user = form.save(commit=False)
        	queries.id=queries.id
        	queries.customer_id =form.cleaned_data['customer_id']
        	queries.query_response = form.cleaned_data['query_response']
        	queries.status=form.cleaned_data['status']
        	queries.save()
        	return HttpResponseRedirect('/queries')
        return render(request, self.template_name,{'form':form,'queries':queries,'all_customers':all_customers})

class Estimate(CreateView,View):
    form_class = estimate
    template_name = 'job/estimate.html'

    def get(self,request,ser_id):
        form = self.form_class(None)
        try:
        	service=Services_Request.objects.get(id=ser_id)
        	customer=Customer.objects.get(id=service.customer_id.id)
        	estimate=Estimation.objects.get(service_id=ser_id)
        	return render(request, self.template_name,{'form':form,'service':service,'customer':customer,'estimate':estimate})
        except:	
        	return render(request, self.template_name,{'form':form,'service':service,'customer':customer})


    def post(self,request,ser_id):
        form = self.form_class(request.POST)
        if form.is_valid():
        	user = form.save(commit=False)
        	try:
	        	estimate=Estimation.objects.get(service_id=ser_id)
	        	estimate.service_id=form.cleaned_data['service_id']
	        	estimate.customer_id=form.cleaned_data['customer_id']
	        	estimate.trasportation_charge=form.cleaned_data['trasportation_charge']
	        	estimate.visit_charge=form.cleaned_data['visit_charge']
	        	estimate.extra_cost=form.cleaned_data['extra_cost']
	        	estimate.total_cost=estimate.trasportation_charge+estimate.visit_charge+estimate.extra_cost
	        	estimate.save()
	        except:
	        	service_id=form.cleaned_data['service_id']
	        	customer_id=form.cleaned_data['customer_id']
	        	trasportation_charge=form.cleaned_data['trasportation_charge']
	        	visit_charge=form.cleaned_data['visit_charge']
	        	extra_cost=form.cleaned_data['extra_cost']
	        	total_cost=trasportation_charge+visit_charge+extra_cost
	        	user.save()
        	if request.session['url']=='services':
        		return HttpResponseRedirect('/service')
        	else:
        		return HttpResponseRedirect('/admin_job_report')
        return render(request, self.template_name,{'form':form})

class SignUp(CreateView, View):
    form_class = AddCustomer
    template_name = 'job/customer_form.html'

    def get(self,request):
        form = self.form_class(None)
        return render(request, self.template_name)

    def post(self,request):
        form = AddCustomer(request.POST,request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            address = form.cleaned_data['address']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']
            mobile_number = form.cleaned_data['mobile_number']
            profile_pic = request.FILES['profile_pic']
            if password == confirm_password:
                user.save()
                user_data = ""
                try:
                    user_data = Customer.objects.get(email=email)
                    subject = 'TRABAZO Account Verification'
                    from_email = settings.EMAIL_HOST_USER
                    email_to = user_data.email
                    html_content =  '<html><body> HI '+ str(user_data.first_name) + ' ' + str(user_data.last_name) +',<br /><br />Your user account with the e-mail address '+ str(user_data.email) + ' and password <b>' + str(user_data.password) + '</b> has been created.<br /><br />Please follow the link below to activate your account.<br /><a href=http://127.0.0.1:9999/' + str(user_data.email)+ '/' +str(user_data.confirmation_code) +'> Click Here </a><br /><br />You will be able to Manage your account once your account is activated.</body></html>'
                    msg = EmailMultiAlternatives(subject, html_content, from_email, [email_to])
                    msg.attach_alternative(html_content, "text/html")
                    msg.send()
                except:
                    user_data.objects.delete()
                    msg = "Email Verification Error. Please Signup Again."
                    return render(request,self.template_name,{'err_msg':msg})

                if user is not None:
                    messages.success(request,'Your Account is Created now check your mail to verification.')
                    return HttpResponseRedirect('/login')
            else:
                msg = "Password and Confirm Password are not same."
                return render(request,self.template_name,{'err_msg':msg})
        msg = "Data is not Valid."
        return render(request,self.template_name,{'err_msg':msg})

class LogInView(View):
	form_class=Add_Customer
	template_name="job/login.html"

	def get(self,request,email="",confirmation_code=""):
		if 'logs' in request.session:
			return HttpResponseRedirect('/index')
		form=self.form_class(None)
		user = ""
		try:
			user = Customer.objects.get(email=email)
			if user.confirmation_code == int(confirmation_code):
				user.confirmation_code = 0
				user.confirm = True
				user.save()
				msg = "Your Account has been confirmed."
				return render(request, self.template_name, {'msg':msg})
			else:
				msg = "Please Confirm your account first."
				return render(request, self.template_name, {'msg':msg})
		except:
			return render(request,self.template_name,{'form':form})

	def post(self,request,email="",confirmation_code=""):
		self.email = request.POST['email']
		self.password = request.POST['password']
		user=""
		try:
			user=Customer.objects.get(email=self.email)
			if(user.confirm == False):
				msg = "Please Confirm your Account First."
				return render(request,self.template_name,{'msg':msg})
			else:
				if(user.password==self.password):
					request.session['logs']=user.first_name
					request.session['profile']=user.profile_pic.url
					request.session['dash']=user.user_type
					request.session['id']=user.id
					logs=request.session['logs']
					profile=user.profile_pic
					request.session.modified = True
					return HttpResponseRedirect('/index')
				else:
					msg = "Email Id / Password is not Correct."
					return render(request,self.template_name,{'msg':msg})
		except:
			msg="Email Id / Password is not Correct."
			return render(request,self.template_name,{'msg':msg})

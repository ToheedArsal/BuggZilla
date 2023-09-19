from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm 
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required,user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignUpForm,LoginForm,ProjectForm,BugForm
from .models import Project,CustomUser,Bug

def is_developer(user):
	profile=CustomUser.objects.get(username=user.username)
	return profile.user_type == "developer"

def is_manager(user):
	profile=CustomUser.objects.get(username=user.username)
	return profile.user_type == "manager"

def is_qa(user):
	profile=CustomUser.objects.get(username=user.username)
	return profile.user_type == "qa"

# for creating a new user
def signup_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Form submission successful')
            return redirect('loginaccount')
        else:
            return render(request, 'signuppage.html', {'error': 'Form Is Not Valid'})
    else:
        form = SignUpForm()
    return render(request, 'signuppage.html', {'form': form})

# for authentication and login
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        profile=CustomUser.objects.get(username=username)
        user_type=profile.user_type
        
        if user is not None:
            if user.is_active:
                login(request, user)
                if user_type == "manager":
                    return redirect('managerdashboard')
                if user_type == "qa":
                    return redirect('qadashboard')  # Replace 'dashboard' with your desired URL name
                if user_type == "developer":
                    return redirect('developerdashboard')
            else:
                # Inactive user account
                return render(request, 'loginpage.html', {'error': 'Account is inactive.'})
        else:
            # Invalid login credentials
            return render(request, 'loginpage.html', {'error': 'Invalid login credentials.'})
    return render(request, 'loginpage.html')

#for logout the user
@login_required(login_url='loginaccount' , redirect_field_name="next")
def logout_account(request):
    logout(request)
    return redirect('loginaccount')

@login_required(login_url='/loginaccount' , redirect_field_name="next")
@user_passes_test(is_manager, login_url='no_access')
def manager_dashboard(request):
	try:
		if request.method== "GET":
			user=request.user
			profile=CustomUser.objects.get(username=user.username)
			projects=Project.objects.filter(managers=profile)
			return render(request, 'managerdashboard.html', {'projects': projects, 'username':user.username})
	except CustomUser.DoesNotExist:
		return render(request,"error.html",{'error_message':"Project not found."})

@user_passes_test(is_manager, login_url='no_access')
@login_required(login_url='loginaccount' , redirect_field_name="next")
def add_project(request):
	try:
		if request.method == 'POST':
			form = ProjectForm(request.POST)
			user=request.user
			profile=CustomUser.objects.get(username=user.username)
			user_type=profile.user_type
			if form.is_valid():
				project = form.save(commit=False)  
				project.managers = profile 
				project.save()  
				return redirect('managerdashboard')  
		else:
			form = ProjectForm()
		
		return render(request, 'createproject.html', {'form': form})

	except CustomUser.DoesNotExist:
		return render(request,"error.html",{'error_message':"User not found."})

@login_required(login_url='loginaccount' , redirect_field_name="next")
@user_passes_test(is_manager, login_url='no_access')
def update_project(request, project_id):
	try:
		project = Project.objects.get(id= project_id)
		if request.method == 'POST':
			form = ProjectForm(request.POST, instance=project)
			if form.is_valid():
				form.save()
				return redirect('managerdashboard') 
		else:
			form = ProjectForm(instance=project)
    
		return render(request, 'updateproject.html', {'form': form})
	except Project.DoesNotExist:
		return render(request,"error.html",{'error_message':"Project not found."})


@login_required(login_url='loginaccount' , redirect_field_name="next")
@user_passes_test(is_manager, login_url='no_access')
def delete_project(request, project_id):
	try:
		project = Project.objects.get(id=project_id)
		project.delete()
		return redirect('managerdashboard')
	except Project.DoesNotExist:
		return render(request,"error.html",{'error_message':"Project not found."})


@login_required(login_url='/loginaccount' , redirect_field_name="next")
@user_passes_test(is_manager, login_url='no_access')
def show_all_projects(request):
	try:
		if request.method== "GET":
			user=request.user
			profile=CustomUser.objects.get(username=user.username)
			projects=Project.objects.filter(managers=profile)
			return render(request, 'showallprojects.html', {'projects': projects})
	except CustomUser.DoesNotExist:
		return render(request,"error.html",{'error_message':"User not found."})
	except Project.DoesNotExist:
		return render(request,"error.html",{'error_message':"Project not found."})
	


@login_required(login_url='/loginaccount' , redirect_field_name="next")
@user_passes_test(is_manager, login_url='no_access')
def show_all_available_developers(request, project_id):
	try:
		project = Project.objects.get(id=project_id)
		developers = project.developer.all()
		excluded_developers = CustomUser.objects.filter(user_type="developer").exclude(id__in=developers.values_list('id', flat=True))
		return render(request, 'showallavailabledevelopers.html', {'excluded_developers': excluded_developers, 'project': project, 'developers': developers})
	except Project.DoesNotExist:
		return render(request,"error.html",{'error_message':"Project not found."})


@login_required(login_url='/loginaccount' , redirect_field_name="next")
@user_passes_test(is_manager, login_url='no_access')
def assign_a_developer(request,project_id):
	try:
		if request.method == 'POST':
			developer_select = request.POST.get('developer_select')
			if developer_select:
				project = Project.objects.get(id=project_id)
				dev = CustomUser.objects.get(username=developer_select)
				project.developer.add(dev)
				return redirect('managerdashboard')
   
		return redirect('managerdashboard')
	except CustomUser.DoesNotExist:
		return render(request,"error.html",{'error_message':"User not found."})
	except Project.DoesNotExist:
		return render(request,"error.html",{'error_message':"Project not found."})
	

@login_required(login_url='/loginaccount' , redirect_field_name="next")
@user_passes_test(is_manager, login_url='no_access')
def show_all_available_qa(request, project_id):
	try:
		project = Project.objects.get(id=project_id)
		qas = project.qa.all()
		excluded_qas = CustomUser.objects.filter(user_type="qa").exclude(id__in=qas.values_list('id', flat=True))
		return render(request, 'showallavailableqa.html', {'excluded_qas': excluded_qas, 'project': project, 'qas': qas})
	except CustomUser.DoesNotExist:
		return render(request,"error.html",{'error_message':"User not found."})
	except Project.DoesNotExist:
		return render(request,"error.html",{'error_message':"Project not found."})
	

@login_required(login_url='/loginaccount' , redirect_field_name="next")
@user_passes_test(is_manager, login_url='no_access')
def assign_a_qa(request, project_id):
	try:
		if request.method == 'POST':
			qa_select = request.POST.get('qa_select')
			if qa_select:
				project = Project.objects.get(id=project_id)
				qa = CustomUser.objects.get(username=qa_select)
				project.qa.add(qa)
				return redirect('managerdashboard')
		return redirect('managerdashboard') 

	except CustomUser.DoesNotExist:
		return render(request,"error.html",{'error_message':"User not found."})
	except Project.DoesNotExist:
		return render(request,"error.html",{'error_message':"Project not found."})


@login_required(login_url='/loginaccount' , redirect_field_name="next")
@user_passes_test(is_manager, login_url='no_access')
def show_assigned_developers(request, project_id):
	try:
		project = Project.objects.get(id=project_id)
		developers=project.developer.all()
		return render(request, 'showassigneddevelopers.html', {'developers': developers, 'project': project})
	except Project.DoesNotExist:
		return render(request,"error.html",{'error_message':"Project not found."})

@login_required(login_url='/loginaccount' , redirect_field_name="next")
@user_passes_test(is_manager, login_url='no_access')
def remove_developer(request, project_id):
	try:
		if request.method == 'POST':
			developer_select = request.POST.get('developer_select')  # Use .get() to avoid KeyError
			if developer_select:
				project = Project.objects.get(id=project_id)
				dev = CustomUser.objects.get(username=developer_select)
				project.developer.remove(dev)
		return redirect('managerdashboard')
	except  Project.DoesNotExist:
		return render(request,"error.html",{'error_message':"Project not found."})
	except  CustomUser.DoesNotExist:
		return render(request,"error.html",{'error_message':"User not found."})

@login_required(login_url='/loginaccount' , redirect_field_name="next")
@user_passes_test(is_manager, login_url='no_access')
def show_assigned_qa(request, project_id):
	try:
		project = Project.objects.get(id=project_id)
		qas=project.qa.all()
		return render(request, 'showassignedqa.html', {'qas': qas, 'project': project})
	except  Project.DoesNotExist:
		return render(request,"error.html",{'error_message':"Project not found."})
	

@login_required(login_url='/loginaccount' , redirect_field_name="next")
@user_passes_test(is_manager, login_url='no_access')
def remove_qa(request, project_id):
	try:
		if request.method == 'POST':
			qa_select = request.POST.get('qa_select')
			if qa_select:
				project = Project.objects.all(id=project_id)
				qa = CustomUser.objects.get(username=qa_select)
				project.qa.remove(qa)
		return redirect('managerdashboard')
	except  Project.DoesNotExist:
		return render(request,"error.html",{'error_message':"Project not found."})
	except  CustomUser.DoesNotExist:
		return render(request,"error.html",{'error_message':"User not found."})


#qa functionality
@login_required(login_url='/loginaccount' , redirect_field_name="next")
@user_passes_test(is_qa, login_url='no_access')
def qa_dashboard(request):
	if request.method== "GET":
		user=request.user
		projects=Project.objects.all()
		return render(request, 'qadashboard.html', {'projects': projects, 'username':user.username})


@login_required(login_url='/loginaccount' , redirect_field_name="next")
@user_passes_test(is_qa, login_url='no_access')
def create_bug(request, project_id):
	try:
		project = Project.objects.get(id=project_id)
		user=request.user
		qa_id=CustomUser.objects.get(username=user.username)
		if request.method == 'POST':
			form = BugForm(request.POST, request.FILES)
			if form.is_valid():
				bug = form.save(commit=False)
				bug.project = project
				bug.creator=qa_id
				bug.save()
				return redirect('qadashboard') 
		else:
			form = BugForm(initial={'project': project})
		
	except  Project.DoesNotExist:
		return render(request,"error.html",{'error_message':"Project not found."})
	except  CustomUser.DoesNotExist:
		return render(request,"error.html",{'error_message':"User not found."})
    
	return render(request, 'bug_form.html', {'form': form})


@login_required(login_url='/loginaccount' , redirect_field_name="next")
@user_passes_test(is_qa, login_url='no_access')
def show_bug_of_a_project(request, project_id):
	try:
		user=request.user
		user_profile=CustomUser.objects.get(username=user.username)
		pro = Project.objects.get(id=project_id)
		bugs=Bug.objects.filter(project=pro, creator=user_profile)
		return render(request, 'bugdetailproject.html', {'bugs': bugs, 'username': user.username })
	except  Project.DoesNotExist:
		return render(request,"error.html",{'error_message':"Project not found."})
	except  CustomUser.DoesNotExist:
		return render(request,"error.html",{'error_message':"User not found."})

@login_required(login_url='/loginaccount' , redirect_field_name="next")
@user_passes_test(is_qa, login_url='no_access')
def delete_a_bug(request, bug_id):
	try:
		bug = Bug.objects.get(id=bug_id)
		bug.delete()
		user=request.user
		user_profille=CustomUser.objects.get(username=user.username)
		bugs=Bug.objects.filter(creator=user_profille)
		return render(request, 'bugdetailproject.html', {'bugs': bugs, 'username': user.username })
	except  CustomUser.DoesNotExist:
		return render(request,"error.html",{'error_message':"User not found."})
	except  Bug.DoesNotExist:
		return render(request,"error.html",{'error_message':"Bug not found."})


@login_required(login_url='/loginaccount' , redirect_field_name="next")
@user_passes_test(is_qa, login_url='no_access')
def show_all_the_bugs_of_a_qa(request):
	try:
		user=request.user
		user_profille=CustomUser.objects.get(username=user.username)
		bugs=Bug.objects.filter(creator=user_profille)
		return render(request, 'show_qa_bugs.html', {'bugs' : bugs})
	except  CustomUser.DoesNotExist:
		return render(request,"error.html",{'error_message':"User not found."})

@login_required(login_url='/loginaccount' , redirect_field_name="next")
@user_passes_test(is_qa, login_url='no_access')
@login_required(login_url='loginaccount' , redirect_field_name="next")
def update_bug(request, bug_id):
    bug = Bug.objects.get(id=bug_id)
    assigned_developers = bug.project.developer.all()
    if request.method == 'POST':
        form = BugForm(request.POST, instance=bug)
        if form.is_valid():
            form.save()
            return redirect('qadashboard')  # Replace 'bug_detail' with the name of your bug detail view
    else:
        form = BugForm(instance=bug)
    
    context = {
        'form': form,
        'bug': bug,
		'assigned_developers':assigned_developers,
    }
    
    return render(request, 'updatebug.html', context)





## Developer functionality
@login_required(login_url='/loginaccount' , redirect_field_name="next")
@user_passes_test(is_developer, login_url='no_access')
def developer_dashboard(request):
	try:
		if request.method== "GET":
			user=request.user
			profile=CustomUser.objects.get(username=user.username)
			projects=Project.objects.filter(developer=profile)
			return render(request, 'developerdashboard.html', {'projects': projects, 'username':user.username})
	except CustomUser.DoesNotExist:
		pass
			

@login_required(login_url='/loginaccount' , redirect_field_name="next")
@user_passes_test(is_developer, login_url='no_access')
def show_all_the_bugs_of_a_project(request,project_id):
	try:
		pro = Project.objects.get(id=project_id)
		bugs=Bug.objects.filter(project=pro)
		return render(request,'showbugsofaproject.html',{'bugs':bugs})
	except Project.DoesNotExist:
		return render(request,"error.html",{'error_message':"Project not found."})

@login_required(login_url='/loginaccount' , redirect_field_name="next")
@user_passes_test(is_developer, login_url='no_access')
def assign_a_bug(request,bug_id):
	try:
		user=request.user
		profile=CustomUser.objects.get(username=user.username)
		bug=Bug.objects.get(id=bug_id)	
		bug.status='started'
		bug.developer=profile
		bug.save()
		return redirect('developerdashboard')
	
	except Bug.DoesNotExist:
		return render(request,"error.html",{'error_message':"Project not found."})
	except CustomUser.DoesNotExist:
		return render(request,"error.html",{'error_message':"User not found."})

		


@login_required(login_url='/loginaccount' , redirect_field_name="next")
@user_passes_test(is_developer, login_url='no_access')
def show_all_the_assigned_bugs_of_qa(request):
	try:
		user=request.user
		profile=CustomUser.objects.get(username=user.username)
		bugs=Bug.objects.filter(developer=profile)
		return render(request, "showallassignedbugs.html", {'bugs':bugs})

	except CustomUser.DoesNotExist:
		return redirect('showerror',{'error_message':"User profile not found."})


        
def show_error(request):
	return render(request,"error.html")

@login_required(login_url='/loginaccount' , redirect_field_name="next")
@user_passes_test(is_developer, login_url='no_access')
def mark_the_bug(request, bug_id):
	try:
		if request.method=="POST":
			bug=Bug.objects.get(id=bug_id)

			if bug.bug_type== "bug":
				bug.status="completed"
			elif bug.bug_type=="feature":
				bug.status="resolved"

			bug.save()
	
		return redirect('showallassignedbugs')
	
	except Bug.DoesNotExist:
		return render(request,"error.html",{'error_message':"Bug not found."})


def no_access(request):
    return render(request, 'no_access.html')

def handle_not_found_pages(request, exception):
    return render(request, '404.html', status=404)

def home(request):
    return render(request,'home.html')

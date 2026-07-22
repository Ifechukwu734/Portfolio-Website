from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login, logout
from .models import ProjectStack, UserExperience, ClientContactForm, PortfolioView
from django.contrib.auth import update_session_auth_hash
from django.utils import timezone
from django.db.models import Count
from django.db.models.functions import TruncDate
from collections import OrderedDict
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator

# Create your views here.


def landing_page_view(request):
    return render(request, 'landing.html')


def signup_page(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        # phone = request.POST.get('phone')
        location = request.POST.get('location')
        email = request.POST.get('email')
        password = request.POST.get('password')
        User = get_user_model()
        
        if not User.objects.filter(email=email).exists():
            user = User.objects.create(first_name=first_name, last_name=last_name, email=email, location=location)
            user.set_password(password)
            user.save()
            messages.success(request, 'Account created successfully, now you can log in')
            return redirect('/login/')
        else:
            messages.warning(request, 'Email already exists')
            return redirect(request.path)
        
    return render(request, 'signup.html')


def login_page(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            #messages.success(request, f'Welcome {request.user.first_name}')
            return redirect('/dashboard/')
        else:
            messages.warning(request, 'Invalid Credentials')
            return redirect(request.path)
    return render(request, 'login.html')


def dashboard_page(request):
    user = request.user
    last_week = timezone.now() - timezone.timedelta(days=7)
    total_contacts = ClientContactForm.objects.filter(user=user).order_by('-sent_on')
    total_contacts_last_week = PortfolioView.objects.filter(user=user, viewed_at__gte=last_week).count()
    number_of_views = PortfolioView.objects.filter(user=user).count()
    unread_contacts_count = ClientContactForm.objects.filter(user=user, viewed=False).count()
    total_contacts_count = total_contacts.count()
    paginator = Paginator(total_contacts, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    today = timezone.now().date()
    start_date = today - timezone.timedelta(days=6)

    current_week_start = today - timezone.timedelta(days=7)
    previous_week_start = today - timezone.timedelta(days=14)

    current_week_views = PortfolioView.objects.filter(
        user=user,
        viewed_at__gte=current_week_start
    ).count()

    current_week_contacts = ClientContactForm.objects.filter(user=user, sent_on__gte=current_week_start).count()

    previous_week_views = PortfolioView.objects.filter(
        user=request.user,
        viewed_at__gte=previous_week_start,
        viewed_at__lt=current_week_start
    ).count()

    if previous_week_views == 0:
        if current_week_views == 0:
            percentage_change = 0
        else:
            percentage_change = 100
    else:
        percentage_change = (
            (current_week_views - previous_week_views)
            / previous_week_views
        ) * 100

    percentage_change = round(percentage_change, 1)

    daily_views = (
        PortfolioView.objects
        .filter(user=user, viewed_at__date__gte=start_date)
        .annotate(day=TruncDate("viewed_at"))
        .values("day")
        .annotate(total=Count("id"))
    )

    chart = OrderedDict()

    for i in range(7):
        day = start_date + timezone.timedelta(days=i)
        chart[day] = 0

    for item in daily_views:
        chart[item["day"]] = item["total"]

    context = {
        'total_contacts': total_contacts,
        'total_contacts_count': total_contacts_count,
        'unread_contacts': unread_contacts_count,
        'number_of_clicks': number_of_views,
        'last_week_contacts': total_contacts_last_week,
        "labels": [d.strftime("%a") for d in chart.keys()],   # Mon Tue Wed...
        "values": list(chart.values()),
        "percentage_change": percentage_change,
        'current_week_contacts': current_week_contacts,
        "page_obj": page_obj,
    }
    return render(request, 'dashboard.html', context)


def auth_project_page(request):
    user = request.user
    if request.method == 'POST':
        tags = request.POST.get('tags')
        project_name = request.POST.get('title')
        project_metrics = request.POST.get('metric', '')
        project_description = request.POST.get('description')
        repo_url = request.POST.get('repo', '')
        demo_url = request.POST.get('demo', '')
        action = request.POST.get('action')
        project_image = request.FILES.get('project-image')

        if project_image:
            if project_image.size > 5 * 1024 * 1024:
                messages.warning(request, 'Image is greater than 5mb')
                return redirect(request.path)

        project = ProjectStack.objects.create(user=user, project_title=project_name, impact_metrics=project_metrics, project_description=project_description, 
                                              repository_url=repo_url, live_demo_url=demo_url, project_tech_stack=tags)
        if project_image:
            project.cover_image = project_image
            project.save()

        if action == 'draft':
            project.status = 'Draft'
            project.save()
        elif action == 'published':
            project.status = 'Published'
            project.save()

        messages.success(request, 'Project added Successfully')
        return redirect(request.path)
    
    unread_contacts_count = ClientContactForm.objects.filter(user=user, viewed=False).count()
    projects = ProjectStack.objects.filter(user=user).order_by('-uploaded_on')
    project_count = projects.count()
    context = {
        'project_count': project_count,
        'projects': projects,
        'unread_contacts': unread_contacts_count
    }

    return render(request, 'upload-project.html', context)


def auth_profile_page(request):
    user = request.user
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        location = request.POST.get('location')
        tech_field = request.POST.get('tech_field')
        bio = request.POST.get('bio')
        github_url = request.POST.get('github')
        linkedin_url = request.POST.get('linkedin')
        profile_image = request.FILES.get('profile_image')

        if profile_image:
            if profile_image.size > 5 * 1024 * 1024:
                messages.warning(request, 'Image greater than 5mb')
                return redirect(request.path)

        user.first_name = first_name
        user.last_name = last_name
        user.location = location
        user.tech_field = tech_field
        user.bio = bio
        user.github_url = github_url
        user.linkedin_url = linkedin_url
        user.save()

        if profile_image:
            user.profile_image = profile_image
            user.save()
        messages.success(request, 'Profile Updated Successfully')
        return redirect(request.path)
    tech_stack_list = user.user_tech_stack
    tech_stack = tech_stack_list.split(',')
    if len(tech_stack) == 1 and tech_stack[0] == '':
        tech_stack = ''
    unread_contacts_count = ClientContactForm.objects.filter(user=user, viewed=False).count()
    initials = f'{str(user.first_name)[0]}{str(user.last_name)[0]}'
    context = {
        'initials': initials,
        'tech_stack': tech_stack,
        'unread_contacts': unread_contacts_count
    }
    return render(request, 'profile.html', context)


def save_tech_stacks(request):
    user = request.user
    if request.method == 'POST':
        tags = request.POST.get('tags', '')
        user.user_tech_stack = tags
        user.save()
        messages.success(request, 'Skill(s) updated Successfully')
    return redirect('/profile/')



def save_professional_info(request):
    user = request.user
    if request.method == 'POST':
        p_headline = request.POST.get('p_headline', '')
        about_me = request.POST.get('about_me', '')
        p_summary = request.POST.get('p_summary', '')
        user.professional_headlines = p_headline
        user.about_me = about_me
        user.professional_summary = p_summary
        user.save()
        messages.success(request, 'Professional profile updated Successfully')
    return redirect('/profile/')




def save_account(request):
    user = request.user
    if request.method == 'POST':
        email = request.POST.get('email')
        new_password = request.POST.get('new-password')
        current_password = request.POST.get('current-password')

        User = get_user_model()
        users = User.objects.all().exclude(email=user.email)
        if users.filter(email=email).exists():
            messages.warning(request, 'Email already exists')
            return redirect('/profile/')
        user.email = email
        user.save()

        if current_password:
            if user.check_password(current_password):
                if user.check_password(new_password):
                    messages.warning(request, 'New password cannot be old password')
                    return redirect('/profile/')
                else:
                    user.set_password(new_password)
                    user.save()
                    update_session_auth_hash(request, user)
            else:
                messages.warning(request, 'Incorrect password')
                return redirect('/profile/')
            
        messages.success(request, 'Account Updated Successfully')
        return redirect('/profile/')


def update_project_page(request, id):
    user = request.user
    project = ProjectStack.objects.filter(id=id).first()
    if request.method == 'POST':
        if user == project.user:
            tags = request.POST.get('tags', '')
            project_name = request.POST.get('title')
            project_metrics = request.POST.get('metric', '')
            project_description = request.POST.get('description')
            repo_url = request.POST.get('repo', '')
            demo_url = request.POST.get('demo', '')
            action = request.POST.get('action')
            project_image = request.FILES.get('cover-image')

            if project_image:
                if project_image.size > 5 * 1024 * 1024:
                    messages.warning(request, 'Image is greater than 5mb')
                    return redirect(request.path)

            project.project_title = project_name
            project.impact_metrics = project_metrics
            project.project_description = project_description
            project.repository_url = repo_url
            project.live_demo_url = demo_url
            project.project_tech_stack = tags
            project.save()
            if project_image:
                project.cover_image = project_image
                project.save()

            if action == 'draft':
                project.status = 'Draft'
                project.save()
            elif action == 'published':
                project.status = 'Published'
                project.save()
        
            messages.success(request, 'Project updated successfully')
            return redirect(request.path)
        else:
            messages.warning(request, 'invalid user')
            return redirect(request.path)
        
    unread_contacts_count = ClientContactForm.objects.filter(user=user, viewed=False).count()
    tech_stack_list = project.project_tech_stack
    tech_stack = tech_stack_list.split(',')
    if len(tech_stack) == 1 and tech_stack[0] == '':
        tech_stack = ''
    context = {
        'project': project,
        'tech_stack': tech_stack,
        'unread_contacts': unread_contacts_count
    }
    return render(request, 'update_project.html', context)



def delete_project(request, id):
    user = request.user
    project = ProjectStack.objects.filter(id=id).first()
    if user == project.user:
        project.delete()
        messages.success(request, 'Project deleted successfully')
    else:
        messages.warning(request, 'invalid user')
    return redirect('/projects/')



def portfolio_page(request, user_id, name):
    User = get_user_model()
    user = User.objects.filter(user_id=user_id).first()
    if user.deactivated:
        return render(request, '404.html')
    else:
        ip_address = request.META.get('REMOTE_ADDR')
        tech_stack_list = user.user_tech_stack
        tech_stack = tech_stack_list.split(',')
        experiences = UserExperience.objects.filter(user=user, status='Published')
        projects = ProjectStack.objects.filter(user=user,status='Published').order_by('-uploaded_on')[:3]
        if experiences:
            for experience in experiences:
                if experience.key_responsibilities:
                    experience.key_responsibilities = [
                        line.strip()
                        for line in experience.key_responsibilities.splitlines()
                        if line.strip()
                    ]
        if projects:
            for project in projects:
                if project.project_tech_stack:
                    project.project_tech_stack = [
                        tag.strip()
                        for tag in project.project_tech_stack.split(",")
                        if tag.strip()
                    ]

        if len(tech_stack) == 1 and tech_stack[0] == '':
            tech_stack = ''
        PortfolioView.objects.create(user=user, ip_address=ip_address)
        context = {
            'projects': projects,
            'experiences': experiences,
            'user': user,
            'tech_stack': tech_stack
        }
        return render(request, 'index.html', context)


def experience_page(request):
    user = request.user
    user_experience = UserExperience.objects.filter(user=user).order_by('-uploaded_on')
    unread_contacts_count = ClientContactForm.objects.filter(user=user, viewed=False).count()
    context = {
        'experiences': user_experience,
        'unread_contacts': unread_contacts_count
    }
    return render(request, 'experience.html', context)


def add_experience(request):
    user = request.user
    if request.method == 'POST':
        company_name = request.POST.get('company_name')
        job_title = request.POST.get('job_title')
        employment_type = request.POST.get('employment_type')
        location = request.POST.get('location')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date', None)
        current_job = request.POST.get('current_job')
        short_description = request.POST.get('short_description', '')
        achievements = request.POST.get('achievements', '')
        tech_stacks = request.POST.get('tech_stack')
        action = request.POST.get('action')
        company_website = request.POST.get('company_website', '')

        experience = UserExperience.objects.create(user=user, company_name=company_name, job_title=job_title, employment_type=employment_type,
                                                   location=location, start_time=start_date, short_description=short_description, key_responsibilities=achievements,
                                                   tech_stack=tech_stacks, company_website=company_website)
        if current_job == 'on':
            experience.working_currently = True
            experience.save()
        
        experience.end_time = end_date
        experience.save()
        if action == 'draft':
            experience.status = 'Draft'
            experience.save()
        elif action == 'published':
            experience.status = 'Published'
            experience.save()
        messages.success(request, 'Experience added successfully')
        return redirect('/experiences/')
    return render(request, 'upload_experience.html')



def update_experience_page(request, id):
    user = request.user
    user_experience = UserExperience.objects.filter(id=id).first()
    if request.method == 'POST':
        if user == user_experience.user:
            company_name = request.POST.get('company_name')
            job_title = request.POST.get('job_title')
            employment_type = request.POST.get('employment_type')
            location = request.POST.get('location')
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date', None)
            current_job = request.POST.get('current_job')
            short_description = request.POST.get('short_description', '')
            achievements = request.POST.get('achievements', '')
            tech_stacks = request.POST.get('tech_stack')
            action = request.POST.get('action')
            company_website = request.POST.get('company_website', '')

            user_experience.company_name = company_name
            user_experience.job_title = job_title
            user_experience.employment_type = employment_type
            user_experience.location = location
            user_experience.start_time = start_date
            user_experience.short_description = short_description
            user_experience.key_responsibilities = achievements
            user_experience.tech_stack = tech_stacks
            user_experience.company_website = company_website
            user_experience.end_time = end_date
            user_experience.save()

            if current_job == 'on':
                user_experience.working_currently = True
                user_experience.save()

            if action == 'draft':
                user_experience.status = 'Draft'
                user_experience.save()
            elif action == 'published':
                user_experience.status = 'Published'
                user_experience.save()
        
            messages.success(request, 'Experience updated successfully')
            return redirect('/experiences/')
        else:
            messages.warning(request, 'invalid user')
            return redirect('/experiences/')

    # tech_stack_list = user_experience.tech_stack
    # tech_stack = tech_stack_list.split(',')
    # if len(tech_stack) == 1 and tech_stack[0] == '':
    #     tech_stack = ''
    context = {
        'user_experience': user_experience,
        # 'tech_stack': tech_stack
    }
    return render(request, 'update_experience.html', context)



def delete_experience(request):
    user = request.user
    user_experience = UserExperience.objects.filter(id=id).first()
    if user == user_experience.user:
        user_experience.delete()
        messages.success(request, 'Experience deleted successfully')
    else:
        messages.warning(request, 'invalid user')
    return redirect('/experiences/')



def portfolio_project_page(request,name, user_id):
    User = get_user_model()
    user = User.objects.filter(user_id=user_id).first()
    if user.deactivated:
        return render(request, '404.html')
    else:
        projects = ProjectStack.objects.filter(user=user,status='Published').order_by('-uploaded_on')
        if projects:
            for project in projects:
                if project.project_tech_stack:
                    project.project_tech_stack = [
                        tag.strip()
                        for tag in project.project_tech_stack.split(",")
                        if tag.strip()
                    ]
        context = {
            'user': user,
            'projects': projects
        }
        return render(request, 'projects.html', context)

def portfolio_contact_page(request, name, user_id):
    User = get_user_model()
    user = User.objects.filter(user_id=user_id).first()
    if user.deactivated:
        return render(request, '404.html')
    else:
        if request.method == 'POST':
            name = request.POST.get('name')
            email = request.POST.get('email')
            subject = request.POST.get('subject')
            message = request.POST.get('message')

            contact = ClientContactForm.objects.create(user=user, name=name, email=email, subject=subject, message=message)
            messages.success(request, 'Contact sent successfully')
            return redirect(request.path)
        context = {
            'user': user
        }
        return render(request, 'contact.html', context)


def user_logout(request):
    messages.success(request, 'Logged out successfully')
    logout(request)
    return redirect('/login/')


def deactivate_portfolio(request):
    user = request.user
    user.deactivated = True
    user.save()
    messages.success(request, 'Portfolio deactivated Successfully')
    return redirect('/profile/')



def reactivate_portfolio(request):
    user = request.user
    user.deactivated = False
    user.save()
    messages.success(request, 'Portfolio reactivated Successfully')
    return redirect('/profile/')



@login_required
def mark_contact_read(request, id):

    if request.method != "POST":
        return JsonResponse({"success": False}, status=405)

    contact = get_object_or_404(
        ClientContactForm,
        id=id,
        user=request.user
    )

    contact.viewed = True
    contact.save()
    total_count = ClientContactForm.objects.filter(user=request.user, viewed=False).count()

    return JsonResponse({
        "success": True,
        'total_count': total_count
    })



@login_required
def mark_contact_unread(request, id):

    if request.method != "POST":
        return JsonResponse({"success": False}, status=405)

    contact = get_object_or_404(
        ClientContactForm,
        id=id,
        user=request.user
    )

    contact.viewed = False
    contact.save()
    total_count = ClientContactForm.objects.filter(user=request.user, viewed=False).count()

    return JsonResponse({
        "success": True,
        'total_count': total_count
    })


@login_required
def delete_contact(request, id):

    if request.method != "POST":
        return JsonResponse({"success": False}, status=405)

    contact = get_object_or_404(
        ClientContactForm,
        id=id,
        user=request.user
    )
    contact.delete()
    
    total_count = ClientContactForm.objects.filter(user=request.user).count()
    return JsonResponse({
        "success": True,
        'total_count': total_count
    })




from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, HttpResponse, get_object_or_404
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout 
import os
import random
import string
from datetime import datetime
from .models import Category, KeySkill, UserProfile, User, ClintProfile, Notification
import uuid
from django.contrib import messages
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from datetime import datetime
# Create your views here.

def index1(request):
    error_message = ''
    if request.user.is_authenticated:
        return redirect('dashboard')  # Replace 'dashboard' with the desired URL name of your dashboard view
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Replace 'dashboard' with the desired URL name of your dashboard view
        else:
            error_message = 'Invalid username or password.'

    return render(request, 'login.html', {'error_message': error_message})


@login_required
def dashboard1(request):
    if request.user.is_staff or request.user.is_superuser:
        #return redirect('admin:index') makemigrations
        #logout(request)
       # return redirect('login')
       pass
    notifications = Notification.objects.all()
    user = request.user
    # Access user data
    username = user.username
    email = user.email
    if request.user.is_superuser:
        name = username
        client_profiles = 'no profile'
    else:
        user_profile = user.clintprofile
        name = user_profile.name
    
    client = request.user.clintprofile  # Get the client profile of the logged-in user
    featured_profiles = client.featured_profile.all()  # Get the featured profiles associated with the client
    current_date = datetime.now()
    context = {
        'username': username,
        'email': email,
        'name': name,
        'notifications': notifications,
        'current_date': current_date,
        'featured_profiles': featured_profiles
        # ... Add other user data fields to the context
    }

    return render(request, 'dashboard.html', context)

def vm(request):
   return render(request, 'vm.html')

def profile(request):
   user = request.user
   username = user.username
   email = user.email
   user_profile = user.clintprofile
   name = user_profile.name
   company = user_profile.company
   designation = user_profile.designation

   context = {
    'username': username,
    'email': email,
    'name': name,
    'company' : company,
    'designation' : designation
        
    }
   return render(request, 'profile.html', context)

from PIL import Image

def is_valid_image(image):
    try:
        img = Image.open(image)
        img.verify()
        return True
    except:
        return False

def generate_random_filename(length=10):
        letters = string.ascii_letters
        return ''.join(random.choice(letters) for _ in range(length))


def generate_random_filename(filename):

    ext = filename.split('.')[-1]
    random_name = uuid.uuid4().hex
    return f"{random_name}.{ext}"

# ...
def create_profile(request):
    if request.method == 'POST':
        # Retrieve form data
        name = request.POST['name']
        phone_number = request.POST['phone_number']
        email = request.POST['email']
        profile_pic = request.FILES['profile_pic']
        categories = request.POST.getlist('category')
        rating = request.POST['rating']
        key_skills = request.POST.getlist('key_skills')
        deliveries = request.POST['deliveries']
        experience = request.POST['experience']
        education = request.POST['education']
        commercial_hr = request.POST['commercial_hr']
        commercial_day = request.POST['commercial_day']


        # Generate a random file name for the image
        file_name = generate_random_filename(profile_pic.name)

        # Save the image to the appropriate location
        file_path = 'profile_pics/' + file_name
        image_data = ContentFile(profile_pic.read())
        default_storage.save(file_path, image_data)

        # Create the user profile object and save it
        profile = UserProfile(
            name=name,
            phone_number=phone_number,
            email=email,
            profile_pic=file_path,
            rating=rating,
            deliveries=deliveries,
            experience=experience,
            education=education,
            commercial_hr=commercial_hr,
            commercial_day=commercial_day,
        )
        profile.save()

        # Associate selected categories with the user profile
        for category_id in categories:
            category = Category.objects.get(id=category_id)
            profile.category.add(category)

        # Associate selected key skills with the user profile
        for key_skill_id in key_skills:
            key_skill = KeySkill.objects.get(id=key_skill_id)
            profile.key_skills.add(key_skill)

        # Display success message and render the template
        categories = Category.objects.all()
        key_skills = KeySkill.objects.all()
        success_message = 'User profile Created successfully.'
        return render(request, 'profile_create.html', {'alert_type': 'success', 'success_message': success_message, 'categories': categories, 'key_skills': key_skills})

    categories = Category.objects.all()
    key_skills = KeySkill.objects.all()

    return render(request, 'profile_create.html', {'categories': categories, 'key_skills': key_skills})


def key_skill(request):
    if request.method == 'POST':
        key_skill_name = request.POST['key_skill_name']
        # Perform any validation or additional logic here
        
        try:
            key_skill = KeySkill.objects.create(key_skill_name=key_skill_name)
            messages.success(request, 'Key skill added successfully!')
        except Exception as e:
            messages.error(request, 'Error adding key skill: {}'.format(str(e)))
    
    return render(request, 'key_skill.html')


def category_view(request):
    if request.method == 'POST':
        category_name = request.POST['category_name']
        # Perform any validation or additional logic here
        
        try:
            category = Category.objects.create(category_name=category_name)
            messages.success(request, 'Category added successfully!')
        except Exception as e:
            messages.error(request, 'Error adding Category : {}'.format(str(e)))
    return render(request, 'category_view.html')
    
def update_profile(request):
    return HttpResponse('this is profile')

def create_client(request):
    if request.method == 'POST':
        # Get the form data from the request
        username = request.POST.get('username')
        name = request.POST.get('name')
        password = request.POST.get('password')
        email = request.POST.get('email')
        company = request.POST.get('company')
        phone_number = request.POST.get('phone_number')
        designation = request.POST.get('designation')

        try:
            # Create a new User object
            user = User.objects.create(username=username, email=email)
            user.set_password(password)
            user.save()

            # Create a ClintProfile object and associate it with the User
            profile = ClintProfile.objects.create(user=user, name=name, company=company, phone_number=phone_number, designation=designation)

            messages.success(request, 'User created successfully!')
        except Exception as e:
            error_message = 'Error creating user: {}'.format(str(e))
            messages.error(request, error_message)

    users = ClintProfile.objects.all()
    return render(request, 'client_create.html',{'users':users})

def all_profile(request):
    if request.user.is_superuser:
        mainy='hii'
        wishlist_profiles="no"
    else:
        client = request.user.clintprofile
        wishlist_profiles = client.wishlist.all()
    if request.method == 'POST':
        selected_categories = request.POST.getlist('categories')
        selected_key_skills = request.POST.getlist('key_skills')

        profiles = UserProfile.objects.all()

        if selected_categories:
            # Filter profiles based on selected categories
            user_ps = profiles.filter(category__in=selected_categories)

        if selected_key_skills:
            # Filter profiles based on selected key skills
            user_ps = profiles.filter(key_skills__in=selected_key_skills)

        user_ps = user_ps.distinct()

        categories = Category.objects.all()
        key_skills = KeySkill.objects.all()

        return render(request, 'all_profile.html', {'user_ps': user_ps, 'categories': categories, 'key_skills': key_skills})

    user_ps = UserProfile.objects.all()
    categories = Category.objects.all()
    key_skills = KeySkill.objects.all()
    return render(request, 'all_profile.html',{'user_ps': user_ps, 'categories': categories, 'key_skills': key_skills, 'wishlist_profiles': wishlist_profiles})
    # return HttpResponse('this is profile')


def logout1(request):
   logout(request)
   return redirect('login')
  # return HttpResponse('this is profile')

def generate_random_filename(filename):
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    _, extension = os.path.splitext(filename)
    random_filename = f'{timestamp}_{random_string}{extension}'
    return random_filename

def profile_user(request, profile_id):
    profile = get_object_or_404(UserProfile, profile_id=profile_id)
    if request.user.is_superuser:
        mainy='hii'
    else:
        clint_profile = get_object_or_404(ClintProfile, user=request.user)
        return render(request, 'profile_page.html', {'profile': profile, 'clint_profile': clint_profile})
    return render(request, 'profile_page.html', {'profile': profile})

def add_to_wishlist(request, profile_id):
    clint_profile = get_object_or_404(ClintProfile, user=request.user)
    user_profile = get_object_or_404(UserProfile, profile_id=profile_id)

    if user_profile in clint_profile.wishlist.all():
        # Profile is already wishlisted
        messages.error(request, 'Profile is already wishlisted.')
    else:
        clint_profile.wishlist.add(user_profile)
        messages.success(request, 'Profile added to wishlist successfully.')
        notification_message = str(clint_profile)+" Shortlisted "+str(user_profile.name)+"(id: "+str(user_profile)+")"
            # Create a notification
        notification = Notification(user=request.user, message=notification_message)
        notification.save()
    return redirect('user_profile', profile_id=profile_id)


def assign_profile(request):
    if request.method == 'POST':
        selected_clients = request.POST.getlist('clients')
        selected_profiles = request.POST.getlist('profiles')

        try:
            clients = ClintProfile.objects.filter(id__in=selected_clients)
            profiles = UserProfile.objects.filter(id__in=selected_profiles)

            for client in clients:
                client.featured_profile.clear()  # Clear existing featured profiles
                client.featured_profile.add(*profiles)  # Assign selected profiles
                client.is_featured = True
                client.save()


                messages.success(request, 'Featured profiles updated successfully.')
        except Exception as e:
            messages.error(request, f'Error occurred: {str(e)}')

        # Retrieve all client profiles and user profiles
    client_profiles = ClintProfile.objects.all()
    user_profiles = UserProfile.objects.all()
        
    context = {
            'client_profiles': client_profiles,
            'user_profiles': user_profiles
        }
    return render(request, 'assign_profile.html', context)


def add_to_wishlist2(request, profile_id):
    clint_profile = get_object_or_404(ClintProfile, user=request.user)
    user_profile = get_object_or_404(UserProfile, profile_id=profile_id)

    if user_profile in clint_profile.wishlist.all():
        # Profile is already wishlisted
        messages.error(request, 'Profile is already wishlisted.')
    else:
        clint_profile.wishlist.add(user_profile)
        messages.success(request, 'Profile added to wishlist successfully.')
        notification_message = str(clint_profile)+" Shortlisted "+str(user_profile.name)+"(id: "+str(user_profile)+")"
            # Create a notification
        notification = Notification(user=request.user, message=notification_message)
        notification.save()

    return redirect('all_profile')
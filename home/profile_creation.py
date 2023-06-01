
import random
import string
from django.conf import settings

# Function to generate a unique profile_id
def generate_unique_profile_id():
    length = 5
    while True:
        profile_id = 'P' + ''.join(random.choices(string.digits, k=length))
        if not UserProfile.objects.filter(profile_id=profile_id).exists():
            return profile_id

# Function to generate a random filename for the uploaded file
def generate_random_filename(filename):
    chars = string.ascii_letters + string.digits
    random_filename = ''.join(random.choice(chars) for _ in range(10))
    extension = filename.split('.')[-1]
    return f"{random_filename}.{extension}"

def create_profile(name, rating, deliveries, experience, education, email, phone_number, category_ids, key_skill_ids, profile_pic):
    # Process the form data and create a new UserProfile object
    profile = UserProfile(
        profile_id=generate_unique_profile_id(),
        name=name,
        rating=rating,
        deliveries=deliveries,
        experience=experience,
        education=education,
        email=email,
        phone_number=phone_number
    )
    profile.save()

    # Assign categories and key skills to the profile
    categories = Category.objects.filter(pk__in=category_ids)
    key_skills = KeySkill.objects.filter(pk__in=key_skill_ids)
    profile.category.set(categories)
    profile.key_skills.set(key_skills)

    # Save the profile_pic file with a random name
    profile.profile_pic.save(
        generate_random_filename(profile_pic.name),
        profile_pic
    )

    return profile
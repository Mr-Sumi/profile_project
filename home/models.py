from django.contrib.auth.models import User
from django.db import models

class Category(models.Model):
    category_id = models.CharField(max_length=5, unique=True, editable=False)
    category_name = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.category_id = 'C' + str(Category.objects.count() + 1).zfill(3)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.category_id

class KeySkill(models.Model):
    key_skill_id = models.CharField(max_length=5, unique=True, editable=False)
    key_skill_name = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.key_skill_id = 'K' + str(KeySkill.objects.count() + 1).zfill(3)
        super(KeySkill, self).save(*args, **kwargs)

    def __str__(self):
        return self.key_skill_id

class UserProfile(models.Model):
    profile_id = models.CharField(max_length=5, unique=True, editable=False)
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    profile_pic = models.ImageField(upload_to='profile_pics')
    category = models.ManyToManyField(Category)
    rating = models.IntegerField()
    key_skills = models.ManyToManyField(KeySkill)
    deliveries = models.CharField(max_length=255)
    experience = models.CharField(max_length=255)
    education = models.CharField(max_length=255)
    commercial_hr = models.IntegerField(default='00')
    commercial_day = models.IntegerField(default='00')

    def save(self, *args, **kwargs):
        if not self.pk:
            self.profile_id = 'P' + str(UserProfile.objects.count() + 1).zfill(3)
        super(UserProfile, self).save(*args, **kwargs)

    def __str__(self):
        return self.profile_id

class ClintProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    profile_img_url = models.URLField(null=True)
    company = models.CharField(max_length=255)
    designation = models.CharField(max_length=255)
    is_featured = models.BooleanField(default=False)
    featured_profile = models.ManyToManyField(UserProfile, blank=True, null=True, related_name='featured_profiles_custom')
    wishlist = models.ManyToManyField(UserProfile, blank=True,  null=True, related_name='wishlists_custom')

    def __str__(self):
        return self.user.username

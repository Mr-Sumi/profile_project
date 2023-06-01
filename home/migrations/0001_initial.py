# Generated by Django 4.2.1 on 2023-05-26 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_id', models.CharField(editable=False, max_length=5, unique=True)),
                ('category_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='KeySkill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key_skill_id', models.CharField(editable=False, max_length=5, unique=True)),
                ('key_skill_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_id', models.CharField(editable=False, max_length=5, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('phone_number', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('profile_pic', models.ImageField(upload_to='profile_pics')),
                ('rating', models.DecimalField(decimal_places=1, max_digits=2)),
                ('deliveries', models.CharField(max_length=255)),
                ('experience', models.CharField(max_length=255)),
                ('education', models.CharField(max_length=255)),
                ('category', models.ManyToManyField(to='home.category')),
                ('key_skills', models.ManyToManyField(to='home.keyskill')),
            ],
        ),
    ]

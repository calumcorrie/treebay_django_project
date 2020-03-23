# Generated by Django 2.2.3 on 2020-03-23 11:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('treebay', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plant',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='plant_images'),
        ),
        migrations.AlterField(
            model_name='plant',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=6),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL),
        ),
    ]

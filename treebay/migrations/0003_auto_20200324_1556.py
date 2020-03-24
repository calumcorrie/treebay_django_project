# Generated by Django 2.2.3 on 2020-03-24 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('treebay', '0002_auto_20200323_1307'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='plant',
            name='stars',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='starred',
            field=models.ManyToManyField(related_name='stars', to='treebay.Plant'),
        ),
        migrations.AlterField(
            model_name='plant',
            name='picture',
            field=models.ImageField(blank=True, upload_to='plant_images'),
        ),
    ]
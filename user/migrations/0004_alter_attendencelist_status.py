# Generated by Django 3.2 on 2021-09-03 05:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_attendence_attendencelist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendencelist',
            name='status',
            field=models.IntegerField(default=0),
        ),
    ]
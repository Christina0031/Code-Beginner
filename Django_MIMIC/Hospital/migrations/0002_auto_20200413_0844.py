# Generated by Django 3.0.5 on 2020-04-13 00:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Hospital', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='admissions',
            old_name='subject',
            new_name='subject_id',
        ),
    ]

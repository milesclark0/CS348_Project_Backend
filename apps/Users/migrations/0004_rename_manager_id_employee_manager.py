# Generated by Django 4.1.2 on 2022-11-02 00:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0003_alter_employee_avg_rating'),
    ]

    operations = [
        migrations.RenameField(
            model_name='employee',
            old_name='manager_id',
            new_name='manager',
        ),
    ]
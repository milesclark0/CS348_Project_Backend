# Generated by Django 4.1.2 on 2022-12-11 20:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Objects', '0004_alter_review_employee_alter_review_order_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='order_id',
            new_name='order',
        ),
    ]

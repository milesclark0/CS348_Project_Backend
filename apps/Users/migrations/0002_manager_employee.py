# Generated by Django 4.1.2 on 2022-11-01 19:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Manager',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50, unique=True)),
                ('password', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=50)),
                ('zip', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=11, unique=True)),
                ('birth_date', models.DateField()),
                ('hire_date', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50, unique=True)),
                ('password', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=50)),
                ('zip', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=11, unique=True)),
                ('birth_date', models.DateField()),
                ('avg_rating', models.FloatField(default=0.0)),
                ('hire_date', models.DateField(auto_now_add=True)),
                ('manager_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Users.manager')),
            ],
        ),
    ]

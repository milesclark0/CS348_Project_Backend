# Generated by Django 4.1.2 on 2022-11-02 02:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Users', '0004_rename_manager_id_employee_manager'),
    ]

    operations = [
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cart_count', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100, unique=True)),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('count', models.IntegerField(default=0)),
                ('rating', models.DecimalField(decimal_places=1, default=0.0, max_digits=2)),
                ('type', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.DecimalField(decimal_places=2, default=0.0, max_digits=7)),
                ('tip', models.DecimalField(decimal_places=2, default=0.0, max_digits=7)),
                ('date', models.DateField(auto_now_add=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Users.customer')),
                ('employee', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Users.employee')),
                ('items', models.ManyToManyField(to='Objects.cartitem')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.DecimalField(decimal_places=1, default=0.0, max_digits=2)),
                ('date', models.DateField(auto_now_add=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Users.customer')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Users.employee')),
                ('item', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Objects.item')),
                ('order_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Objects.order')),
            ],
        ),
        migrations.AddField(
            model_name='cartitem',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Objects.item'),
        ),
    ]

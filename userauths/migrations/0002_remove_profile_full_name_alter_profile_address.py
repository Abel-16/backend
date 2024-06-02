# Generated by Django 4.2.13 on 2024-06-02 08:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userauths', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='full_name',
        ),
        migrations.AlterField(
            model_name='profile',
            name='address',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, to='userauths.useraddress'),
        ),
    ]

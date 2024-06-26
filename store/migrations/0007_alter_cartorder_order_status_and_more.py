# Generated by Django 4.2.13 on 2024-06-04 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_alter_tax_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartorder',
            name='order_status',
            field=models.CharField(choices=[('pending', 'Pending'), ('fulfilled', 'Fulfilled'), ('Cancelled', 'Cancelled')], default='pending', max_length=100),
        ),
        migrations.AlterField(
            model_name='cartorder',
            name='payment_status',
            field=models.CharField(choices=[('processing', 'Processing'), ('pending', 'Pending'), ('paid', 'Paid'), ('Cancelled', 'Cancelled')], default='processing', max_length=100),
        ),
        migrations.AlterField(
            model_name='product',
            name='status',
            field=models.CharField(choices=[('draft', 'Drafted'), ('disabled', 'Disabled'), ('in_review', 'In review'), ('published', 'Published')], default='published', max_length=100),
        ),
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.IntegerField(choices=[('4', '4 Star'), ('5', '5 Star'), ('3', '3 Star'), ('2', '2 Star'), ('1', '1 Star')], default=None),
        ),
    ]

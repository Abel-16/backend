# Generated by Django 4.2.13 on 2024-06-04 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_alter_cartorder_order_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartorder',
            name='payment_status',
            field=models.CharField(choices=[('processing', 'Processing'), ('paid', 'Paid'), ('Cancelled', 'Cancelled'), ('pending', 'Pending')], default='processing', max_length=100),
        ),
        migrations.AlterField(
            model_name='product',
            name='status',
            field=models.CharField(choices=[('in_review', 'In review'), ('disabled', 'Disabled'), ('published', 'Published'), ('draft', 'Drafted')], default='published', max_length=100),
        ),
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.IntegerField(choices=[('5', '5 Star'), ('2', '2 Star'), ('3', '3 Star'), ('4', '4 Star'), ('1', '1 Star')], default=None),
        ),
    ]

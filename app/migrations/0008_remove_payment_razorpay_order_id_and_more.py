# Generated by Django 4.2.1 on 2023-06-01 10:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_payment_razorpay_order_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='razorpay_order_id',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='razorpay_payment_id',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='razorpay_payment_status',
        ),
    ]

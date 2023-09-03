# Generated by Django 4.2.3 on 2023-08-24 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_orderproduct_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderproduct',
            name='status',
            field=models.CharField(choices=[('delivered', 'delivered'), ('Order Placed', 'Order Placed'), ('out for delivery', 'out for delivery'), ('shipped', 'shipped'), ('cancelled', 'cancelled')], default='Order Placed', max_length=100),
        ),
    ]
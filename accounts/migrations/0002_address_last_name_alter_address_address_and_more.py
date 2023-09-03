# Generated by Django 4.2.3 on 2023-08-21 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='last_name',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='address',
            name='address',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='address',
            name='name',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='address',
            name='phone',
            field=models.CharField(default='', max_length=15),
        ),
        migrations.AlterField(
            model_name='address',
            name='pincode',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='address',
            name='state',
            field=models.CharField(max_length=50),
        ),
    ]

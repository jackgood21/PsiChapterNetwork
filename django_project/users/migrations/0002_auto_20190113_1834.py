# Generated by Django 2.1.3 on 2019-01-13 23:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='major',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='profile',
            name='phone',
            field=models.CharField(max_length=14),
        ),
    ]

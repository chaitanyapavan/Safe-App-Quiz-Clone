# Generated by Django 3.0.3 on 2020-03-29 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('safe_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='status',
            field=models.CharField(default='', max_length=10),
        ),
    ]

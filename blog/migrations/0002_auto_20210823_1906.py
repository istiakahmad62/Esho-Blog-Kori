# Generated by Django 3.1.2 on 2021-08-23 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='excerpt',
            field=models.TextField(max_length=1000),
        ),
    ]
# Generated by Django 3.2.23 on 2024-01-26 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='postpoint',
            name='post_header',
            field=models.CharField(default='HEADER', max_length=250),
        ),
    ]

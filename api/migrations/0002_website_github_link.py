# Generated by Django 4.1.3 on 2024-04-28 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='website',
            name='github_link',
            field=models.TextField(blank=True, null=True),
        ),
    ]

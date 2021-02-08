# Generated by Django 3.1.4 on 2021-02-08 01:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webface', '0006_auto_20210208_0103'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='securitymeta',
            name='company_url',
        ),
        migrations.RemoveField(
            model_name='securitymeta',
            name='description',
        ),
        migrations.RemoveField(
            model_name='securitymeta',
            name='employees',
        ),
        migrations.AddField(
            model_name='securitymeta',
            name='fulltimeemployees',
            field=models.IntegerField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='securitymeta',
            name='logo_url',
            field=models.CharField(default=None, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='securitymeta',
            name='longbusinesssummary',
            field=models.CharField(default=None, max_length=2000, null=True),
        ),
    ]
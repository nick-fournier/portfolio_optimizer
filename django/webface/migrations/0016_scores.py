# Generated by Django 3.1.4 on 2021-02-12 03:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webface', '0015_remove_securitymeta_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Scores',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.IntegerField(default=None, null=True)),
                ('variance', models.DecimalField(decimal_places=10, default=None, max_digits=10, null=True)),
                ('PF_score', models.IntegerField(default=None, null=True)),
                ('PF_score_weighted', models.DecimalField(decimal_places=10, default=None, max_digits=10, null=True)),
                ('ROA', models.DecimalField(decimal_places=10, default=None, max_digits=10, null=True)),
                ('cash', models.DecimalField(decimal_places=10, default=None, max_digits=10, null=True)),
                ('cash_ratio', models.DecimalField(decimal_places=10, default=None, max_digits=10, null=True)),
                ('delta_ROA', models.DecimalField(decimal_places=10, default=None, max_digits=10, null=True)),
                ('accruals', models.DecimalField(decimal_places=10, default=None, max_digits=10, null=True)),
                ('delta_long_leverage_ratio', models.DecimalField(decimal_places=10, default=None, max_digits=10, null=True)),
                ('delta_current_leverage_ratio', models.DecimalField(decimal_places=10, default=None, max_digits=10, null=True)),
                ('delta_shares', models.DecimalField(decimal_places=10, default=None, max_digits=10, null=True)),
                ('delta_gross_margin', models.DecimalField(decimal_places=10, default=None, max_digits=10, null=True)),
                ('delta_asset_turnover', models.DecimalField(decimal_places=10, default=None, max_digits=10, null=True)),
            ],
        ),
    ]

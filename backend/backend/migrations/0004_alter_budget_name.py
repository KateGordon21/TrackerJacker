# Generated by Django 4.2.19 on 2025-03-03 00:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0003_alter_budget_end_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='budget',
            name='name',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]

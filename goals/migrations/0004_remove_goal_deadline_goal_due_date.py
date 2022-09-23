# Generated by Django 4.0.1 on 2022-09-23 12:14

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0003_goal_description_remove_goal_category_goal_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='goal',
            name='deadline',
        ),
        migrations.AddField(
            model_name='goal',
            name='due_date',
            field=models.DateField(verbose_name='Дедлайн'),
            preserve_default=False,
        ),
    ]

# Generated by Django 4.0.1 on 2022-09-23 11:40

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0002_goal'),
    ]

    operations = [
        migrations.AddField(
            model_name='goal',
            name='description',
            field=models.CharField(max_length=500, verbose_name='Описание'),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='goal',
            name='category',
        ),
        migrations.AddField(
            model_name='goal',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='goals.goalcategory', verbose_name='Категории'),
            preserve_default=False,
        ),
    ]

# Generated by Django 4.0.1 on 2022-10-04 11:59

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tguser',
            name='verification_code',
            field=models.CharField(default=django.utils.timezone.now, max_length=51, verbose_name='Код верификации'),
            preserve_default=False,
        ),
    ]
# Generated by Django 2.2.16 on 2022-06-15 23:48

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20210608_0213'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='review',
            options={'ordering': ['pub_date']},
        ),
        migrations.RemoveField(
            model_name='review',
            name='rating',
        ),
        migrations.AlterField(
            model_name='review',
            name='score',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1, 'Минимальная оценка - 1'), django.core.validators.MaxValueValidator(10, 'Максимальная оценка - 10')]),
        ),
    ]

# Generated by Django 3.2 on 2022-05-14 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20220514_1314'),
    ]

    operations = [
        migrations.AddField(
            model_name='theme',
            name='image',
            field=models.URLField(default='https://asd.pl'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='ThemeImage',
        ),
    ]

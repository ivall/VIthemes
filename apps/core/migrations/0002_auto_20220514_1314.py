# Generated by Django 3.2 on 2022-05-14 11:14

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='theme',
            name='name',
            field=models.CharField(default='nazwa', max_length=16),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='theme',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]

# Generated by Django 4.1 on 2022-08-25 12:47

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0012_alter_bookinstance_options_alter_bookinstance_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookinstance',
            name='id',
            field=models.UUIDField(default=uuid.UUID('c8bc722b-2891-4125-a76e-92aaaa4e82f7'), help_text='Unique ID for this particular book across whole library', primary_key=True, serialize=False),
        ),
    ]

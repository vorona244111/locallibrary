# Generated by Django 4.1 on 2022-08-19 12:21

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_language_alter_book_options_alter_bookinstance_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookinstance',
            name='id',
            field=models.UUIDField(default=uuid.UUID('01c87dd5-d389-4da8-9d2f-ce976ccffdb5'), help_text='Unique ID for this particular book across whole library', primary_key=True, serialize=False),
        ),
    ]

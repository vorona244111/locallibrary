# Generated by Django 4.1 on 2022-08-22 13:47

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_alter_bookinstance_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookinstance',
            name='id',
            field=models.UUIDField(default=uuid.UUID('1b8804d9-8124-47bc-aa15-5a082f507ec4'), help_text='Unique ID for this particular book across whole library', primary_key=True, serialize=False),
        ),
    ]

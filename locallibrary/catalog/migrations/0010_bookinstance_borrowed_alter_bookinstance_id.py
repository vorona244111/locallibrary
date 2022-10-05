# Generated by Django 4.1 on 2022-08-24 09:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalog', '0009_alter_bookinstance_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookinstance',
            name='borrowed',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='bookinstance',
            name='id',
            field=models.UUIDField(default=uuid.UUID('39a477df-ed5a-4179-a9e8-e9c02f4bcde4'), help_text='Unique ID for this particular book across whole library', primary_key=True, serialize=False),
        ),
    ]

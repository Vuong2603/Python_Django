# Generated by Django 4.2.5 on 2023-10-12 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appfour', '0013_draft_is_approved'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='status',
            field=models.CharField(default='draft', max_length=50),
        ),
    ]

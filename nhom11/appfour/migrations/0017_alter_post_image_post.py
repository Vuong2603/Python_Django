# Generated by Django 4.2.5 on 2023-10-14 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appfour', '0016_alter_post_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image_post',
            field=models.ImageField(blank=True, null=True, upload_to='image_post/%Y/%m/%d/'),
        ),
    ]

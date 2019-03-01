# Generated by Django 2.1 on 2019-02-27 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mobi', '0014_auto_20190227_0631'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='background',
            field=models.ImageField(upload_to='bg/'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='poster',
            field=models.ImageField(upload_to='poster/'),
        ),
        migrations.AlterField(
            model_name='user',
            name='display_pic',
            field=models.ImageField(null=True, upload_to='display_pic/'),
        ),
    ]

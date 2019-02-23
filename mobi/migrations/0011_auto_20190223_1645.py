# Generated by Django 2.1 on 2019-02-23 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mobi', '0010_auto_20190223_1637'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='background',
            field=models.ImageField(upload_to='static/mobi/img/bg'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='poster',
            field=models.ImageField(upload_to='static/mobi/img/poster'),
        ),
        migrations.AlterField(
            model_name='user',
            name='display_pic',
            field=models.ImageField(null=True, upload_to='static/mobi/img/display_pic'),
        ),
    ]

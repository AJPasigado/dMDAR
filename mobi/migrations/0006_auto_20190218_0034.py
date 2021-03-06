# Generated by Django 2.0.7 on 2019-02-17 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mobi', '0005_auto_20190218_0034'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='genre',
            name='id',
        ),
        migrations.AlterField(
            model_name='genre',
            name='genre',
            field=models.CharField(choices=[('Action', 'ACTION'), ('Adult', 'ADULT'), ('Adventure', 'ADVENTURE'), ('Animation', 'ANIMATION'), ('Biography', 'BIOGRAPHY'), ('Comedy', 'COMEDY'), ('Crime', 'CRIME'), ('Documentary', 'DOCUMENTARY'), ('Drama', 'DRAMA'), ('Family', 'FAMILY'), ('Fantasy', 'FANTASY'), ('Film', 'FILM'), ('Noir', 'NOIR'), ('Game - Show', 'GAMESHOW'), ('History', 'HISTORY'), ('Horror', 'HORROR'), ('Musical', 'MUSICAL'), ('Music', 'MUSIC'), ('Mystery', 'MYSTERY'), ('News', 'NEWS'), ('Reality - TV', 'REALITY'), ('Romance', 'ROMANCE'), ('Sci - Fi', 'SCIFI'), ('Short', 'SHORT'), ('Sport', 'SPORT'), ('Talk - Show', 'TALKSHOW'), ('Thriller', 'THRILLER'), ('War', 'WAR'), ('Western', 'WESTERN')], max_length=15, primary_key=True, serialize=False),
        ),
    ]

# Generated by Django 4.2.4 on 2023-08-11 09:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_remove_follow_uniqe_follow_follow_unique_follow'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='follow',
            options={'ordering': ('-id',), 'verbose_name': 'Подписка', 'verbose_name_plural': 'Подписки'},
        ),
    ]
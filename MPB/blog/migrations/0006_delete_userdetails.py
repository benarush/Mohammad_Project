# Generated by Django 3.1.7 on 2021-03-04 18:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20210109_1410'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserDetails',
        ),
    ]
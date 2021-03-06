# Generated by Django 2.0.2 on 2018-05-31 04:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20180422_2304'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deployhistory',
            name='status',
            field=models.IntegerField(choices=[(0, 'FAIL'), (1, 'SUCCESS'), (2, 'UNKNOWN')]),
        ),
        migrations.AlterField(
            model_name='source',
            name='status',
            field=models.BooleanField(choices=[(0, 'ERROR'), (1, 'PASSED')]),
        ),
    ]

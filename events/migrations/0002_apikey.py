# Generated by Django 4.0 on 2021-12-29 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApiKey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'apikeys',
            },
        ),
    ]

# Generated by Django 4.0.3 on 2022-04-05 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, null=True)),
                ('author', models.CharField(max_length=250, null=True)),
                ('pub_date', models.DateField(null=True)),
                ('ISBN_number', models.CharField(max_length=30, null=True, unique=True)),
                ('number_of_pages', models.IntegerField(null=True)),
                ('URL_to_book_cover', models.URLField(null=True)),
                ('book_language', models.CharField(max_length=15, null=True)),
            ],
        ),
    ]
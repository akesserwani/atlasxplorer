# Generated by Django 4.2.13 on 2024-07-11 09:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserMap',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('private', models.BooleanField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Pin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('lat', models.CharField(max_length=50)),
                ('long', models.CharField(max_length=50)),
                ('notes', models.CharField(max_length=1000)),
                ('usermap', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.usermap')),
            ],
        ),
    ]

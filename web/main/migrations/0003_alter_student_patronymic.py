# Generated by Django 4.0.3 on 2022-04-10 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_student_patronymic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='patronymic',
            field=models.CharField(default='', max_length=32, verbose_name='Отчество'),
            preserve_default=False,
        ),
    ]

# Generated by Django 4.0.5 on 2022-07-17 02:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myResidenceService', '0007_alter_sse_colony_colony_code_alter_sse_colony_empno'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sse_colony',
            name='Colony_code',
            field=models.CharField(max_length=750),
        ),
    ]
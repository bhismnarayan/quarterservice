# Generated by Django 3.2.5 on 2021-10-24 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myResidenceService', '0009_alter_sse_colony_empno'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qtr_occupancy',
            name='Occ_dt',
            field=models.DateField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='qtr_occupancy',
            name='Vac_dt',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
    ]

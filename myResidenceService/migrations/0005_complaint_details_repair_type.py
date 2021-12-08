# Generated by Django 3.2.5 on 2021-10-30 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myResidenceService', '0004_auto_20211024_2025'),
    ]

    operations = [
        migrations.AddField(
            model_name='complaint_details',
            name='Repair_type',
            field=models.CharField(choices=[('Select', 'Select'), ('ROOF LEAKAGE', 'Roof Leakeage'), ('Masonary', 'Masonary Work/Floor Plastering'), ('Pipeline', 'Pipeline/Sanitary'), ('Water', 'Water Supply'), ('CARPENTARY', 'carpentary(Doors/Windows)'), ('DRAINS', 'Drains'), ('HORTICULTURE', 'Horticulture'), ('OTHERS', 'Other')], default='Select', max_length=15),
        ),
    ]
# Generated by Django 4.2.16 on 2024-11-10 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_remove_customuser_address_remove_customuser_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='custom',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
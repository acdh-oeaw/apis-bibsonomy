# Generated by Django 3.1.14 on 2023-01-20 16:18

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("apis_bibsonomy", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="reference",
            name="folio",
            field=models.CharField(
                blank=True,
                help_text="String to more precisely define the location of the information",
                max_length=255,
                null=True,
            ),
        ),
    ]

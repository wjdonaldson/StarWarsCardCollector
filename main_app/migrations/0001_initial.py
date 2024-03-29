# Generated by Django 4.2.3 on 2023-08-01 22:03

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="StarWarsCard",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "series_type",
                    models.CharField(
                        choices=[("B", "Blue"), ("R", "Red"), ("Y", "Yellow")],
                        max_length=1,
                    ),
                ),
                ("card_number", models.IntegerField()),
                ("caption", models.CharField(max_length=100)),
                ("condition", models.CharField(max_length=10)),
                ("description", models.TextField(max_length=250)),
            ],
        ),
    ]

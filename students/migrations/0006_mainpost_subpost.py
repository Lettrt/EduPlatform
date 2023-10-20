# Generated by Django 4.2.6 on 2023-10-20 10:20

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("students", "0005_literature"),
    ]

    operations = [
        migrations.CreateModel(
            name="MainPost",
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
                    "title",
                    models.CharField(max_length=200, verbose_name="Название топика"),
                ),
            ],
            options={
                "ordering": ["-title"],
            },
        ),
        migrations.CreateModel(
            name="Subpost",
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
                ("title", models.TextField(verbose_name="Пост")),
                ("slug", models.SlugField(max_length=250, unique_for_date="publish")),
                ("publish", models.DateTimeField(default=django.utils.timezone.now)),
                (
                    "main_post",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="students.mainpost",
                        verbose_name="Тема поста",
                    ),
                ),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="students.students",
                        verbose_name="Студент",
                    ),
                ),
            ],
        ),
    ]

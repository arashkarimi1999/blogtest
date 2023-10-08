# Generated by Django 4.2.5 on 2023-10-06 19:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('article_module', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'verbose_name': ' article', 'verbose_name_plural': 'articles'},
        ),
        migrations.AlterField(
            model_name='article',
            name='author',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='writer'),
        ),
        migrations.AlterField(
            model_name='article',
            name='date_created',
            field=models.DateField(auto_now_add=True, verbose_name='date writed '),
        ),
        migrations.AlterField(
            model_name='article',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='active/deactive'),
        ),
        migrations.AlterField(
            model_name='article',
            name='selected_categories',
            field=models.ManyToManyField(to='article_module.articlecategory', verbose_name=' categories '),
        ),
        migrations.AlterField(
            model_name='article',
            name='short_description',
            field=models.CharField(max_length=300, verbose_name='short description '),
        ),
        migrations.AlterField(
            model_name='article',
            name='slug',
            field=models.SlugField(max_length=200, unique=True, verbose_name=' URL'),
        ),
        migrations.AlterField(
            model_name='article',
            name='text',
            field=models.TextField(verbose_name='text'),
        ),
        migrations.AlterField(
            model_name='article',
            name='title',
            field=models.CharField(max_length=300, verbose_name='title'),
        ),
    ]

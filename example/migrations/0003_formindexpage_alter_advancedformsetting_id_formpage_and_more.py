# Generated by Django 5.0.6 on 2024-06-04 08:49

import django.db.models.deletion
import wagtail.blocks
import wagtail.fields
import wagtailstreamforms.blocks
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('example', '0002_advancedformsetting'),
        ('wagtailcore', '0093_uploadedfile'),
        ('wagtailstreamforms', '0004_alter_form_id_alter_form_slug_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='FormIndexPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.AlterField(
            model_name='advancedformsetting',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.CreateModel(
            name='FormPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('body', wagtail.fields.StreamField([('form', wagtail.blocks.StructBlock([('form', wagtailstreamforms.blocks.FormChooserBlock()), ('form_action', wagtail.blocks.CharBlock(help_text='The form post action. "" or "." for the current page or a url', required=False)), ('form_reference', wagtailstreamforms.blocks.InfoBlock(help_text='This form will be given a unique reference once saved', required=False))]))])),
                ('form', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='wagtailstreamforms.form')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.DeleteModel(
            name='BasicPage',
        ),
    ]

# Generated by Django 4.2.3 on 2023-07-31 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dash', '0002_sld_chain'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sld_chain',
            name='type_annonce',
            field=models.CharField(default=1, max_length=500),
            preserve_default=False,
        ),
    ]

# Generated by Django 2.2 on 2021-05-18 10:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DetailDocument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.CharField(default='1', max_length=45)),
                ('contents', models.TextField()),
                ('doc_file', models.FileField(upload_to='documents/')),
                ('title', models.CharField(max_length=45)),
                ('pages', models.IntegerField(default=0)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kategori', models.CharField(max_length=45)),
                ('likes', models.CharField(blank=True, max_length=500)),
                ('views', models.CharField(blank=True, max_length=500)),
                ('level', models.IntegerField(default=1)),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='create_date')),
                ('update_date', models.DateTimeField(auto_now_add=True, verbose_name='update_date')),
            ],
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(max_length=45, verbose_name='Action')),
                ('username', models.CharField(max_length=45, verbose_name='Username')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='create time')),
                ('document', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='docs.DetailDocument')),
            ],
        ),
        migrations.AddField(
            model_name='detaildocument',
            name='document',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='documents', to='docs.Document'),
        ),
        migrations.CreateModel(
            name='Bab',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bab', models.CharField(max_length=45, verbose_name='Bab')),
                ('sub_bab', models.CharField(blank=True, max_length=45)),
                ('text', models.TextField()),
                ('page', models.CharField(max_length=45)),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='create_date')),
                ('update_date', models.DateTimeField(auto_now_add=True, verbose_name='update_date')),
                ('detaildocument', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='detaildocuments', to='docs.DetailDocument')),
            ],
        ),
    ]
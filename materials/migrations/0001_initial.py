import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Назва')),
                ('description', models.TextField(blank=True, verbose_name='Опис')),
                ('file', models.FileField(blank=True, upload_to='materials/', verbose_name='Файл')),
                ('url', models.URLField(blank=True, verbose_name='Посилання (у т.ч. YouTube)')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Додано')),
                ('uploaded_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='materials', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Матеріал',
                'verbose_name_plural': 'Матеріали',
                'ordering': ['-created_at'],
            },
        ),
    ]

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
            name='Vote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Питання')),
                ('description', models.TextField(blank=True, verbose_name='Опис')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Створено')),
            ],
            options={
                'verbose_name': 'Голосування',
                'verbose_name_plural': 'Голосування',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=200, verbose_name='Варіант')),
                ('vote', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', to='votes.vote')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Ballot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ballots', to='votes.option')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ballots', to=settings.AUTH_USER_MODEL)),
                ('vote', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ballots', to='votes.vote')),
            ],
        ),
        migrations.AddConstraint(
            model_name='ballot',
            constraint=models.UniqueConstraint(fields=('vote', 'user'), name='unique_ballot_per_user'),
        ),
    ]

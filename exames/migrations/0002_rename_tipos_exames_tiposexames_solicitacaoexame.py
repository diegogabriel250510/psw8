# Generated by Django 4.2.5 on 2023-10-04 00:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('exames', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='tipos_exames',
            new_name='Tiposexames',
        ),
        migrations.CreateModel(
            name='SolicitacaoExame',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('E', 'Em análise'), ('F', 'Finalizado')], max_length=2)),
                ('resultado', models.FileField(blank=True, null=True, upload_to='resultados')),
                ('requer_senha', models.BooleanField(default=False)),
                ('senha', models.CharField(blank=True, max_length=16, null=True)),
                ('exame', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='exames.tiposexames')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

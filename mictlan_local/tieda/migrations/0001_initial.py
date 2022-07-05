# Generated by Django 4.0.5 on 2022-07-04 22:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telefono', models.CharField(max_length=50)),
                ('calle', models.CharField(max_length=50)),
                ('colonia', models.CharField(max_length=50)),
                ('entrecalles', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='PedidoCompleto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.CharField(max_length=30)),
                ('id_pedido', models.IntegerField()),
                ('nombre_pedido', models.CharField(max_length=50)),
                ('cantidad', models.IntegerField()),
                ('precio_unitario', models.IntegerField()),
                ('descripcion', models.CharField(max_length=50)),
                ('montextra', models.IntegerField()),
                ('subtotal', models.IntegerField()),
                ('total', models.IntegerField()),
                ('calle', models.CharField(max_length=50)),
                ('colonia', models.CharField(max_length=50)),
                ('entrecalles', models.CharField(max_length=50)),
                ('telefono', models.CharField(max_length=50)),
                ('estado', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='PedidoIncompleto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_pedido', models.IntegerField()),
                ('nombre', models.CharField(max_length=50)),
                ('cantidad', models.IntegerField()),
                ('precio_unitario', models.IntegerField()),
                ('descripcion', models.CharField(max_length=50)),
                ('montoextra', models.IntegerField()),
                ('subtotal', models.IntegerField()),
                ('total', models.IntegerField()),
            ],
        ),
    ]
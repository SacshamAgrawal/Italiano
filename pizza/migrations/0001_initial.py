# Generated by Django 3.0.4 on 2020-04-01 10:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cart', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'cart',
                'verbose_name_plural': 'carts',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=32, verbose_name='Category Name')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Chef',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name="Chef's Name")),
                ('speciality', models.CharField(default='Chef', max_length=16, verbose_name='Speciality')),
                ('bio', models.TextField(default='Cooking is an art.', max_length=80, verbose_name="Chef's Bio")),
                ('display_picture', models.ImageField(default='default_chef.jpg', upload_to='Chefs', verbose_name='Chefs DP')),
            ],
            options={
                'verbose_name': 'chef',
                'verbose_name_plural': 'chefs',
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Item Name')),
                ('description', models.TextField(default='Will Be Added..', verbose_name='Item Discription')),
                ('image', models.ImageField(upload_to='item-images', verbose_name='Item Image')),
                ('image_thumbnail', models.ImageField(blank=True, null=True, upload_to='item-thumbnails', verbose_name='Item Thumbnail')),
                ('price', models.DecimalField(decimal_places=2, default=20.43, max_digits=7)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='pizza.Category')),
            ],
            options={
                'verbose_name': 'Item',
                'verbose_name_plural': 'Items',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(max_length=13, null=True, verbose_name='ORDER_ID')),
                ('billing_address', models.CharField(max_length=128, verbose_name='Billing Address')),
                ('status', models.IntegerField(choices=[(1, 'NEW'), (2, 'PAID'), (3, 'PROCESSING'), (4, 'SENT_FOR_DELIVERY'), (5, 'COMPLETED')], default=1, verbose_name='STATUS OF ORDER')),
                ('transaction_id', models.CharField(blank=True, max_length=50, verbose_name='TRANSACTION ID')),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='AMOUNT ')),
                ('time', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'order',
                'verbose_name_plural': 'orders',
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pizza.Item')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orderitem', to='pizza.Order')),
            ],
            options={
                'verbose_name': 'OrderItem',
                'verbose_name_plural': 'OrderItems',
            },
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='quantity')),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cartitem', to='pizza.Cart')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pizza.Item')),
            ],
            options={
                'verbose_name': 'CartItem',
                'verbose_name_plural': 'CartItems',
            },
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, null=True)),
                ('address1', models.CharField(max_length=128, null=True, verbose_name='Address line 1')),
                ('address2', models.CharField(max_length=128, null=True, verbose_name='Address line 2')),
                ('zip_code', models.IntegerField(null=True, verbose_name='ZIP / Postal code')),
                ('city', models.CharField(max_length=32, null=True)),
                ('country', models.CharField(choices=[('IN', 'INDIA')], default='IN', max_length=3)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='addresses', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'address',
                'verbose_name_plural': 'addresses',
            },
        ),
    ]

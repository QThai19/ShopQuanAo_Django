# -*- coding: utf-8 -*-
"""
Management command: python manage.py seed_data
Nap du lieu mau: danh muc, san pham voi size va anh placeholder dep.
"""
import urllib.request
import sys
import io
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from store.models import Category, Product, ProductSize, ProductImage

# Fix Windows console encoding
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')


class Command(BaseCommand):
    help = 'Seed sample data for fashion boutique'

    def handle(self, *args, **options):
        print('>>> Dang nap du lieu mau...')

        # Create categories
        categories_data = [
            {'name': 'Dam/Vay', 'slug': 'dam-vay', 'icon': '', 'order': 1},
            {'name': 'Ao kieu', 'slug': 'ao-kieu', 'icon': '', 'order': 2},
            {'name': 'Do bo', 'slug': 'do-bo', 'icon': '', 'order': 3},
            {'name': 'Vest/Blazer', 'slug': 'vest', 'icon': '', 'order': 4},
        ]

        cats = {}
        for cdata in categories_data:
            cat, created = Category.objects.get_or_create(
                slug=cdata['slug'],
                defaults={
                    'name': cdata['name'],
                    'icon': cdata['icon'],
                    'order': cdata['order'],
                }
            )
            cats[cdata['slug']] = cat
            status = 'TAO MOI' if created else 'DA TON TAI'
            print(f'  [{status}] danh muc: {cat.name}')

        # Sample products data
        products_data = [
            {
                'name': 'Dam Lua To Tam Hoa Nho Thanh Lich',
                'category_slug': 'dam-vay',
                'fabric': 'lua',
                'price': 650000,
                'sale_price': 520000,
                'is_featured': True,
                'is_new': True,
                'description': 'Dam lua to tam thien nhien 100%, hoa tiet hoa nho tinh te. Kieu dang A-line ton dang, co V thanh lich. Phu hop di choi, du tiec, hop mat.',
                'sizes': [('M', '44-50kg'), ('L', '50-56kg'), ('XL', '56-62kg'), ('2XL', '62-70kg')],
                'image_url': 'https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?w=600&q=80',
            },
            {
                'name': 'Vay Dui Tu Nhien Co Tron Vintage',
                'category_slug': 'dam-vay',
                'fabric': 'dui',
                'price': 480000,
                'sale_price': None,
                'is_featured': True,
                'is_new': True,
                'description': 'Vay vai dui tu nhien, mem mai, thoang mat. Kieu dang vintage duyen dang. Co tui hai ben tien dung.',
                'sizes': [('M', '44-50kg'), ('L', '50-56kg'), ('XL', '56-62kg'), ('2XL', '62-70kg'), ('3XL', '70-78kg')],
                'image_url': 'https://images.unsplash.com/photo-1496747611176-843222e1e57c?w=600&q=80',
            },
            {
                'name': 'Dam Phi Bong Co Sen Nu Quy Phai',
                'category_slug': 'dam-vay',
                'fabric': 'phi_bong',
                'price': 590000,
                'sale_price': 470000,
                'is_featured': False,
                'is_new': True,
                'description': 'Dam phi bong cao cap, bong min, ru dep. Co sen thanh lich, tay ngan thoang mat. Thiet ke om vua van, ton voc dang.',
                'sizes': [('L', '50-56kg'), ('XL', '56-62kg'), ('2XL', '62-70kg'), ('3XL', '70-78kg')],
                'image_url': 'https://images.unsplash.com/photo-1539008835657-9e8e9680c956?w=600&q=80',
            },
            {
                'name': 'Dam Nhung Tuyet Den Du Tiec',
                'category_slug': 'dam-vay',
                'fabric': 'nhung',
                'price': 780000,
                'sale_price': 620000,
                'is_featured': True,
                'is_new': False,
                'description': 'Dam nhung tuyet den sang trong, phu hop du tiec, khai truong, su kien quan trong. Chat lieu nhung min, khong nhan, giu phom tot.',
                'sizes': [('M', '44-50kg'), ('L', '50-56kg'), ('XL', '56-62kg'), ('2XL', '62-70kg')],
                'image_url': 'https://images.unsplash.com/photo-1502716119720-b23a93e5fe1b?w=600&q=80',
            },
            {
                'name': 'Ao Kieu Kate Thai Theu Hoa',
                'category_slug': 'ao-kieu',
                'fabric': 'kate',
                'price': 350000,
                'sale_price': None,
                'is_featured': False,
                'is_new': True,
                'description': 'Ao kieu Kate Thai theu hoa song dong, mau sac tuoi tan. Tay lo tinh te, co tron nhe nhang.',
                'sizes': [('M', '44-50kg'), ('L', '50-56kg'), ('XL', '56-62kg'), ('2XL', '62-70kg'), ('3XL', '70-78kg')],
                'image_url': 'https://images.unsplash.com/photo-1434389677669-e08b4cac3105?w=600&q=80',
            },
            {
                'name': 'Ao Dui Tha Rong Phong Cach Vintage',
                'category_slug': 'ao-kieu',
                'fabric': 'dui',
                'price': 320000,
                'sale_price': 270000,
                'is_featured': True,
                'is_new': True,
                'description': 'Ao dui tha rong, dang suong thoai mai. Phong cach vintage doc dao, de phoi cung quan ong suong hoac chan vay.',
                'sizes': [('M', '44-52kg'), ('L', '52-60kg'), ('XL', '60-68kg'), ('2XL', '68-75kg')],
                'image_url': 'https://images.unsplash.com/photo-1512436991641-6745cdb1723f?w=600&q=80',
            },
            {
                'name': 'Ao Lua Co Tru Nut Bac Sang Trong',
                'category_slug': 'ao-kieu',
                'fabric': 'lua',
                'price': 420000,
                'sale_price': 360000,
                'is_featured': False,
                'is_new': False,
                'description': 'Ao lua to tam co tru voi hang nut bac tinh xao. Thiet ke thanh lich, phu hop moi truong van phong.',
                'sizes': [('M', '44-50kg'), ('L', '50-56kg'), ('XL', '56-62kg'), ('2XL', '62-70kg')],
                'image_url': 'https://images.unsplash.com/photo-1525507119028-ed4fba0c9e25?w=600&q=80',
            },
            {
                'name': 'Bo Dui Theu Hoa Co Truyen Cao Cap',
                'category_slug': 'do-bo',
                'fabric': 'dui',
                'price': 680000,
                'sale_price': 540000,
                'is_featured': True,
                'is_new': True,
                'description': 'Bo do dui theu hoa co truyen tinh te. Gom ao va quan, chat lieu dui mem mat, theu tay tinh xao.',
                'sizes': [('M', '44-50kg'), ('L', '50-56kg'), ('XL', '56-62kg'), ('2XL', '62-70kg'), ('3XL', '70-78kg')],
                'image_url': 'https://images.unsplash.com/photo-1583744946564-b52ac1c389c8?w=600&q=80',
            },
            {
                'name': 'Bo Lua To Tam In Hoa Nho Diu Dang',
                'category_slug': 'do-bo',
                'fabric': 'lua',
                'price': 750000,
                'sale_price': None,
                'is_featured': False,
                'is_new': True,
                'description': 'Bo do lua to tam in hoa nho tinh te, mem mai va thoang mat. Dang suong thoai mai, phu hop mac hang ngay.',
                'sizes': [('M', '44-50kg'), ('L', '50-56kg'), ('XL', '56-62kg'), ('2XL', '62-70kg')],
                'image_url': 'https://images.unsplash.com/photo-1490481651871-ab68de25d43d?w=600&q=80',
            },
            {
                'name': 'Bo Cotton Cao Cap The Thao Nhe Nhang',
                'category_slug': 'do-bo',
                'fabric': 'cotton',
                'price': 420000,
                'sale_price': 350000,
                'is_featured': False,
                'is_new': False,
                'description': 'Bo do cotton cao cap nhe nhang, phong cach the thao thoai mai. Thich hop mac tap the duc buoi sang, yoga, hoac dao pho.',
                'sizes': [('M', '44-50kg'), ('L', '50-56kg'), ('XL', '56-62kg'), ('2XL', '62-70kg'), ('3XL', '70-78kg')],
                'image_url': 'https://images.unsplash.com/photo-1556821840-3a63f15732ce?w=600&q=80',
            },
            {
                'name': 'Vest Linen Dang Dai Phong Cach Tay',
                'category_slug': 'vest',
                'fabric': 'cotton',
                'price': 890000,
                'sale_price': 720000,
                'is_featured': True,
                'is_new': True,
                'description': 'Vest linen dang dai phong cach tay lich lam. Chat lieu linen cao cap, thoang mat. Phu hop di lam, hop hanh, tiec tung.',
                'sizes': [('M', '44-50kg'), ('L', '50-56kg'), ('XL', '56-62kg'), ('2XL', '62-70kg')],
                'image_url': 'https://images.unsplash.com/photo-1529139574466-a303027c1d8b?w=600&q=80',
            },
            {
                'name': 'Ao Khoac Len Min Cuc Boc Vai',
                'category_slug': 'vest',
                'fabric': 'len',
                'price': 650000,
                'sale_price': None,
                'is_featured': False,
                'is_new': True,
                'description': 'Ao khoac len min voi cuc boc vai tinh te. Giu am hieu qua, kieu dang thanh lich. Co tui trong tien loi.',
                'sizes': [('M', '44-50kg'), ('L', '50-56kg'), ('XL', '56-62kg'), ('2XL', '62-70kg')],
                'image_url': 'https://images.unsplash.com/photo-1551488831-00ddcb6c6bd3?w=600&q=80',
            },
        ]

        created_count = 0

        for pdata in products_data:
            cat = cats.get(pdata['category_slug'])

            if Product.objects.filter(name=pdata['name']).exists():
                print(f'  [SKIP] Da ton tai: {pdata["name"]}')
                continue

            product = Product.objects.create(
                category=cat,
                name=pdata['name'],
                fabric=pdata['fabric'],
                price=pdata['price'],
                sale_price=pdata.get('sale_price'),
                is_featured=pdata.get('is_featured', False),
                is_new=pdata.get('is_new', True),
                description=pdata.get('description', ''),
            )

            for size_name, weight_hint in pdata.get('sizes', []):
                ProductSize.objects.create(
                    product=product,
                    size=size_name,
                    weight_hint=weight_hint,
                    is_available=True,
                )

            img_url = pdata.get('image_url', '')
            if img_url:
                try:
                    req = urllib.request.Request(img_url, headers={'User-Agent': 'Mozilla/5.0'})
                    with urllib.request.urlopen(req, timeout=15) as response:
                        img_data = response.read()

                    img_name = f'{product.slug}.jpg'
                    product_image = ProductImage(
                        product=product,
                        alt_text=product.name,
                        is_main=True,
                        order=0,
                    )
                    product_image.image.save(img_name, ContentFile(img_data), save=True)
                    print(f'  [OK] Tao san pham + anh: {product.name}')
                except Exception as e:
                    print(f'  [WARN] Tao san pham (khong anh): {product.name} - {e}')
            else:
                print(f'  [OK] Tao san pham: {product.name}')

            created_count += 1

        print(f'\n>>> Hoan thanh! Da tao {created_count} san pham moi.')
        print('>>> Truy cap: http://127.0.0.1:8000/')

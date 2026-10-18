import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shopquanao.settings')
django.setup()

from django.contrib.auth import get_user_model
from store.models import Category, Product, ProductSize, ShopSetting, Banner

def seed():
    print("--- DANG KHOI TAO DU LIEU CHO RENDER ---")
    
    # 1. Tao tai khoan Admin
    User = get_user_model()
    admin_user = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
    admin_pass = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin123')
    if not User.objects.filter(username=admin_user).exists():
        User.objects.create_superuser(username=admin_user, email='admin@shopquanao.com', password=admin_pass)
        print(f"-> Da tao admin: {admin_user} / {admin_pass}")

    # 2. Cau hinh ShopSetting
    setting = ShopSetting.get_settings()
    setting.shop_name = "Shop Hồng Loan"
    setting.hotline = "0901 234 567"
    setting.zalo_phone = "0901234567"
    setting.address = "123 Nguyễn Trãi, P.3, Q.5, TP.HCM"
    setting.open_hours = "8:00 - 20:00 (Thứ 2 - Chủ nhật)"
    setting.banner_text = "Giao hàng toàn quốc · Kiểm tra hàng trước khi thanh toán · Đổi trả 7 ngày"
    setting.save()
    print("-> Da khoi tao ShopSetting thanh cong!")

    # 3. Tao Danh muc
    categories_data = [
        {"name": "Đầm/Váy", "slug": "dam-vay", "icon": "👗", "order": 1},
        {"name": "Áo kiểu", "slug": "ao-kieu", "icon": "👚", "order": 2},
        {"name": "Đồ bộ", "slug": "do-bo", "icon": "🧥", "order": 3},
        {"name": "Vest/Blazer", "slug": "vest", "icon": "🥻", "order": 4},
    ]
    cats = {}
    for c in categories_data:
        obj, _ = Category.objects.get_or_create(slug=c["slug"], defaults=c)
        cats[c["slug"]] = obj

    # 4. Tao San pham mau & Bang size
    products_data = [
        {
            "name": "Đầm Suông Lụa Tơ Tằm Họa Tiết Hoa",
            "slug": "dam-suong-lua-to-tam-hoa-tiet-hoa",
            "category": cats["dam-vay"],
            "price": 680000,
            "sale_price": 590000,
            "fabric": "lua",
            "description": "Đầm suông cao cấp chất liệu lụa tơ tằm mềm mại, thoáng mát, hoa văn trang nhã quý phái dành cho phụ nữ trung niên. Phom suông khéo léo che khuyết điểm bụng.",
            "is_featured": True,
            "is_new": True,
            "sizes": [("L", "50-55 kg"), ("XL", "55-62 kg"), ("2XL", "62-70 kg"), ("3XL", "70-80 kg")]
        },
        {
            "name": "Đầm Xòe Vải Đũi Thêu Hoa Sen",
            "slug": "dam-xoe-vai-dui-theu-hoa-sen",
            "category": cats["dam-vay"],
            "price": 550000,
            "sale_price": 480000,
            "fabric": "dui",
            "description": "Đầm xòe nhẹ chất liệu vải đũi tơ tự nhiên, thêu hoa sen tỉ mỉ thủ công, mặc nhẹ nhàng thanh thoát khi dạo phố hay đi lễ.",
            "is_featured": True,
            "is_new": True,
            "sizes": [("M", "45-50 kg"), ("L", "50-55 kg"), ("XL", "55-62 kg"), ("2XL", "62-70 kg")]
        },
        {
            "name": "Áo Kiểu Cổ Tròn Thêu Nổi Tinh Tế",
            "slug": "ao-kieu-co-tron-theu-noi-tinh-te",
            "category": cats["ao-kieu"],
            "price": 420000,
            "sale_price": 360000,
            "fabric": "dui",
            "description": "Áo kiểu trung niên vải đũi cao cấp phối họa tiết thêu nổi trang nhã, phom dáng suông rộng rãi thoải mái cả ngày.",
            "is_featured": True,
            "is_new": True,
            "sizes": [("L", "50-55 kg"), ("XL", "55-62 kg"), ("2XL", "62-70 kg"), ("3XL", "70-80 kg")]
        },
        {
            "name": "Áo Lụa Trung Niên Dáng Suông Quý Phái",
            "slug": "ao-lua-trung-nien-dang-suong-quy-phai",
            "category": cats["ao-kieu"],
            "price": 450000,
            "sale_price": 390000,
            "fabric": "lua",
            "description": "Áo lụa cao cấp mềm rủ, cổ đính ngọc thanh lịch, phù hợp mặc dự tiệc, họp mặt gia đình.",
            "is_featured": True,
            "is_new": False,
            "sizes": [("M", "45-50 kg"), ("L", "50-55 kg"), ("XL", "55-62 kg"), ("2XL", "62-70 kg")]
        },
        {
            "name": "Bộ Đồ Lụa Satin Trung Niên Sang Trọng",
            "slug": "bo-do-lua-satin-trung-nien-sang-trong",
            "category": cats["do-bo"],
            "price": 720000,
            "sale_price": 650000,
            "fabric": "lua",
            "description": "Bộ đồ mặc nhà và dạo phố chất liệu lụa satin loại 1, thoáng mát, mềm mịn, đường may tinh xảo.",
            "is_featured": True,
            "is_new": True,
            "sizes": [("L", "50-55 kg"), ("XL", "55-62 kg"), ("2XL", "62-70 kg"), ("3XL", "70-80 kg")]
        },
        {
            "name": "Bộ Đũi Cổ Tàu Thêu Hoa Thủ Công",
            "slug": "bo-dui-co-tau-theu-hoa-thu-cong",
            "category": cats["do-bo"],
            "price": 580000,
            "sale_price": 490000,
            "fabric": "dui",
            "description": "Bộ quần áo đũi cổ tàu phong cách truyền thống quý phái, chất vải đũi tự nhiên mát rượi.",
            "is_featured": True,
            "is_new": True,
            "sizes": [("L", "50-55 kg"), ("XL", "55-62 kg"), ("2XL", "62-70 kg"), ("3XL", "70-80 kg")]
        },
        {
            "name": "Áo Khoác Blazer Trung Niên Thanh Lịch",
            "slug": "ao-khoac-blazer-trung-nien-thanh-lich",
            "category": cats["vest"],
            "price": 850000,
            "sale_price": 750000,
            "fabric": "cotton",
            "description": "Áo blazer dáng đứng sang trọng, thiết kế phom chuẩn người trung niên, mặc tôn dáng thanh thoát.",
            "is_featured": True,
            "is_new": True,
            "sizes": [("L", "50-55 kg"), ("XL", "55-62 kg"), ("2XL", "62-70 kg")]
        }
    ]

    for p_data in products_data:
        sizes = p_data.pop("sizes")
        slug = p_data["slug"]
        prod, created = Product.objects.get_or_create(slug=slug, defaults=p_data)
        if created:
            for s, hint in sizes:
                ProductSize.objects.create(product=prod, size=s, weight_hint=hint, is_available=True)
            print(f"-> Da tao san pham: {prod.name}")

    print("--- HOAN TAT KHOI TAO DU LIEU SAN PHAM ---")

if __name__ == '__main__':
    seed()

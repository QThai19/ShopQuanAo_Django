"""
Script to update product and category names to proper Vietnamese.
Run: python fix_names.py
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shopquanao.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from store.models import Category, Product

# Fix category names
cat_names = {
    'dam-vay': 'Đầm/Váy',
    'ao-kieu': 'Áo kiểu',
    'do-bo': 'Đồ bộ',
    'vest': 'Vest/Blazer',
}
cat_icons = {
    'dam-vay': '👗',
    'ao-kieu': '👚',
    'do-bo': '🧥',
    'vest': '🥻',
}

for slug, name in cat_names.items():
    Category.objects.filter(slug=slug).update(name=name, icon=cat_icons[slug])
    print(f'Updated category: {name}')

# Fix product names
product_updates = {
    'Dam Lua To Tam Hoa Nho Thanh Lich': 'Đầm Lụa Tơ Tằm Hoa Nhỏ Thanh Lịch',
    'Vay Dui Tu Nhien Co Tron Vintage': 'Váy Đũi Tự Nhiên Cổ Tròn Vintage',
    'Dam Phi Bong Co Sen Nu Quy Phai': 'Đầm Phi Bóng Cổ Sen Nữ Quý Phái',
    'Dam Nhung Tuyet Den Du Tiec': 'Đầm Nhung Tuyết Đen Dự Tiệc',
    'Ao Kieu Kate Thai Theu Hoa': 'Áo Kiểu Kate Thái Thêu Hoa',
    'Ao Dui Tha Rong Phong Cach Vintage': 'Áo Đũi Thả Rộng Phong Cách Vintage',
    'Ao Lua Co Tru Nut Bac Sang Trong': 'Áo Lụa Cổ Trụ Nút Bạc Sang Trọng',
    'Bo Dui Theu Hoa Co Truyen Cao Cap': 'Bộ Đũi Thêu Hoa Cổ Truyền Cao Cấp',
    'Bo Lua To Tam In Hoa Nho Diu Dang': 'Bộ Lụa Tơ Tằm In Hoa Nhỏ Dịu Dàng',
    'Bo Cotton Cao Cap The Thao Nhe Nhang': 'Bộ Cotton Cao Cấp Thể Thao Nhẹ Nhàng',
    'Vest Linen Dang Dai Phong Cach Tay': 'Vest Linen Dáng Dài Phong Cách Tây',
    'Ao Khoac Len Min Cuc Boc Vai': 'Áo Khoác Len Mịn Cúc Bọc Vải',
}

for old_name, new_name in product_updates.items():
    updated = Product.objects.filter(name=old_name).update(name=new_name)
    if updated:
        print(f'Updated: {new_name}')

# Fix descriptions
desc_updates = {
    'Đầm Lụa Tơ Tằm Hoa Nhỏ Thanh Lịch': 'Đầm lụa tơ tằm thiên nhiên 100%, họa tiết hoa nhỏ tinh tế. Kiểu dáng A-line tôn dáng, cổ V thanh lịch. Phù hợp đi chơi, dự tiệc, họp mặt gia đình.',
    'Váy Đũi Tự Nhiên Cổ Tròn Vintage': 'Váy vải đũi tự nhiên, mềm mại, thoáng mát. Kiểu dáng vintage duyên dáng, màu sắc trung tính dễ phối đồ. Có túi hai bên tiện dụng.',
    'Đầm Phi Bóng Cổ Sen Nữ Quý Phái': 'Đầm phi bóng cao cấp, bóng mịn, rủ đẹp. Cổ sen thanh lịch, tay ngắn thoáng mát. Thiết kế ôm vừa vặn, tôn vóc dáng người phụ nữ trung niên.',
    'Đầm Nhung Tuyết Đen Dự Tiệc': 'Đầm nhung tuyết đen sang trọng, phù hợp dự tiệc, khai trương, sự kiện quan trọng. Chất liệu nhung mịn, không nhăn, giữ phom tốt suốt cả ngày.',
    'Áo Kiểu Kate Thái Thêu Hoa': 'Áo kiểu Kate Thái thêu hoa sống động, màu sắc tươi tắn. Tay lỡ tinh tế, cổ tròn nhẹ nhàng. Phù hợp mặc dạo phố, đi chơi cuối tuần.',
    'Áo Đũi Thả Rộng Phong Cách Vintage': 'Áo đũi thả rộng, dáng suông thoải mái. Phong cách vintage độc đáo, dễ phối cùng quần ống suông hoặc chân váy. Mặc được 4 mùa.',
    'Áo Lụa Cổ Trụ Nút Bạc Sang Trọng': 'Áo lụa tơ tằm cổ trụ với hàng nút bạc tinh xảo. Thiết kế thanh lịch, phù hợp môi trường văn phòng và sự kiện trang trọng.',
    'Bộ Đũi Thêu Hoa Cổ Truyền Cao Cấp': 'Bộ đồ đũi thêu hoa cổ truyền tinh tế. Gồm áo và quần, chất liệu đũi mềm mát, thêu tay tinh xảo. Set đồ sang trọng phù hợp mặc ở nhà hay đi chơi.',
    'Bộ Lụa Tơ Tằm In Hoa Nhỏ Dịu Dàng': 'Bộ đồ lụa tơ tằm in hoa nhỏ tinh tế, mềm mại và thoáng mát. Dáng suông thoải mái, phù hợp mặc hàng ngày và đi chơi cuối tuần.',
    'Bộ Cotton Cao Cấp Thể Thao Nhẹ Nhàng': 'Bộ đồ cotton cao cấp nhẹ nhàng, phong cách thể thao thoải mái. Thích hợp mặc tập thể dục buổi sáng, yoga, hoặc dạo phố.',
    'Vest Linen Dáng Dài Phong Cách Tây': 'Vest linen dáng dài phong cách tây lịch lãm. Chất liệu linen cao cấp, thoáng mát. Phù hợp đi làm, họp hành, tiệc tùng sang trọng.',
    'Áo Khoác Len Mịn Cúc Bọc Vải': 'Áo khoác len mịn với cúc bọc vải tinh tế. Giữ ấm hiệu quả, kiểu dáng thanh lịch. Có túi trong tiện lợi.',
}

for name, desc in desc_updates.items():
    Product.objects.filter(name=name).update(description=desc)

print('\nAll names and descriptions updated to Vietnamese!')
print('Server running at: http://127.0.0.1:8000/')

import os
import sys
import django

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shopquanao.settings')
django.setup()

from django.core.management import call_command
from django.contrib.auth import get_user_model
from store.models import Category, Product, ShopSetting

def seed():
    print("=== DANG NAP DU LIEU CO SO DU LIEU CHO RENDER / CLOUD ===")

    # 1. Nap toan bo du lieu tu data_backup.json neu co
    backup_path = os.path.join(os.path.dirname(__file__), 'data_backup.json')
    if os.path.exists(backup_path):
        try:
            call_command('loaddata', 'data_backup.json')
            print("-> Da nap thanh cong 84 doi tuong tu data_backup.json!")
        except Exception as e:
            print(f"Luu y khi nap data_backup.json: {e}")

    # 2. Tao hoac dat lai mat khau tai khoan Admin
    User = get_user_model()
    admin_user = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
    admin_pass = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin123')
    admin_email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@shopquanao.com')

    if not User.objects.filter(username=admin_user).exists():
        User.objects.create_superuser(username=admin_user, email=admin_email, password=admin_pass)
        print(f"-> Da tao tai khoan Admin: {admin_user} / {admin_pass}")
    else:
        u = User.objects.get(username=admin_user)
        u.set_password(admin_pass)
        u.is_staff = True
        u.is_superuser = True
        u.save()
        print(f"-> Da cap nhat quyen va mat khau cho Admin: {admin_user}")

    # 3. Dam bao ShopSetting duoc kich hoat
    try:
        setting = ShopSetting.get_settings()
        setting.shop_name = "Shop Hồng Loan"
        if not setting.hotline:
            setting.hotline = "0866191976"
            setting.zalo_phone = "0866191976"
        setting.save()
        print(f"-> Cai dat cua hang: {setting.shop_name} | Hotline: {setting.hotline}")
    except Exception as e:
        print(f"Loi ShopSetting: {e}")

    # Thong ke
    prod_count = Product.objects.count()
    cat_count = Category.objects.count()
    print(f"=== HOAN TAT: Hien co {cat_count} danh muc, {prod_count} san pham san sang ===")

if __name__ == '__main__':
    seed()

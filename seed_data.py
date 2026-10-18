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

    # Kiem tra DATABASE_URL co duoc cau hinh khong
    db_url = os.environ.get('DATABASE_URL', '')
    if db_url:
        print(f"-> Dang dung PostgreSQL: {db_url[:30]}...")
    else:
        print("-> CANH BAO: Khong tim thay DATABASE_URL, dang dung SQLite!")

    # 1. Nap toan bo du lieu tu data_backup.json neu co
    backup_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data_backup.json')
    print(f"-> Tim file backup tai: {backup_path}")
    if os.path.exists(backup_path):
        print("-> Bat dau nap data_backup.json...")
        try:
            call_command('loaddata', backup_path, verbosity=2)
            print("-> Da nap thanh cong tu data_backup.json!")
        except Exception as e:
            print(f"CANH BAO khi nap data_backup.json: {type(e).__name__}: {e}")
            print("-> Thu lai voi duong dan tuong doi...")
            try:
                call_command('loaddata', 'data_backup.json', verbosity=1)
                print("-> Nap thanh cong voi duong dan tuong doi!")
            except Exception as e2:
                print(f"LOI NGHIEM TRONG khi loaddata: {type(e2).__name__}: {e2}")
    else:
        print(f"LOI: Khong tim thay file backup tai {backup_path}")

    # 2. Tao hoac dat lai mat khau tai khoan Admin
    User = get_user_model()
    admin_user = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
    admin_pass = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin123')
    admin_email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@shopquanao.com')

    try:
        if not User.objects.filter(username=admin_user).exists():
            User.objects.create_superuser(username=admin_user, email=admin_email, password=admin_pass)
            print(f"-> Da tao tai khoan Admin: {admin_user}")
        else:
            u = User.objects.get(username=admin_user)
            u.set_password(admin_pass)
            u.is_staff = True
            u.is_superuser = True
            u.save()
            print(f"-> Da cap nhat quyen va mat khau cho Admin: {admin_user}")
    except Exception as e:
        print(f"LOI tao Admin: {e}")

    # 3. Dam bao ShopSetting duoc kich hoat
    try:
        setting = ShopSetting.get_settings()
        setting.shop_name = "Shop Hong Loan"
        if not setting.hotline:
            setting.hotline = "0866191976"
            setting.zalo_phone = "0866191976"
        setting.save()
        print(f"-> Cai dat cua hang OK | Hotline: {setting.hotline}")
    except Exception as e:
        print(f"Loi ShopSetting: {e}")

    # Thong ke cuoi
    try:
        prod_count = Product.objects.count()
        cat_count = Category.objects.count()
        print(f"=== HOAN TAT: {cat_count} danh muc, {prod_count} san pham ===")
        if prod_count == 0:
            print("!!! CANH BAO: Khong co san pham nao! Kiem tra data_backup.json !!!")
    except Exception as e:
        print(f"Loi dem san pham: {e}")

if __name__ == '__main__':
    seed()

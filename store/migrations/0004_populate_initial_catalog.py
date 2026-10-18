import os
from django.db import migrations
from django.core.management import call_command

def load_catalog_data(apps, schema_editor):
    db_alias = schema_editor.connection.alias
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    fixture_path = os.path.join(base_dir, 'data_backup.json')
    
    if os.path.exists(fixture_path):
        print(f"\n[MIGRATION] Dang nap du lieu san pham tu {fixture_path} vao database '{db_alias}'...")
        try:
            call_command('loaddata', fixture_path, database=db_alias, verbosity=1)
            print("[MIGRATION] -> Nap thanh cong 24 san pham va danh muc vao database!")
        except Exception as e:
            print(f"[MIGRATION WARNING] Khong the nap fixture: {e}")
            # Try fallback to relative path
            try:
                call_command('loaddata', 'data_backup.json', database=db_alias, verbosity=1)
            except Exception as e2:
                print(f"[MIGRATION WARNING] Fallback cung that bai: {e2}")

def unload_catalog_data(apps, schema_editor):
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_alter_banner_options_alter_order_options_and_more'),
    ]

    operations = [
        migrations.RunPython(load_catalog_data, reverse_code=unload_catalog_data),
    ]

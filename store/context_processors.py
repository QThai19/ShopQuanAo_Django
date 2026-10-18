from .models import ShopSetting


def shop_settings(request):
    try:
        setting = ShopSetting.get_settings()
    except Exception:
        setting = None
    return {
        'shop_setting': setting
    }

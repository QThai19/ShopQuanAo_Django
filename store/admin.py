from django.contrib import admin
from django.utils.html import format_html, format_html_join
from django.utils.safestring import mark_safe
from django.urls import reverse
from .models import Category, Product, ProductSize, ProductImage, Order, Banner, ShopSetting


# ============================================================
# INLINE MODELS
# ============================================================
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ['image_preview', 'image', 'alt_text', 'is_main', 'order']
    readonly_fields = ['image_preview']

    def image_preview(self, obj):
        if obj and obj.image:
            try:
                return format_html(
                    '<img src="{}" style="width: 50px; height: 65px; object-fit: cover; border-radius: 6px; box-shadow: 0 1px 3px rgba(0,0,0,0.15);" />',
                    obj.image.url
                )
            except Exception:
                pass
        return mark_safe('<span style="color:#94a3b8; font-size: 12px;">Chưa chọn ảnh</span>')
    image_preview.short_description = "Xem trước"


class ProductSizeInline(admin.TabularInline):
    model = ProductSize
    extra = 2
    fields = ['size', 'weight_hint', 'is_available']


# ============================================================
# CATEGORY ADMIN
# ============================================================
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['icon_name_display', 'slug', 'products_count_link', 'order']
    list_editable = ['order']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'slug']
    ordering = ['order', 'name']

    def icon_name_display(self, obj):
        icon = obj.icon or '📁'
        return format_html('<span style="font-size: 20px; margin-right: 8px;">{}</span><strong>{}</strong>', icon, obj.name)
    icon_name_display.short_description = "Tên danh mục"

    def products_count_link(self, obj):
        count = obj.products.count()
        url = reverse('admin:store_product_changelist') + f'?category__id__exact={obj.pk}'
        return format_html(
            '<a href="{}" class="badge badge-info" style="font-size: 13px; padding: 5px 10px; text-decoration: none;">🛍️ {} sản phẩm</a>',
            url, count
        )
    products_count_link.short_description = "Số lượng sản phẩm"


# ============================================================
# PRODUCT ADMIN
# ============================================================
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'image_thumbnail',
        'name',
        'category',
        'price_display',
        'fabric_badge',
        'sizes_display',
        'is_featured',
        'is_active',
        'created_at_display'
    ]
    list_filter = ['category', 'fabric', 'is_new', 'is_featured', 'is_active', 'created_at']
    search_fields = ['name', 'description', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline, ProductSizeInline]
    list_editable = ['is_featured', 'is_active']
    list_per_page = 15

    fieldsets = (
        ("🏷️ Thông tin sản phẩm", {
            "fields": ("name", "category", "fabric", "slug"),
            "description": "Nhập tên và phân loại danh mục, chất liệu của mẫu thời trang."
        }),
        ("💰 Giá bán & Khuyến mãi", {
            "fields": (("price", "sale_price"),),
            "description": "Nếu có giá khuyến mãi, website sẽ tự động hiển thị tem giảm giá % tương ứng."
        }),
        ("📝 Mô tả chi tiết", {
            "fields": ("description",),
            "classes": ("collapse",),
            "description": "Mô tả chất vải, form dáng, cách giặt ủi và các điểm nổi bật."
        }),
        ("⚙️ Cấu hình hiển thị", {
            "fields": (("is_new", "is_featured", "is_active"),),
            "description": "Bật 'Hàng mới' để có tem Mới, 'Nổi bật' để đưa lên đầu trang chủ, 'Đang hiển thị' để mở bán."
        }),
    )

    def image_thumbnail(self, obj):
        img_url = obj.main_image_url
        if img_url:
            return format_html(
                '<img src="{}" style="width: 48px; height: 64px; object-fit: cover; border-radius: 6px; box-shadow: 0 2px 6px rgba(0,0,0,0.12);" alt="{}" />',
                img_url, obj.name
            )
        return mark_safe(
            '<div style="width: 48px; height: 64px; background: #f1f5f9; border-radius: 6px; display: flex; align-items: center; justify-content: center; font-size: 22px;">👗</div>'
        )
    image_thumbnail.short_description = "Ảnh đại diện"

    def price_display(self, obj):
        if obj.sale_price and obj.sale_price > 0:
            return format_html(
                '<div><strong style="color: #e11d48; font-size: 14px;">{}</strong><br><small style="color: #94a3b8; text-decoration: line-through;">{}</small></div>',
                obj.formatted_sale_price, obj.formatted_price
            )
        return format_html('<strong style="color: #0f172a; font-size: 14px;">{}</strong>', obj.formatted_price)
    price_display.short_description = "Giá bán"

    def fabric_badge(self, obj):
        return format_html(
            '<span class="badge badge-warning" style="font-size: 12px; font-weight: 600; padding: 4px 8px;">🧵 {}</span>',
            obj.get_fabric_display_name()
        )
    fabric_badge.short_description = "Chất liệu"

    def sizes_display(self, obj):
        sizes = obj.sizes.filter(is_available=True)
        if sizes.exists():
            return format_html_join(
                '',
                '<span class="badge badge-light" style="margin: 1px 2px; font-size: 11px; padding: 3px 6px; border: 1px solid #cbd5e1;">{}</span>',
                ((s.size,) for s in sizes)
            )
        return mark_safe('<span style="color:#94a3b8; font-size:12px;">Chưa cấu hình size</span>')
    sizes_display.short_description = "Size sẵn có"

    def created_at_display(self, obj):
        return obj.created_at.strftime('%d/%m/%Y')
    created_at_display.short_description = "Ngày đăng"

    # Custom Bulk Actions
    @admin.action(description="⭐ Đặt thành Sản phẩm Nổi bật")
    def make_featured(self, request, queryset):
        count = queryset.update(is_featured=True)
        self.message_user(request, f"Đã đánh dấu {count} sản phẩm thành Nổi bật.")

    @admin.action(description="Bỏ đánh dấu Nổi bật")
    def remove_featured(self, request, queryset):
        count = queryset.update(is_featured=False)
        self.message_user(request, f"Đã bỏ nổi bật cho {count} sản phẩm.")

    @admin.action(description="👁️ Hiển thị trên website (Kích hoạt)")
    def make_active(self, request, queryset):
        count = queryset.update(is_active=True)
        self.message_user(request, f"Đã kích hoạt hiển thị {count} sản phẩm.")

    @admin.action(description="🚫 Tạm ẩn khỏi website")
    def make_inactive(self, request, queryset):
        count = queryset.update(is_active=False)
        self.message_user(request, f"Đã ẩn {count} sản phẩm.")

    actions = ['make_featured', 'remove_featured', 'make_active', 'make_inactive']


# ============================================================
# ORDER ADMIN
# ============================================================
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'order_id_badge',
        'customer_info',
        'product_info',
        'total_price',
        'status',
        'created_at_display'
    ]
    list_editable = ['status']
    list_filter = ['status', 'created_at']
    search_fields = ['customer_name', 'customer_phone', 'customer_address', 'id', 'note']
    readonly_fields = ['created_at']
    list_per_page = 20

    fieldsets = (
        ("👤 Thông tin khách hàng", {
            "fields": ("customer_name", "customer_phone", "customer_address"),
            "description": "Họ tên, số điện thoại liên hệ và địa chỉ nhận hàng của khách."
        }),
        ("📦 Chi tiết đặt hàng", {
            "fields": ("product", "size", "status", "note"),
            "description": "Sản phẩm, kích cỡ và trạng thái đơn hàng."
        }),
        ("🕒 Thời gian", {
            "fields": ("created_at",),
        }),
    )

    def order_id_badge(self, obj):
        return format_html(
            '<span class="badge badge-dark" style="font-family: monospace; font-size: 13px; padding: 5px 8px;">#{}</span>',
            obj.pk
        )
    order_id_badge.short_description = "Mã đơn"

    def customer_info(self, obj):
        return format_html(
            '<div><strong style="font-size: 14px; color: #0f172a;">{}</strong><br>'
            '<a href="tel:{}" style="color: #2563eb; font-weight: 600; text-decoration: none;">📞 {}</a><br>'
            '<small style="color: #64748b;">📍 {}</small></div>',
            obj.customer_name, obj.customer_phone, obj.customer_phone, obj.customer_address
        )
    customer_info.short_description = "Khách hàng"

    def product_info(self, obj):
        if obj.product:
            img_html = ''
            img_url = obj.product.main_image_url
            if img_url:
                img_html = format_html(
                    '<img src="{}" style="width: 34px; height: 44px; object-fit: cover; border-radius: 4px; margin-right: 8px; vertical-align: middle;" />',
                    img_url
                )
            return format_html(
                '<div>{}<strong style="vertical-align: middle;">{}</strong>'
                '<br><small style="color: #64748b;">Size: <span class="badge badge-secondary">{}</span></small></div>',
                img_html, obj.product.name, obj.size or "Mặc định"
            )
        return mark_safe('<span style="color: #94a3b8;">Sản phẩm đã xóa</span>')
    product_info.short_description = "Sản phẩm đặt mua"

    def total_price(self, obj):
        if obj.product:
            return format_html(
                '<strong style="color: #e11d48; font-size: 15px;">{}</strong>',
                obj.product.formatted_display_price
            )
        return mark_safe('<span style="color:#94a3b8;">-</span>')
    total_price.short_description = "Tổng tiền"

    def created_at_display(self, obj):
        return obj.created_at.strftime('%d/%m/%Y %H:%M')
    created_at_display.short_description = "Thời gian đặt"

    # Custom Bulk Actions
    @admin.action(description="🔵 Đổi thành: Đã xác nhận")
    def mark_confirmed(self, request, queryset):
        updated = queryset.update(status='confirmed')
        self.message_user(request, f"Đã cập nhật {updated} đơn hàng thành 'Đã xác nhận'.")

    @admin.action(description="🟣 Đổi thành: Đang giao hàng")
    def mark_shipping(self, request, queryset):
        updated = queryset.update(status='shipping')
        self.message_user(request, f"Đã cập nhật {updated} đơn hàng thành 'Đang giao hàng'.")

    @admin.action(description="🟢 Đổi thành: Đã giao thành công")
    def mark_delivered(self, request, queryset):
        updated = queryset.update(status='delivered')
        self.message_user(request, f"Đã cập nhật {updated} đơn hàng thành 'Đã giao thành công'.")

    @admin.action(description="🔴 Đổi thành: Đã hủy")
    def mark_cancelled(self, request, queryset):
        updated = queryset.update(status='cancelled')
        self.message_user(request, f"Đã cập nhật {updated} đơn hàng thành 'Đã hủy'.")

    actions = ['mark_confirmed', 'mark_shipping', 'mark_delivered', 'mark_cancelled']


# ============================================================
# BANNER ADMIN
# ============================================================
@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ['banner_preview', 'title', 'subtitle', 'link', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    search_fields = ['title', 'subtitle', 'link']

    fieldsets = (
        ("Thông tin Banner", {
            "fields": ("title", "subtitle", "image", "link", ("order", "is_active")),
        }),
    )

    def banner_preview(self, obj):
        if obj and obj.image:
            try:
                return format_html(
                    '<img src="{}" style="width: 130px; height: 50px; object-fit: cover; border-radius: 6px; box-shadow: 0 1px 4px rgba(0,0,0,0.15);" />',
                    obj.image.url
                )
            except Exception:
                pass
        return mark_safe('<span style="color:#94a3b8; font-size: 12px;">Chưa có ảnh</span>')
    banner_preview.short_description = "Xem trước Banner"


# ============================================================
# SHOP SETTING ADMIN (CẤU HÌNH SHOP, HOTLINE, ZALO)
# ============================================================
@admin.register(ShopSetting)
class ShopSettingAdmin(admin.ModelAdmin):
    list_display = ['shop_name', 'hotline', 'zalo_phone', 'address', 'open_hours']
    fieldsets = (
        ("📞 Thông tin liên hệ & Hotline", {
            "fields": ("shop_name", "hotline", "zalo_phone", "banner_text"),
            "description": "Chỉnh sửa số điện thoại Hotline và số Zalo tư vấn. Website và Chatbot AI sẽ tự động đồng bộ theo số này."
        }),
        ("📍 Địa chỉ & Giờ làm việc", {
            "fields": ("address", "open_hours", "facebook_url"),
            "description": "Địa chỉ cửa hàng và link mạng xã hội hiển thị dưới chân trang (Footer)."
        }),
    )

    def has_add_permission(self, request):
        if self.model.objects.count() >= 1:
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        return False

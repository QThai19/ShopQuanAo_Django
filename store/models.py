from django.db import models
from django.utils.text import slugify
from django.urls import reverse
import uuid


VIETNAMESE_MAP = {
    'à': 'a', 'á': 'a', 'ả': 'a', 'ã': 'a', 'ạ': 'a',
    'ă': 'a', 'ằ': 'a', 'ắ': 'a', 'ẳ': 'a', 'ẵ': 'a', 'ặ': 'a',
    'â': 'a', 'ầ': 'a', 'ấ': 'a', 'ẩ': 'a', 'ẫ': 'a', 'ậ': 'a',
    'đ': 'd', 'è': 'e', 'é': 'e', 'ẻ': 'e', 'ẽ': 'e', 'ẹ': 'e',
    'ê': 'e', 'ề': 'e', 'ế': 'e', 'ể': 'e', 'ễ': 'e', 'ệ': 'e',
    'ì': 'i', 'í': 'i', 'ỉ': 'i', 'ĩ': 'i', 'ị': 'i',
    'ò': 'o', 'ó': 'o', 'ỏ': 'o', 'õ': 'o', 'ọ': 'o',
    'ô': 'o', 'ồ': 'o', 'ố': 'o', 'ổ': 'o', 'ỗ': 'o', 'ộ': 'o',
    'ơ': 'o', 'ờ': 'o', 'ớ': 'o', 'ở': 'o', 'ỡ': 'o', 'ợ': 'o',
    'ù': 'u', 'ú': 'u', 'ủ': 'u', 'ũ': 'u', 'ụ': 'u',
    'ư': 'u', 'ừ': 'u', 'ứ': 'u', 'ử': 'u', 'ữ': 'u', 'ự': 'u',
    'ỳ': 'y', 'ý': 'y', 'ỷ': 'y', 'ỹ': 'y', 'ỵ': 'y',
    'À': 'A', 'Á': 'A', 'Ả': 'A', 'Ã': 'A', 'Ạ': 'A',
    'Ă': 'A', 'Ằ': 'A', 'Ắ': 'A', 'Ẳ': 'A', 'Ẵ': 'A', 'Ặ': 'A',
    'Â': 'A', 'Ầ': 'A', 'Ấ': 'A', 'Ẩ': 'A', 'Ẫ': 'A', 'Ậ': 'A',
    'Đ': 'D', 'È': 'E', 'É': 'E', 'Ẻ': 'E', 'Ẽ': 'E', 'Ẹ': 'E',
    'Ê': 'E', 'Ề': 'E', 'Ế': 'E', 'Ể': 'E', 'Ễ': 'E', 'Ệ': 'E',
    'Ì': 'I', 'Í': 'I', 'Ỉ': 'I', 'Ĩ': 'I', 'Ị': 'I',
    'Ò': 'O', 'Ó': 'O', 'Ỏ': 'O', 'Õ': 'O', 'Ọ': 'O',
    'Ô': 'O', 'Ồ': 'O', 'Ố': 'O', 'Ổ': 'O', 'Ỗ': 'O', 'Ộ': 'O',
    'Ơ': 'O', 'Ờ': 'O', 'Ớ': 'O', 'Ở': 'O', 'Ỡ': 'O', 'Ợ': 'O',
    'Ù': 'U', 'Ú': 'U', 'Ủ': 'U', 'Ũ': 'U', 'Ụ': 'U',
    'Ư': 'U', 'Ừ': 'U', 'Ứ': 'U', 'Ử': 'U', 'Ữ': 'U', 'Ự': 'U',
    'Ỳ': 'Y', 'Ý': 'Y', 'Ỷ': 'Y', 'Ỹ': 'Y', 'Ỵ': 'Y'
}


def vietnamese_slugify(text):
    """Chuyển chuỗi tiếng Việt thành slug an toàn chuẩn SEO (giữ chữ đ/Đ thành d/D)."""
    if not text:
        return ''
    for vi, en in VIETNAMESE_MAP.items():
        text = text.replace(vi, en)
    return slugify(text)


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Tên danh mục")
    slug = models.SlugField(unique=True, blank=True, max_length=150)
    icon = models.CharField(max_length=50, blank=True, default='👗', verbose_name="Icon biểu tượng")
    order = models.PositiveIntegerField(default=0, verbose_name="Thứ tự hiển thị")

    class Meta:
        verbose_name = "Danh mục"
        verbose_name_plural = "Danh mục sản phẩm"
        ordering = ['order', 'name']

    def __str__(self):
        return f"{self.icon} {self.name}" if self.icon else self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = vietnamese_slugify(self.name) or 'danh-muc'
            slug = base_slug
            counter = 1
            while Category.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)


class Product(models.Model):
    FABRIC_CHOICES = [
        ('dui', 'Vải đũi'),
        ('lua', 'Lụa tơ tằm'),
        ('cotton', 'Cotton cao cấp'),
        ('phi_bong', 'Phi bóng'),
        ('kate', 'Kate Thái'),
        ('len', 'Len mịn'),
        ('nhung', 'Nhung tuyết'),
        ('chiffon', 'Chiffon'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products', verbose_name="Danh mục")
    name = models.CharField(max_length=200, verbose_name="Tên sản phẩm")
    slug = models.SlugField(unique=True, blank=True, max_length=250)
    description = models.TextField(verbose_name="Mô tả sản phẩm", blank=True)
    fabric = models.CharField(max_length=20, choices=FABRIC_CHOICES, default='dui', verbose_name="Chất liệu vải")
    price = models.DecimalField(max_digits=12, decimal_places=0, verbose_name="Giá gốc (VNĐ)")
    sale_price = models.DecimalField(max_digits=12, decimal_places=0, null=True, blank=True, verbose_name="Giá khuyến mãi (VNĐ)")
    is_new = models.BooleanField(default=True, verbose_name="Hàng mới về")
    is_featured = models.BooleanField(default=False, verbose_name="Sản phẩm nổi bật")
    is_active = models.BooleanField(default=True, verbose_name="Đang hiển thị bán")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")

    class Meta:
        verbose_name = "Sản phẩm"
        verbose_name_plural = "Sản phẩm"
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = vietnamese_slugify(self.name) or 'san-pham'
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('store:product_detail', kwargs={'slug': self.slug})

    @property
    def display_price(self):
        return self.sale_price if (self.sale_price is not None and self.sale_price > 0) else self.price

    @property
    def formatted_price(self):
        return f"{int(self.price):,}".replace(",", ".") + " đ"

    @property
    def formatted_sale_price(self):
        if self.sale_price is not None and self.sale_price > 0:
            return f"{int(self.sale_price):,}".replace(",", ".") + " đ"
        return ""

    @property
    def formatted_display_price(self):
        price = self.display_price
        return f"{int(price):,}".replace(",", ".") + " đ"

    @property
    def discount_percent(self):
        if self.sale_price and self.price > 0 and self.sale_price < self.price:
            return int((1 - self.sale_price / self.price) * 100)
        return 0

    @property
    def main_image(self):
        img = self.images.filter(is_main=True).first()
        if not img:
            img = self.images.first()
        return img

    @property
    def main_image_url(self):
        """Trả về URL ảnh chính an toàn, không bị văng Exception khi chưa có file."""
        img = self.main_image
        if img and img.image:
            try:
                return img.image.url
            except ValueError:
                return ''
        return ''

    def get_fabric_display_name(self):
        return dict(self.FABRIC_CHOICES).get(self.fabric, self.fabric)


class ProductSize(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sizes', verbose_name="Sản phẩm")
    size = models.CharField(max_length=20, verbose_name="Size (M, L, XL, 2XL...)")
    weight_hint = models.CharField(max_length=60, verbose_name="Gợi ý cân nặng (vd: 50 - 55 kg)", blank=True)
    is_available = models.BooleanField(default=True, verbose_name="Còn hàng")

    class Meta:
        verbose_name = "Size sản phẩm"
        verbose_name_plural = "Bảng Size sản phẩm"
        ordering = ['size']

    def __str__(self):
        hint = f" ({self.weight_hint})" if self.weight_hint else ""
        return f"{self.product.name} - Size {self.size}{hint}"


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name="Sản phẩm")
    image = models.ImageField(upload_to='products/', verbose_name="File hình ảnh")
    alt_text = models.CharField(max_length=200, blank=True, verbose_name="Mô tả ảnh")
    is_main = models.BooleanField(default=False, verbose_name="Đặt làm ảnh chính đại diện")
    order = models.PositiveIntegerField(default=0, verbose_name="Thứ tự ảnh")

    class Meta:
        verbose_name = "Ảnh sản phẩm"
        verbose_name_plural = "Ảnh sản phẩm"
        ordering = ['-is_main', 'order']

    def __str__(self):
        return f"Ảnh: {self.product.name} (#{self.pk})"

    @property
    def safe_url(self):
        if self.image:
            try:
                return self.image.url
            except ValueError:
                return ''
        return ''


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', '🟡 Chờ xử lý'),
        ('confirmed', '🔵 Đã xác nhận'),
        ('shipping', '🟣 Đang giao hàng'),
        ('delivered', '🟢 Đã giao thành công'),
        ('cancelled', '🔴 Đã hủy'),
    ]

    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, verbose_name="Sản phẩm đặt")
    size = models.CharField(max_length=20, blank=True, verbose_name="Size đặt")
    customer_name = models.CharField(max_length=100, verbose_name="Họ tên người nhận")
    customer_phone = models.CharField(max_length=20, verbose_name="Số điện thoại")
    customer_address = models.TextField(verbose_name="Địa chỉ nhận hàng")
    note = models.TextField(blank=True, verbose_name="Ghi chú đơn hàng")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Trạng thái đơn hàng")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Thời gian đặt")

    class Meta:
        verbose_name = "Đơn hàng"
        verbose_name_plural = "Quản lý Đơn hàng"
        ordering = ['-created_at']

    def __str__(self):
        return f"Đơn #{self.pk} - {self.customer_name} ({self.customer_phone})"

    @property
    def order_price(self):
        if self.product:
            return self.product.formatted_display_price
        return "-"


class Banner(models.Model):
    title = models.CharField(max_length=200, verbose_name="Tiêu đề banner")
    subtitle = models.CharField(max_length=300, blank=True, verbose_name="Dòng chữ phụ")
    image = models.ImageField(upload_to='banners/', verbose_name="Hình ảnh banner")
    link = models.CharField(max_length=200, blank=True, verbose_name="Đường dẫn liên kết (vd: /bo-suu-tap/)")
    is_active = models.BooleanField(default=True, verbose_name="Kích hoạt hiển thị")
    order = models.PositiveIntegerField(default=0, verbose_name="Thứ tự hiển thị")

    class Meta:
        verbose_name = "Banner Trang Chủ"
        verbose_name_plural = "Banner Trang Chủ"
        ordering = ['order']

    def __str__(self):
        return self.title


class ShopSetting(models.Model):
    shop_name = models.CharField(max_length=150, default="Shop Hồng Loan", verbose_name="Tên cửa hàng")
    hotline = models.CharField(max_length=25, default="0866191976", verbose_name="Số Hotline tư vấn (vd: 0866191976)")
    zalo_phone = models.CharField(max_length=25, default="0866191976", verbose_name="Số Zalo nhận tin (vd: 0866191976)")
    address = models.CharField(max_length=255, default="Chợ Cổ Cò, Cái Bè, Đồng Tháp", verbose_name="Địa chỉ cửa hàng")
    open_hours = models.CharField(max_length=100, default="8:00 - 20:00 (Hàng ngày)", verbose_name="Giờ mở cửa")
    facebook_url = models.CharField(max_length=255, blank=True, default="https://facebook.com", verbose_name="Link Facebook Fanpage")
    banner_text = models.CharField(max_length=255, default="Giao hàng toàn quốc · Đổi trả 7 ngày", verbose_name="Thông báo thanh trên cùng")

    class Meta:
        verbose_name = "Cài đặt Cửa Hàng (Hotline, Zalo, Địa chỉ)"
        verbose_name_plural = "Cài đặt Cửa Hàng (Hotline, Zalo, Địa chỉ)"

    def __str__(self):
        return f"{self.shop_name} (Hotline: {self.hotline} | Zalo: {self.zalo_phone})"

    @classmethod
    def get_settings(cls):
        obj, _ = cls.objects.get_or_create(id=1)
        return obj

    @property
    def clean_zalo_number(self):
        clean = ''.join(c for c in self.zalo_phone if c.isdigit())
        return clean if clean else "0866191976"

    @property
    def zalo_link(self):
        return f"https://zalo.me/{self.clean_zalo_number}"

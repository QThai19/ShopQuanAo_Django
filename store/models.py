from django.db import models
from django.utils.text import slugify
from django.urls import reverse
import uuid


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Tên danh mục")
    slug = models.SlugField(unique=True, blank=True)
    icon = models.CharField(max_length=50, blank=True, default='👗', verbose_name="Icon")
    order = models.PositiveIntegerField(default=0, verbose_name="Thứ tự")

    class Meta:
        verbose_name = "Danh mục"
        verbose_name_plural = "Danh mục sản phẩm"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
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
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="Giá gốc")
    sale_price = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True, verbose_name="Giá khuyến mãi")
    is_new = models.BooleanField(default=True, verbose_name="Hàng mới")
    is_featured = models.BooleanField(default=False, verbose_name="Nổi bật")
    is_active = models.BooleanField(default=True, verbose_name="Hiển thị")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Sản phẩm"
        verbose_name_plural = "Sản phẩm"
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
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
        return self.sale_price if self.sale_price else self.price

    @property
    def formatted_price(self):
        return f"{int(self.price):,}".replace(",", ".") + " đ"

    @property
    def formatted_sale_price(self):
        if self.sale_price:
            return f"{int(self.sale_price):,}".replace(",", ".") + " đ"
        return ""

    @property
    def formatted_display_price(self):
        price = self.display_price
        return f"{int(price):,}".replace(",", ".") + " đ"

    @property
    def discount_percent(self):
        if self.sale_price and self.price > 0:
            return int((1 - self.sale_price / self.price) * 100)
        return 0

    @property
    def main_image(self):
        img = self.images.filter(is_main=True).first()
        if not img:
            img = self.images.first()
        return img

    def get_fabric_display_name(self):
        return dict(self.FABRIC_CHOICES).get(self.fabric, self.fabric)


class ProductSize(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sizes', verbose_name="Sản phẩm")
    size = models.CharField(max_length=10, verbose_name="Size")
    weight_hint = models.CharField(max_length=50, verbose_name="Gợi ý cân nặng", blank=True)
    is_available = models.BooleanField(default=True, verbose_name="Còn hàng")

    class Meta:
        verbose_name = "Size sản phẩm"
        verbose_name_plural = "Size sản phẩm"
        ordering = ['size']

    def __str__(self):
        return f"{self.product.name} - {self.size}"


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name="Sản phẩm")
    image = models.ImageField(upload_to='products/', verbose_name="Hình ảnh")
    alt_text = models.CharField(max_length=200, blank=True, verbose_name="Mô tả ảnh")
    is_main = models.BooleanField(default=False, verbose_name="Ảnh chính")
    order = models.PositiveIntegerField(default=0, verbose_name="Thứ tự")

    class Meta:
        verbose_name = "Ảnh sản phẩm"
        verbose_name_plural = "Ảnh sản phẩm"
        ordering = ['-is_main', 'order']

    def __str__(self):
        return f"Ảnh {self.product.name}"


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Chờ xử lý'),
        ('confirmed', 'Đã xác nhận'),
        ('shipping', 'Đang giao hàng'),
        ('delivered', 'Đã giao'),
        ('cancelled', 'Đã hủy'),
    ]

    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, verbose_name="Sản phẩm")
    size = models.CharField(max_length=10, blank=True, verbose_name="Size")
    customer_name = models.CharField(max_length=100, verbose_name="Họ tên")
    customer_phone = models.CharField(max_length=15, verbose_name="Số điện thoại")
    customer_address = models.TextField(verbose_name="Địa chỉ")
    note = models.TextField(blank=True, verbose_name="Ghi chú")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Trạng thái")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Đơn hàng"
        verbose_name_plural = "Đơn hàng"
        ordering = ['-created_at']

    def __str__(self):
        return f"Đơn #{self.pk} - {self.customer_name}"


class Banner(models.Model):
    title = models.CharField(max_length=200, verbose_name="Tiêu đề")
    subtitle = models.CharField(max_length=300, blank=True, verbose_name="Phụ đề")
    image = models.ImageField(upload_to='banners/', verbose_name="Hình ảnh")
    link = models.CharField(max_length=200, blank=True, verbose_name="Đường dẫn")
    is_active = models.BooleanField(default=True, verbose_name="Hiển thị")
    order = models.PositiveIntegerField(default=0, verbose_name="Thứ tự")

    class Meta:
        verbose_name = "Banner"
        verbose_name_plural = "Banner"
        ordering = ['order']

    def __str__(self):
        return self.title


class ShopSetting(models.Model):
    shop_name = models.CharField(max_length=150, default="Shop Hồng Loan", verbose_name="Tên cửa hàng")
    hotline = models.CharField(max_length=25, default="0901 234 567", verbose_name="Số Hotline tư vấn (ví dụ: 0901 234 567)")
    zalo_phone = models.CharField(max_length=25, default="0901234567", verbose_name="Số Zalo nhận tin nhắn (viết liền, ví dụ: 0901234567)")
    address = models.CharField(max_length=255, default="123 Nguyễn Trãi, P.3, Q.5, TP.HCM", verbose_name="Địa chỉ cửa hàng")
    open_hours = models.CharField(max_length=100, default="8:00 - 20:00 (Thứ 2 - Chủ nhật)", verbose_name="Giờ mở cửa")
    facebook_url = models.CharField(max_length=255, blank=True, default="https://facebook.com", verbose_name="Link Facebook Fanpage")
    banner_text = models.CharField(max_length=255, default="Giao hàng toàn quốc · Đổi trả 7 ngày", verbose_name="Dòng chữ thanh thông báo trên cùng")

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
        return clean if clean else "0901234567"

    @property
    def zalo_link(self):
        return f"https://zalo.me/{self.clean_zalo_number}"

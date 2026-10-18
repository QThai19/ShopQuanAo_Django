from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import Product, Category, Order, Banner, ProductImage
from .chatbot import ask_chatbot
import json
import logging

chat_logger = logging.getLogger(__name__)


def home(request):
    categories = Category.objects.all()
    featured_products = Product.objects.filter(is_featured=True, is_active=True)[:6]
    new_products = Product.objects.filter(is_new=True, is_active=True)[:8]
    banners = Banner.objects.filter(is_active=True)[:5]

    # Get all products for catalog
    selected_category = request.GET.get('category', '').strip()
    if selected_category:
        products = Product.objects.filter(category__slug=selected_category, is_active=True)
    else:
        products = Product.objects.filter(is_active=True)

    context = {
        'categories': categories,
        'featured_products': featured_products,
        'new_products': new_products,
        'banners': banners,
        'products': products,
        'selected_category': selected_category,
        'page_title': 'Thời Trang Trung Niên Cao Cấp | Shop Hồng Loan',
    }
    return render(request, 'store/home.html', context)


def catalog(request):
    categories = Category.objects.all()
    selected_category = request.GET.get('category', '').strip()

    products = Product.objects.filter(is_active=True).select_related('category').prefetch_related('images', 'sizes')
    if selected_category:
        products = products.filter(category__slug=selected_category)

    context = {
        'categories': categories,
        'products': products,
        'selected_category': selected_category,
        'page_title': 'Bộ Sưu Tập Thời Trang | Shop Hồng Loan',
    }
    return render(request, 'store/catalog.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    images = product.images.all()
    sizes = product.sizes.filter(is_available=True)
    related_products = Product.objects.filter(
        category=product.category, is_active=True
    ).exclude(pk=product.pk)[:4]

    # Build Open Graph meta tags an toàn
    og_image_url = ''
    if product.main_image_url:
        try:
            og_image_url = request.build_absolute_uri(product.main_image_url)
        except Exception:
            og_image_url = ''

    context = {
        'product': product,
        'images': images,
        'sizes': sizes,
        'related_products': related_products,
        'og_image_url': og_image_url,
        'page_title': f'{product.name} | Shop Hồng Loan',
        'page_description': product.description[:160] if product.description else f'Mẫu {product.name} chất liệu {product.get_fabric_display_name()} cao cấp tại Shop Hồng Loan',
    }
    return render(request, 'store/product_detail.html', context)


@csrf_exempt
@require_POST
def place_order(request):
    """API Đặt hàng nhanh từ Website"""
    try:
        data = json.loads(request.body.decode('utf-8'))
        product_id = data.get('product_id')
        if not product_id:
            return JsonResponse({'success': False, 'message': 'Vui lòng chọn sản phẩm cần đặt!'}, status=400)

        product = get_object_or_404(Product, pk=product_id)

        customer_name = data.get('name', '').strip()
        customer_phone = data.get('phone', '').strip()
        customer_address = data.get('address', '').strip()
        size = data.get('size', '').strip()
        note = data.get('note', '').strip()

        if not customer_name:
            return JsonResponse({'success': False, 'message': 'Dạ cô/chú/chị vui lòng nhập họ tên để bên em tiện liên hệ!'}, status=400)

        if not customer_phone or len(customer_phone) < 9:
            return JsonResponse({'success': False, 'message': 'Dạ cô/chú/chị vui lòng nhập đúng số điện thoại nhận hàng nhé ạ!'}, status=400)

        order = Order.objects.create(
            product=product,
            size=size,
            customer_name=customer_name,
            customer_phone=customer_phone,
            customer_address=customer_address,
            note=note,
            status='pending',
        )

        return JsonResponse({
            'success': True,
            'message': f'Dạ đặt hàng thành công! Mã đơn #{order.pk}. Nhân viên Shop Hồng Loan sẽ liên hệ gọi điện xác nhận trong ít phút.',
            'order_id': order.pk,
        })
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Dữ liệu gửi lên không hợp lệ.'}, status=400)
    except Exception as e:
        chat_logger.error(f"Lỗi tạo đơn hàng: {e}")
        return JsonResponse({'success': False, 'message': f'Có lỗi xảy ra: {str(e)}'}, status=400)


def about(request):
    context = {
        'page_title': 'Về Chúng Tôi | Shop Hồng Loan',
    }
    return render(request, 'store/about.html', context)


@csrf_exempt
@require_POST
def api_chat(request):
    """API Endpoint nhận câu hỏi từ Chatbot AI và trả về phản hồi tư vấn."""
    try:
        data = json.loads(request.body.decode('utf-8'))
        user_message = data.get('message', '').strip()
        history = data.get('history', [])

        if not user_message:
            return JsonResponse({
                'success': False,
                'message': 'Dạ cô/chú/chị vui lòng nhập câu hỏi để em hỗ trợ nhé ạ! 🌸'
            }, status=400)

        reply = ask_chatbot(user_message, history=history)

        return JsonResponse({
            'success': True,
            'reply': reply
        })
    except Exception as e:
        chat_logger.error(f"Lỗi xử lý chat API: {e}")
        return JsonResponse({
            'success': False,
            'message': 'Dạ đường truyền tư vấn đang gián đoạn một chút, cô/chú/chị có thể bấm Gọi Hotline hoặc nhắn Zalo để bên em hỗ trợ ngay nhé ạ!'
        }, status=500)

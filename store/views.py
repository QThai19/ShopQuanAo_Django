from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import Product, Category, Order, Banner, ProductImage
import json


def home(request):
    categories = Category.objects.all()
    featured_products = Product.objects.filter(is_featured=True, is_active=True)[:6]
    new_products = Product.objects.filter(is_new=True, is_active=True)[:8]
    banners = Banner.objects.filter(is_active=True)[:5]
    
    # Get all products for catalog
    selected_category = request.GET.get('category', '')
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
    selected_category = request.GET.get('category', '')
    
    products = Product.objects.filter(is_active=True).select_related('category').prefetch_related('images')
    if selected_category:
        products = products.filter(category__slug=selected_category)

    context = {
        'categories': categories,
        'products': products,
        'selected_category': selected_category,
        'page_title': 'Bộ Sưu Tập | Shop Hồng Loan',
    }
    return render(request, 'store/catalog.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    images = product.images.all()
    sizes = product.sizes.filter(is_available=True)
    related_products = Product.objects.filter(
        category=product.category, is_active=True
    ).exclude(pk=product.pk)[:4]

    # Build Open Graph meta tags
    main_image = product.main_image
    og_image_url = request.build_absolute_uri(main_image.image.url) if main_image else ''

    context = {
        'product': product,
        'images': images,
        'sizes': sizes,
        'related_products': related_products,
        'og_image_url': og_image_url,
        'page_title': f'{product.name} | Shop Hồng Loan',
        'page_description': product.description[:160] if product.description else f'Mua {product.name} chất liệu {product.get_fabric_display_name()} cao cấp tại Shop Hồng Loan',
    }
    return render(request, 'store/product_detail.html', context)


from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
@require_POST
def place_order(request):
    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
        product = get_object_or_404(Product, pk=product_id)
        
        order = Order.objects.create(
            product=product,
            size=data.get('size', ''),
            customer_name=data.get('name', ''),
            customer_phone=data.get('phone', ''),
            customer_address=data.get('address', ''),
            note=data.get('note', ''),
        )
        return JsonResponse({
            'success': True,
            'message': f'Đặt hàng thành công! Mã đơn #{order.pk}. Chúng tôi sẽ gọi lại cho bạn trong vòng 30 phút.',
            'order_id': order.pk,
        })
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)


def about(request):
    context = {
        'page_title': 'Về Chúng Tôi | Shop Hồng Loan',
    }
    return render(request, 'store/about.html', context)


from .chatbot import ask_chatbot
import logging

chat_logger = logging.getLogger(__name__)


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


from django.contrib.postgres import search
from django.views.generic import ListView, DetailView
from django.db.models import Avg
from .models import Category, Product, Subcategory, Brand
from django.shortcuts import redirect, get_object_or_404, render


class ProductListView(ListView):
    model = Product
    template_name = 'store/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = Product.objects.annotate(
            average_rating=Avg('reviews__rating')
        )

        search = self.request.GET.get('search')
        category = self.request.GET.get('category')
        subcategory = self.request.GET.get('subcategory')
        brand = self.request.GET.get('brand')
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        rating = self.request.GET.get('rating')

        if search:
            queryset = queryset.filter(name__icontains=search)

        if category:
            queryset = queryset.filter(category_id=category)

        if subcategory:
            queryset = queryset.filter(subcategory_id=subcategory)

        if brand:
            queryset = queryset.filter(brand__id=brand)

        if min_price:
            queryset = queryset.filter(price__gte=min_price)

        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        if rating:
            queryset = queryset.filter(average_rating__gte=rating)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        cart = self.request.session.get('cart', {})
        context['cart_count'] = sum(cart.values())

        context['categories'] = Category.objects.all()
        context['subcategories'] = Subcategory.objects.all()
        context['brands'] = Brand.objects.all()
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'store/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['reviews'] = self.object.reviews.all()

        return context


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart = request.session.get('cart', {})

    product_id = str(product.id)

    if product_id in cart:
        cart[product_id] += 1
    else:
        cart[product_id] = 1

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('product-list')


def cart_view(request):
    cart = request.session.get('cart', {})

    cart_items = []
    total_price = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)

        item_total = product.price * quantity
        total_price += item_total

        cart_items.append({
            'product': product,
            'quantity': quantity,
            'item_total': item_total,
        })

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }

    return render(request, 'store/cart.html', context)


def update_cart(request, product_id, action):
    cart = request.session.get('cart', {})

    product_id = str(product_id)

    if product_id in cart:

        if action == 'increase':
            cart[product_id] += 1

        elif action == 'decrease':
            cart[product_id] -= 1

            if cart[product_id] <= 0:
                del cart[product_id]

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('cart')


def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})

    product_id = str(product_id)

    if product_id in cart:
        del cart[product_id]

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('cart')









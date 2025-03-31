from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from .models import Product, ProductImage, Category, Favorite
from .forms import ProductForm
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.views import View


class ProductListView(ListView):
    model = Product
    template_name = 'marketplace/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        today = timezone.now().date()
        queryset = Product.objects.filter(is_active=True).exclude(expires_at__lt=today)
        request = self.request

        q = request.GET.get('q')
        price_min = request.GET.get('price_min')
        price_max = request.GET.get('price_max')
        product_type = request.GET.get('type')

        if q:
            queryset = queryset.filter(
                Q(title__icontains=q) | Q(description__icontains=q)
            )
        if price_min:
            queryset = queryset.filter(price__gte=price_min)
        if price_max:
            queryset = queryset.filter(price__lte=price_max)
        if product_type:
            queryset = queryset.filter(type=product_type)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['q'] = self.request.GET.get('q', '')
        context['price_min'] = self.request.GET.get('price_min', '')
        context['price_max'] = self.request.GET.get('price_max', '')
        context['type'] = self.request.GET.get('type', '')

        if self.request.user.is_authenticated:
            context['favorite_ids'] = Favorite.objects.filter(user=self.request.user).values_list('product_id', flat=True)

        return context


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'marketplace/product_create.html'
    success_url = reverse_lazy('marketplace')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        response = super().form_valid(form)
        images = self.request.FILES.getlist('images')
        for image in images:
            ProductImage.objects.create(product=self.object, image=image)
        return response


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'marketplace/product_edit.html'
    success_url = reverse_lazy('marketplace')

    def form_valid(self, form):
        response = super().form_valid(form)
        images = self.request.FILES.getlist('images')
        if images:
            self.object.images.all().delete()
            for image in images:
                ProductImage.objects.create(product=self.object, image=image)
        return response

    def test_func(self):
        return self.get_object().owner == self.request.user
    

class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    template_name = 'marketplace/product_delete.html'
    success_url = reverse_lazy('marketplace')

    def test_func(self):
        product = self.get_object()
        return product.owner == self.request.user
    
    
class ProductDetailView(DetailView):
    model = Product
    template_name = 'marketplace/product_detail.html'
    context_object_name = 'product'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'


class AddToFavoritesView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        Favorite.objects.get_or_create(user=request.user, product=product)
        return redirect(request.META.get('HTTP_REFERER', 'marketplace'))
    

class RemoveFromFavoritesView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        Favorite.objects.filter(user=request.user, product=product).delete()
        return redirect(request.META.get('HTTP_REFERER', 'marketplace'))
    
    
class FavoriteListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'marketplace/favorite_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.filter(favorited_by__user=self.request.user, is_active=True).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['favorite_ids'] = Favorite.objects.filter(user=self.request.user).values_list('product_id', flat=True)
        return context
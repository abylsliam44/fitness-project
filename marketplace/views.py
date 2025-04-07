from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.db.models import Q
from django.utils import timezone
from django.views import View
from .models import Product, ProductImage, Category, Favorite, Comment, ProductView
from .forms import ProductForm, CommentForm, CommentReplyForm
from django.template.loader import render_to_string
from django.http import JsonResponse
from datetime import timedelta
from django.template.response import TemplateResponse


class ProductListView(ListView):
    model = Product
    template_name = 'marketplace/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = Product.objects.active()
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
        form.instance.owner = self.request.user
        form.instance.latitude = self.request.POST.get('latitude')  
        form.instance.longitude = self.request.POST.get('longitude')  

        response = super().form_valid(form)
        images = self.request.FILES.getlist('images')
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

    def get_queryset(self):
        return Product.objects.active()

    def get_client_ip(self):
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip

    def track_view(self, product):
        user = self.request.user
        ip = self.get_client_ip()
        time_threshold = timezone.now() - timedelta(hours=6)

        if user.is_authenticated:
            has_viewed = ProductView.objects.filter(
                product=product, user=user, viewed_at__gte=time_threshold
            ).exists()
        else:
            has_viewed = ProductView.objects.filter(
                product=product, ip_address=ip, viewed_at__gte=time_threshold
            ).exists()

        if not has_viewed:
            ProductView.objects.create(
                product=product,
                user=user if user.is_authenticated else None,
                ip_address=None if user.is_authenticated else ip
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object

        self.track_view(product)

        context['comments'] = product.comments.select_related('author').order_by('-created_at')
        context['comment_form'] = CommentForm()
        context['reply_forms'] = {
            comment.id: CommentReplyForm(instance=comment)
            for comment in product.comments.all()
        }
        if self.request.user.is_authenticated:
            context['favorite_ids'] = Favorite.objects.filter(user=self.request.user).values_list('product_id', flat=True)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        product = self.object

        if 'comment_submit' in request.POST:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.product = product
                comment.author = request.user
                comment.save()

        elif 'reply_submit' in request.POST:
            comment_id = request.POST.get('comment_id')
            comment = get_object_or_404(Comment, id=comment_id, product=product)
            if request.user == product.owner and not comment.reply:
                form = CommentReplyForm(request.POST, instance=comment)
                if form.is_valid():
                    reply = form.save(commit=False)
                    reply.replied_at = timezone.now()
                    reply.save()

        return redirect('product_detail', slug=product.slug)


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
        return Product.objects.active().filter(favorited_by__user=self.request.user).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['favorite_ids'] = Favorite.objects.filter(user=self.request.user).values_list('product_id', flat=True)
        return context
    


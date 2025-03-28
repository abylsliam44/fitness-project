from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from .models import Product, ProductImage, Category
from .forms import ProductForm

class ProductListView(ListView):
    model = Product
    template_name = 'marketplace/product_list.html'
    context_object_name = 'products'
    queryset = Product.objects.filter(is_active=True).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'marketplace/create_product.html'
    success_url = reverse_lazy('product_list')

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
    template_name = 'marketplace/edit_product.html'
    success_url = reverse_lazy('product_list')

    def test_func(self):
        product = self.get_object()
        return product.owner == self.request.user
    

class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    template_name = 'marketplace/delete_product.html'
    success_url = reverse_lazy('product_list')

    def test_func(self):
        product = self.get_object()
        return product.owner == self.request.user
    
    
class ProductDetailView(DetailView):
    model = Product
    template_name = 'marketplace/product_detail.html'
    context_object_name = 'product'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

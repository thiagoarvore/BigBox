import json
from django.shortcuts import render, redirect, get_object_or_404
from bigbox.models import Category, Product, Kit
from django.views import View
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from bigbox.forms import ProductModelForm, KitModelForm, ProductSelectionForm, CategoryModelForm


@method_decorator(login_required(login_url='login'), name='dispatch')
class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryModelForm
    template_name = 'new_category.html'
    success_url = '/products_list/'


@method_decorator(login_required(login_url='login'), name='dispatch')
class ProductsListView(ListView):
    model = Product
    template_name = 'products_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = super().get_queryset().order_by('name')
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(name__icontains=search)
        return queryset


class Test(View):

    def get(self, request, *args, **kwargs):
        return render(template_name='test.html', request=request)


@method_decorator(login_required(login_url='login'), name='dispatch')
class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'


@method_decorator(login_required(login_url='login'), name='dispatch')
class ProductCreateView(CreateView):
    model = Product
    form_class = ProductModelForm
    template_name = 'new_product.html'
    success_url = '/products_list/'


@method_decorator(login_required(login_url='login'), name='dispatch')
class ProductUpdateView(UpdateView):
    model = Product
    form_model = ProductModelForm
    template_name = 'product_update.html'
    success_url = '/product_detail/'
    fields = '__all__'

    def get_success_url(self):
        return reverse_lazy(
            'product_detail',
            kwargs={'pk': self.object.pk}
        )


@method_decorator(login_required(login_url='login'), name='dispatch')
class ProductDeleteView(DeleteView):
    model = Product
    form_model = ProductModelForm
    template_name = 'product_delete.html'
    success_url = 'products_list'

    def get_success_url(self):
        return reverse_lazy('products_list')


@method_decorator(login_required(login_url='login'), name='dispatch')
class ProductLogListView(DetailView):
    model = Product
    template_name = 'product_log.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object
        audit_logs = product.history.all()
        parsed_logs = []
        for log in audit_logs:
            changes_dict = json.loads(log.changes)
            parsed_logs.append({'timestamp': log.timestamp, 'changes': changes_dict})

        context['product'] = self.object
        context['audit_logs'] = parsed_logs  # history é o campo do model Product e audit_logs é o que passa para o template
        context['username'] = self.request.user.username
        return context


@method_decorator(login_required(login_url='login'), name='dispatch')
class KitListView(ListView):
    model = Kit
    template_name = 'kit_list.html'
    context_object_name = 'kits'

    def get_queryset(self):
        queryset = super().get_queryset().order_by('label')
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(model__icontains=search)
        return queryset


@method_decorator(login_required(login_url='login'), name='dispatch')
class KitDetailView(DetailView):
    model = Kit
    template_name = 'kit_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['content'] = self.object.content.all()

        return context


def create_kit(request):
    allproducts = Product.objects.all()
    if request.method == 'POST':
        form = ProductSelectionForm(request.POST or None)
        if form.is_valid():
            selected_products = []
            all_products = Product.objects.all()

            for product in all_products:
                field_name = f'product_{product.id}'
                if form.cleaned_data.get(field_name):
                    selected_products.append(product)
            price = 27.99
            cost = sum(product.price for product in selected_products) + 1.50 + (price * 6 / 100)
            profit = round(price - cost, 2)
            label = form.cleaned_data.get('label', '')

            kit = Kit.objects.create(
                cost=cost,
                price=27.99,
                profit=profit,
                label=label
            )
            kit.content.set(selected_products)

            return redirect('kit_list')
    else:
        form = ProductSelectionForm()

    context = {
        'form': form,
        'allproducts': allproducts,
    }
    return render(request, 'new_kit.html', context)


class KitDeleteView(DeleteView):
    model = Kit
    form_model = KitModelForm
    template_name = 'kit_delete.html'
    success_url = 'kit_list'

    def get_success_url(self):
        return reverse_lazy('kit_list')


def create_identical_kit(request, pk):
    original_kit = get_object_or_404(Kit, pk=pk)
    new_kit = Kit.objects.create(
        cost=original_kit.cost,
        price=original_kit.price,
        profit=original_kit.profit,
        label=original_kit.label
    )
    new_kit.content.set(original_kit.content.all())

    return HttpResponseRedirect(reverse('kit_list'))

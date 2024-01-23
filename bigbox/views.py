from typing import Any
from django.shortcuts import render, redirect 
from bigbox.models import Category, Product, Kit
from django.views import View
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from bigbox.forms import ProductModelForm, KitModelForm, ProductSelectionForm
from bigbox import models
import json
from datetime import datetime
from random import randint

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
        from django.http import HttpRequest
        context = super().get_context_data(**kwargs)
        product = self.object
        audit_logs = product.history.all()
        parsed_logs = []
        for log in audit_logs:
            changes_dict = json.loads(log.changes)
            parsed_logs.append({'timestamp': log.timestamp, 'changes': changes_dict})
        
        
        context['product'] = self.object
        context['audit_logs'] = parsed_logs #history é o campo do model Product e audit_logs é o que passa para o template  
        context['username'] = self.request.user.username
        return context
    
@method_decorator(login_required(login_url='login'), name='dispatch')
class KitListView(ListView):
    model = Kit
    template_name = 'kit_list.html'
    context_object_name = 'kits'

@method_decorator(login_required(login_url='login'), name='dispatch')
class KitDetailView(DetailView):
    model = Kit
    template_name = 'kit_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['content'] = self.object.content.all()   
        
        return context


def create_kit(request):
    total_cost = 0
    if request.method == 'POST':
        form = ProductSelectionForm(request.POST)
        if form.is_valid():
            selected_products = form.cleaned_data['products']
            cost = sum(product.price for product in selected_products) + 1.50
            label = '-'.join(str(product.id).zfill(3) for product in selected_products)
            price = 27.99
            profit = round(price-cost, 2)
            ano = datetime.now().year
            end = randint(100, 1000)

            kit = Kit.objects.create(
                cost=cost,
                price=27.99,
                profit=profit,
                label='789'+ str(ano) + '3128' + '-' + str(end)
            )
            kit.content.set(selected_products)
            
            for product in selected_products:
                total_cost += product.price
            context = {
                'form': form,
                'kit_price': total_cost,
            }
            return redirect('kit_list')
    else:
        form = ProductSelectionForm()    
    context = {
                'form': form,
                'kit_price': total_cost,
            }    
    return render(request, 'new_kit.html', context)



class KitDeleteView(DeleteView):
    model = Kit
    form_model = KitModelForm
    template_name = 'kit_delete.html'
    success_url = 'kit_list'

    def get_success_url(self):
        return reverse_lazy('kit_list')


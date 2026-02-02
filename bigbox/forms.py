from django import forms
from bigbox.models import Category, Product, Kit


class CategoryModelForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        labels = {
            'name': 'Nome',
        }


class ProductModelForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'price': forms.NumberInput(attrs={'step': '0.01'}),
        }
        labels = {
            'name': 'Nome',
            'description': 'Descrição',
            'price': 'Preço',
            'category': 'Categoria',
            'amount': 'Quantidade',
            'premium': 'Premium',
            'ncm': 'NCM',
        }

    def clean_price(self):
        price = self.cleaned_data['price']
        # Garanta que o preço tenha no máximo duas casas decimais
        if len(str(price).split('.')[-1]) > 2:
            raise forms.ValidationError("O preço deve ter no máximo duas casas decimais.")
        return price


class KitModelForm(forms.ModelForm):
    class Meta:
        model = Kit
        fields = '__all__'


class ProductSelectionForm(forms.ModelForm):
    class Meta:
        model = Kit
        fields = ['label']
        labels = {
            'label': 'Etiqueta',
            'content': 'Conteúdo',
            'cost': 'Custo',
            'price': 'Preço',
            'profit': 'Lucro',
        }

    # product_filter = forms.CharField(
    #     label='Filtrar produtos',
    #     required=False,
    #     widget=forms.TextInput(attrs={'class': 'product-filter'}),
    # )

    def __init__(self, *args, **kwargs):
        super(ProductSelectionForm, self).__init__(*args, **kwargs)
        all_products = Product.objects.all()

        for product in all_products:
            self.fields[f'product_{product.id}'] = forms.BooleanField(
                label=product.name,
                required=False,
                widget=forms.CheckboxInput(attrs={'data-price': product.price, 'class': 'product-checkbox'}),
            )

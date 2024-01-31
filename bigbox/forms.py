from django import forms 
from bigbox.models import Category, Product, Kit, Category

class CategoryModelForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

class ProductModelForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'price': forms.NumberInput(attrs={'step': '0.01'}),
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
            
class ProductSelectionForm(forms.Form):
    products = forms.ModelMultipleChoiceField(
        queryset=Product.objects.all(),
        to_field_name="name",
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'product-checkbox'}),
        required=True
    )
    label = forms.CharField(max_length=50, required=False, label="Etiqueta")

    def __init__(self, *args, **kwargs):
        super(ProductSelectionForm, self).__init__(*args, **kwargs)
        for product in self.fields['products'].queryset:
            self.fields[f'product_{product.id}'] = forms.BooleanField(
                label=product.name,
                required=False,
                widget=forms.CheckboxInput(attrs={'data-price': product.price}),
            )
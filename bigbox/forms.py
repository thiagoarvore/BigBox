from django import forms 
from bigbox.models import Category, Product, Kit

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
    products = forms.ModelMultipleChoiceField(
        queryset=Product.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'product-checkbox'}),
        required=True
    )
        
    
class ProductSelectionForm(forms.Form):
    products = forms.ModelMultipleChoiceField(
        queryset=Product.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'product-checkbox'}),
        required=True
    )
    label = forms.CharField(max_length=50, required=False)
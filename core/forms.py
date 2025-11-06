# core/forms.py

from django import forms
from .models import Transacao, Conta, Categoria

# ----------------------------------------------------------------------
# 1. Formulário de Transação (Criação/Edição)
# ----------------------------------------------------------------------

class TransacaoForm(forms.ModelForm):
    """
    Formulário para criar e atualizar instâncias do modelo Transacao.
    """
    
    # Campo 'data' ajustado para usar um widget de data amigável
    data = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label='Data da Transação'
    )
    
    class Meta:
        model = Transacao
        # Campos que o usuário irá preencher
        fields = [
            'tipo', 
            'conta', 
            'categoria', 
            'descricao', 
            'valor', 
            'data', 
            'efetivada'
        ]
        
        # Adiciona classes CSS para estilização (Bootstrap)
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'conta': forms.Select(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'descricao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Salário, Aluguel, Compra no Supermercado'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'efetivada': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    # Sobrescreve o inicializador para filtrar as Contas e Categorias do usuário
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        
        if self.request and self.request.user.is_authenticated:
            # Filtra o queryset para mostrar apenas as Contas e Categorias do usuário logado
            self.fields['conta'].queryset = Conta.objects.filter(user=self.request.user)
            self.fields['categoria'].queryset = Categoria.objects.filter(user=self.request.user)

# ----------------------------------------------------------------------
# 2. Formulário de Conta (Criação/Edição)
# ----------------------------------------------------------------------

class ContaForm(forms.ModelForm):
    """
    Formulário para criar e atualizar instâncias do modelo Conta.
    """
    class Meta:
        model = Conta
        fields = ['nome', 'tipo', 'saldo_inicial']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Nubank, Carteira Pessoal'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'saldo_inicial': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }
        labels = {
            'nome': 'Nome da Conta',
            'tipo': 'Tipo',
            'saldo_inicial': 'Saldo Inicial (R$)',
        }

# ----------------------------------------------------------------------
# 3. Formulário de Categoria (Criação/Edição)
# ----------------------------------------------------------------------

class CategoriaForm(forms.ModelForm):
    """
    Formulário para criar e atualizar instâncias do modelo Categoria.
    """
    class Meta:
        model = Categoria
        fields = ['nome']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Alimentação, Salário, Lazer'}),
        }
        labels = {
            'nome': 'Nome da Categoria',
        }
# core/urls.py

from django.urls import path
from .views import (
    TransacaoListView, TransacaoCreateView, TransacaoUpdateView, TransacaoDeleteView,
    ContaListView, ContaCreateView, ContaUpdateView, ContaDeleteView,
    CategoriaListView, CategoriaCreateView, CategoriaUpdateView, CategoriaDeleteView,
)

urlpatterns = [
    # --- ROTAS DE TRANSAÇÕES (Extrato) ---
    path('transacoes/', TransacaoListView.as_view(), name='extrato_transacoes'),
    path('transacoes/nova/', TransacaoCreateView.as_view(), name='adicionar_transacao'),
    path('transacoes/editar/<int:pk>/', TransacaoUpdateView.as_view(), name='editar_transacao'),
    path('transacoes/excluir/<int:pk>/', TransacaoDeleteView.as_view(), name='excluir_transacao'),
    
    # --- ROTAS DE CONTAS ---
    path('contas/', ContaListView.as_view(), name='lista_contas'),
    path('contas/nova/', ContaCreateView.as_view(), name='adicionar_conta'),
    path('contas/editar/<int:pk>/', ContaUpdateView.as_view(), name='editar_conta'),
    path('contas/excluir/<int:pk>/', ContaDeleteView.as_view(), name='excluir_conta'),
    
    # --- ROTAS DE CATEGORIAS ---
    path('categorias/', CategoriaListView.as_view(), name='lista_categorias'),
    path('categorias/nova/', CategoriaCreateView.as_view(), name='adicionar_categoria'),
    path('categorias/editar/<int:pk>/', CategoriaUpdateView.as_view(), name='editar_categoria'),
    path('categorias/excluir/<int:pk>/', CategoriaDeleteView.as_view(), name='excluir_categoria'),
]
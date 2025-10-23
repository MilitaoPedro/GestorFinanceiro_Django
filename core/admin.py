from django.contrib import admin
from .models import Conta, Categoria, Transacao

@admin.register(Conta)
class ContaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo', 'saldo_inicial', 'user')
    list_filter = ('tipo', 'user')
    search_fields = ('nome',)

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'user')
    list_filter = ('user',)
    search_fields = ('nome',)

@admin.register(Transacao)
class TransacaoAdmin(admin.ModelAdmin):
    list_display = ('descricao', 'data', 'tipo', 'valor', 'conta', 'categoria', 'efetivada')
    list_filter = ('tipo', 'data', 'efetivada', 'conta', 'categoria')
    search_fields = ('descricao',)
    date_hierarchy = 'data'
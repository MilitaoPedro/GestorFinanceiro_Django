import datetime
import json
from decimal import Decimal 
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Sum, F, ExpressionWrapper, Case, When, DecimalField as ModelDecimalField
from django.db.models.functions import TruncMonth 
from django.contrib.auth.mixins import LoginRequiredMixin 

from .models import Transacao, Conta, Categoria
from .forms import TransacaoForm, ContaForm, CategoriaForm


# ----------------------------------------------------------------------
# 1. VISÃO GERAL / DASHBOARD
# ----------------------------------------------------------------------

class DashboardView(LoginRequiredMixin, TemplateView):
    """
    Exibe o Painel de Controle (Dashboard) com balanço, resumo e gráficos.
    """
    template_name = 'core/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        hoje = datetime.date.today()
        
        # BASE QUERY
        base_query = Transacao.objects.filter(user=user, efetivada=True)

        # ----------------------------------------------------------------------
        # DADOS DOS CARDS DE RESUMO
        # ----------------------------------------------------------------------
        
        receitas_total = base_query.filter(tipo=Transacao.TipoTransacao.RECEITA).aggregate(Sum('valor'))['valor__sum'] or 0
        despesas_total = base_query.filter(tipo=Transacao.TipoTransacao.DESPESA).aggregate(Sum('valor'))['valor__sum'] or 0
        saldo_total = receitas_total - despesas_total
        context['saldo_total'] = saldo_total
        
        transacoes_mes = base_query.filter(
            data__year=hoje.year, data__month=hoje.month
        )
        context['receita_mes'] = transacoes_mes.filter(tipo=Transacao.TipoTransacao.RECEITA).aggregate(Sum('valor'))['valor__sum'] or 0
        context['despesa_mes'] = transacoes_mes.filter(tipo=Transacao.TipoTransacao.DESPESA).aggregate(Sum('valor'))['valor__sum'] or 0
        context['saldo_mes'] = context['receita_mes'] - context['despesa_mes']

        # ----------------------------------------------------------------------
        # 5. TRANSAÇÕES RECENTES (LISTA)
        # ----------------------------------------------------------------------
        
        extrato_recente_real = base_query.select_related('conta', 'categoria').order_by('-data')[:10]
        context['extrato_recente'] = extrato_recente_real 

        # ----------------------------------------------------------------------
        # 6. SALDO POR CONTA
        # ----------------------------------------------------------------------
        
        contas = Conta.objects.filter(user=user).order_by('nome')
        for conta in contas:
            conta.saldo_atual = conta.saldo_inicial
        
        context['contas'] = contas
        
        # ----------------------------------------------------------------------
        # 7. DADOS PARA GRÁFICOS
        # ----------------------------------------------------------------------

        todas_transacoes_grafico = base_query
        
        # GRÁFICO 1: Despesas por Categoria
        despesas_por_categoria = todas_transacoes_grafico.filter(
            tipo=Transacao.TipoTransacao.DESPESA
        ).values('categoria__nome').annotate(
            total=Sum('valor')
        ).order_by('-total')
        
        chart_despesas_labels = [item['categoria__nome'] or 'Sem Categoria' for item in despesas_por_categoria]
        chart_despesas_data = [float(item['total']) for item in despesas_por_categoria]

        context['chart_despesas_labels'] = json.dumps(chart_despesas_labels)
        context['chart_despesas_data'] = json.dumps(chart_despesas_data)

        # GRÁFICO 2: Balanço Mensal
        transacoes_com_sinal = todas_transacoes_grafico.annotate(
            sinal=ExpressionWrapper(
                F('valor') * Case(
                    When(tipo=Transacao.TipoTransacao.RECEITA, then=1),
                    When(tipo=Transacao.TipoTransacao.DESPESA, then=-1),
                    default=0,
                    output_field=ModelDecimalField()
                ),
                output_field=ModelDecimalField()
            )
        )

        balanco_mensal = transacoes_com_sinal.annotate(
            mes=TruncMonth('data')
        ).values('mes').annotate(
            balanco_do_mes=Sum('sinal')
        ).order_by('mes')
        
        chart_balanco_labels = [item['mes'].strftime("%b/%y") for item in balanco_mensal]
        chart_balanco_data = [float(item['balanco_do_mes']) for item in balanco_mensal]

        context['chart_balanco_labels'] = json.dumps(chart_balanco_labels)
        context['chart_balanco_data'] = json.dumps(chart_balanco_data)
        
        return context


# ----------------------------------------------------------------------
# 2. CRUD DE TRANSAÇÕES (Extrato Financeiro)
# ----------------------------------------------------------------------

class TransacaoListView(LoginRequiredMixin, ListView):
    """Lista todas as transações do usuário (Extrato)."""
    model = Transacao
    template_name = 'core/transacao_list.html'
    context_object_name = 'transacoes'
    paginate_by = 25 
    
    def get_queryset(self):
        return Transacao.objects.filter(
            user=self.request.user
        ).select_related('conta', 'categoria').order_by('-data')

class TransacaoCreateView(LoginRequiredMixin, CreateView):
    """View para adicionar uma nova transação (Receita ou Despesa)."""
    model = Transacao
    form_class = TransacaoForm
    template_name = 'core/transacao_form.html'
    success_url = reverse_lazy('extrato_transacoes')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request 
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class TransacaoUpdateView(LoginRequiredMixin, UpdateView):
    """View para editar uma transação existente."""
    model = Transacao
    form_class = TransacaoForm
    template_name = 'core/transacao_form.html'
    success_url = reverse_lazy('extrato_transacoes')
    
    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request 
        return kwargs

class TransacaoDeleteView(LoginRequiredMixin, DeleteView):
    """View para excluir uma transação."""
    model = Transacao
    template_name = 'core/transacao_confirm_delete.html'
    success_url = reverse_lazy('extrato_transacoes')

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


# ----------------------------------------------------------------------
# 3. CRUD DE CONTAS (Carteira, Banco, etc.)
# ----------------------------------------------------------------------

class ContaListView(LoginRequiredMixin, ListView):
    """Lista todas as Contas do usuário."""
    model = Conta
    template_name = 'core/conta_list.html'
    context_object_name = 'contas'
    
    def get_queryset(self):
        return Conta.objects.filter(user=self.request.user).order_by('nome')

class ContaCreateView(LoginRequiredMixin, CreateView):
    """Cria uma nova Conta."""
    model = Conta
    form_class = ContaForm
    template_name = 'core/conta_form.html'
    success_url = reverse_lazy('lista_contas')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ContaUpdateView(LoginRequiredMixin, UpdateView):
    """Edita uma Conta existente."""
    model = Conta
    form_class = ContaForm
    template_name = 'core/conta_form.html'
    success_url = reverse_lazy('lista_contas')
    
    def get_queryset(self):
        return Conta.objects.filter(user=self.request.user)

class ContaDeleteView(LoginRequiredMixin, DeleteView):
    """Exclui uma Conta."""
    model = Conta
    template_name = 'core/conta_confirm_delete.html'
    success_url = reverse_lazy('lista_contas')

    def get_queryset(self):
        return Conta.objects.filter(user=self.request.user)


# ----------------------------------------------------------------------
# 4. CRUD DE CATEGORIAS (Alimentação, Salário, etc.)
# ----------------------------------------------------------------------

class CategoriaListView(LoginRequiredMixin, ListView):
    """Lista todas as Categorias do usuário."""
    model = Categoria
    template_name = 'core/categoria_list.html'
    context_object_name = 'categorias'
    
    def get_queryset(self):
        return Categoria.objects.filter(user=self.request.user).order_by('nome')

class CategoriaCreateView(LoginRequiredMixin, CreateView):
    """Cria uma nova Categoria."""
    model = Categoria
    form_class = CategoriaForm
    template_name = 'core/categoria_form.html'
    success_url = reverse_lazy('lista_categorias')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class CategoriaUpdateView(LoginRequiredMixin, UpdateView):
    """Edita uma Categoria existente."""
    model = Categoria
    form_class = CategoriaForm
    template_name = 'core/categoria_form.html'
    success_url = reverse_lazy('lista_categorias')
    
    def get_queryset(self):
        return Categoria.objects.filter(user=self.request.user)

class CategoriaDeleteView(LoginRequiredMixin, DeleteView):
    """Exclui uma Categoria."""
    model = Categoria
    template_name = 'core/categoria_confirm_delete.html'
    success_url = reverse_lazy('lista_categorias')
    
    def get_queryset(self):
        return Categoria.objects.filter(user=self.request.user)
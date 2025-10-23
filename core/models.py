# core/models.py

from django.db import models
from django.conf import settings  # <-- GARANTA QUE ESTA LINHA EXISTA
from django.utils import timezone

# Não precisamos mais da linha 'User = settings.AUTH_USER_MODEL' aqui em cima.
# Vamos usar o settings.AUTH_USER_MODEL diretamente nos campos.

class Conta(models.Model):
    """
    Representa uma conta do usuário (ex: Carteira, Banco, Cartão de Crédito).
    """
    class TipoConta(models.TextChoices):
        CARTEIRA = 'CARTEIRA', 'Carteira'
        CONTA_CORRENTE = 'CC', 'Conta Corrente'
        POUPANCA = 'POUPANCA', 'Poupança'
        CARTAO_CREDITO = 'CREDITO', 'Cartão de Crédito'
        INVESTIMENTO = 'INVEST', 'Investimento'
        OUTRO = 'OUTRO', 'Outro'

    # Relacionamento: Cada conta pertence a UM usuário.
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # <-- CORREÇÃO AQUI
        on_delete=models.CASCADE,
        related_name='contas',
        verbose_name='Usuário'
    )
    
    nome = models.CharField('Nome da Conta', max_length=100)
    
    tipo = models.CharField(
        'Tipo de Conta',
        max_length=10,
        choices=TipoConta.choices,
        default=TipoConta.CONTA_CORRENTE
    )
    
    saldo_inicial = models.DecimalField(
        'Saldo Inicial',
        max_digits=15,
        decimal_places=2,
        default=0.00
    )
    
    data_criacao = models.DateTimeField('Data de Criação', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Conta'
        verbose_name_plural = 'Contas'
        unique_together = ('user', 'nome')
        ordering = ['nome']

    def __str__(self):
        return f'{self.nome} ({self.get_tipo_display()})'


class Categoria(models.Model):
    """
    Categorias para classificar despesas e receitas (Ex: Alimentação, Salário).
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # <-- CORREÇÃO AQUI
        on_delete=models.CASCADE,
        related_name='categorias',
        verbose_name='Usuário'
    )
    
    nome = models.CharField('Nome da Categoria', max_length=100)
    
    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        unique_together = ('user', 'nome')
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Transacao(models.Model):
    """
    O registro principal: uma Despesa ou uma Receita.
    """
    class TipoTransacao(models.TextChoices):
        RECEITA = 'RECEITA', 'Receita'
        DESPESA = 'DESPESA', 'Despesa'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # <-- CORREÇÃO AQUI
        on_delete=models.CASCADE,
        related_name='transacoes',
        verbose_name='Usuário'
    )
    
    conta = models.ForeignKey(
        Conta,
        on_delete=models.CASCADE, 
        related_name='transacoes',
        verbose_name='Conta'
    )
    
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL, 
        null=True,
        blank=True, 
        related_name='transacoes',
        verbose_name='Categoria'
    )

    descricao = models.CharField('Descrição', max_length=255)
    
    valor = models.DecimalField(
        'Valor',
        max_digits=15,
        decimal_places=2,
        help_text='Insira um valor positivo. O tipo define se é entrada ou saída.'
    )
    
    tipo = models.CharField(
        'Tipo de Transação',
        max_length=7,
        choices=TipoTransacao.choices,
        default=TipoTransacao.DESPESA
    )
    
    data = models.DateField(
        'Data da Transação',
        default=timezone.now
    )
    
    efetivada = models.BooleanField(
        'Efetivada?',
        default=True,
        help_text='Marque se a transação já foi paga/recebida.'
    )

    data_criacao = models.DateTimeField('Data de Criação', auto_now_add=True)
    data_atualizacao = models.DateTimeField('Última Atualização', auto_now=True)
    
    class Meta:
        verbose_name = 'Transação'
        verbose_name_plural = 'Transações'
        ordering = ['-data', '-data_criacao']

    def __str__(self):
        sinal = '-' if self.tipo == self.TipoTransacao.DESPESA else '+'
        return f'{self.data} | {self.descricao} ({sinal}R$ {self.valor})'
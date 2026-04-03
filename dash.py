"""
Dashboard Interativo - VarejoMax
Análise de Vendas, Vendedores, Clientes e Produtos
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# ─────────────────────────────────────────────
# CONFIG DA PÁGINA
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="VarejoMax | Dashboard",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# CSS CUSTOMIZADO
# ─────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Sans:wght@300;400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(160deg, #0f172a 0%, #1e293b 100%);
        border-right: 1px solid #334155;
    }
    [data-testid="stSidebar"] * {
        color: #e2e8f0 !important;
    }
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stMultiselect label {
        color: #94a3b8 !important;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }

    /* Fundo principal */
    .main {
        background-color: #f8fafc;
    }

    /* Cabeçalho */
    .page-header {
        background: linear-gradient(135deg, #0f172a 0%, #1e40af 60%, #2563eb 100%);
        border-radius: 16px;
        padding: 2rem 2.5rem;
        margin-bottom: 1.5rem;
        color: white;
        position: relative;
        overflow: hidden;
    }
    .page-header::before {
        content: '';
        position: absolute;
        top: -40px; right: -40px;
        width: 220px; height: 220px;
        border-radius: 50%;
        background: rgba(255,255,255,0.05);
    }
    .page-header h1 {
        font-family: 'Syne', sans-serif;
        font-size: 2rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.02em;
    }
    .page-header p {
        margin: 0.25rem 0 0;
        color: #93c5fd;
        font-size: 0.9rem;
    }

    /* KPI Cards */
    .kpi-card {
        background: white;
        border-radius: 12px;
        padding: 1.25rem 1.5rem;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
        margin-bottom: 0.5rem;
    }
    .kpi-label {
        font-size: 0.72rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #64748b;
        margin-bottom: 0.4rem;
    }
    .kpi-value {
        font-family: 'Syne', sans-serif;
        font-size: 1.75rem;
        font-weight: 700;
        color: #0f172a;
        line-height: 1;
    }
    .kpi-sub {
        font-size: 0.78rem;
        color: #10b981;
        margin-top: 0.3rem;
        font-weight: 500;
    }

    /* Section titles */
    .section-title {
        font-family: 'Syne', sans-serif;
        font-size: 1.1rem;
        font-weight: 700;
        color: #0f172a;
        margin: 1.5rem 0 0.75rem;
        padding-bottom: 0.4rem;
        border-bottom: 2px solid #e2e8f0;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: #f1f5f9;
        border-radius: 10px;
        padding: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        font-size: 0.85rem;
        font-weight: 500;
        color: #475569;
        padding: 6px 18px;
    }
    .stTabs [aria-selected="true"] {
        background: white !important;
        color: #1e40af !important;
        box-shadow: 0 1px 4px rgba(0,0,0,0.1);
    }

    /* Métricas nativas do streamlit */
    [data-testid="metric-container"] {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1rem 1.25rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }

    /* Esconde rodapé padrão */
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# CARREGAMENTO DOS DADOS
# ─────────────────────────────────────────────
@st.cache_data
def carregar_dados():
    df_clientes  = pd.read_csv('clientes_varejomax_grande.csv')
    df_vendas    = pd.read_csv('vendas_varejomax_grande.csv')
    df_vendedores = pd.read_csv('vendedores_varejomax_grande.csv')
    df_empregados = pd.read_csv('empregados_varejomax_grande.csv')

    df_vendas['data'] = pd.to_datetime(df_vendas['data'])
    df_empregados['data_admissao'] = pd.to_datetime(df_empregados['data_admissao'])

    df_vendas = df_vendas.merge(df_clientes, on='id_cliente')
    df_vendas = df_vendas.merge(df_vendedores, on='id_vendedor')
    df_vendas = df_vendas.rename(columns={
        "nome_x": "nome_cliente",
        "nome_y": "nome_vendedor",
        "regiao_x": "regiao_cliente",
        "regiao_y": "regiao_vendedor",
    })

    df_vendas['mes']      = df_vendas['data'].dt.to_period('M')
    df_vendas['mes_str']  = df_vendas['data'].dt.strftime('%m/%Y')
    df_vendas['ano']      = df_vendas['data'].dt.year
    df_vendas['mes_num']  = df_vendas['data'].dt.month

    return df_vendas, df_empregados

try:
    df_vendas, df_empregados = carregar_dados()
    dados_ok = True
except FileNotFoundError as e:
    dados_ok = False
    arquivo_faltando = str(e)


# ─────────────────────────────────────────────
# SIDEBAR — FILTROS
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🛒 VarejoMax")
    st.markdown("---")

    if dados_ok:
        st.markdown("**Filtros**")

        anos_disponiveis = sorted(df_vendas['ano'].unique())
        ano_selecionado = st.multiselect(
            "Ano",
            options=anos_disponiveis,
            default=anos_disponiveis,
        )

        regioes_disponiveis = sorted(df_vendas['regiao_vendedor'].unique())
        regiao_selecionada = st.multiselect(
            "Região",
            options=regioes_disponiveis,
            default=regioes_disponiveis,
        )

        produtos_disponiveis = sorted(df_vendas['produto'].unique())
        produto_selecionado = st.multiselect(
            "Produto",
            options=produtos_disponiveis,
            default=produtos_disponiveis,
        )

        top_n = st.slider("Top N (rankings)", min_value=3, max_value=15, value=5)

        st.markdown("---")
        st.markdown(
            "<span style='font-size:0.75rem;color:#475569'>Case fictício — VarejoMax S.A.</span>",
            unsafe_allow_html=True,
        )


# ─────────────────────────────────────────────
# VERIFICAÇÃO DE ARQUIVOS
# ─────────────────────────────────────────────
if not dados_ok:
    st.error(f"❌ Arquivo não encontrado: `{arquivo_faltando}`")
    st.info("Certifique-se de que os CSVs estão na mesma pasta que este script.")
    st.stop()


# ─────────────────────────────────────────────
# APLICAR FILTROS
# ─────────────────────────────────────────────
df = df_vendas.copy()
if ano_selecionado:
    df = df[df['ano'].isin(ano_selecionado)]
if regiao_selecionada:
    df = df[df['regiao_vendedor'].isin(regiao_selecionada)]
if produto_selecionado:
    df = df[df['produto'].isin(produto_selecionado)]


# ─────────────────────────────────────────────
# CABEÇALHO
# ─────────────────────────────────────────────
st.markdown("""
<div class="page-header">
    <h1>🛒 VarejoMax — Dashboard de Vendas</h1>
    <p>Análise interativa de faturamento, vendedores, clientes e produtos</p>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# KPIs PRINCIPAIS
# ─────────────────────────────────────────────
faturamento_total  = df['valor'].sum()
total_vendas       = df['id_venda'].nunique()
ticket_medio       = faturamento_total / total_vendas if total_vendas else 0
total_clientes     = df['id_cliente'].nunique()
total_vendedores   = df['id_vendedor'].nunique()

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("💰 Faturamento Total", f"R$ {faturamento_total:,.0f}".replace(",", "."))
with col2:
    st.metric("🧾 Total de Vendas", f"{total_vendas:,}".replace(",", "."))
with col3:
    st.metric("🎯 Ticket Médio", f"R$ {ticket_medio:,.2f}".replace(",", "."))
with col4:
    st.metric("👥 Clientes Ativos", total_clientes)
with col5:
    st.metric("🏆 Vendedores", total_vendedores)


# ─────────────────────────────────────────────
# TABS PRINCIPAIS
# ─────────────────────────────────────────────
tab_tempo, tab_vendedores, tab_clientes, tab_produtos, tab_regioes = st.tabs([
    "📅 Evolução Temporal",
    "🏆 Vendedores",
    "👥 Clientes",
    "📦 Produtos",
    "🗺️ Regiões",
])


# ── CORES PADRÃO ──────────────────────────────
COR_PRIMARIA  = "#1e40af"
COR_ACENTO    = "#3b82f6"
PALETA        = px.colors.sequential.Blues_r
PALETA_BAR    = [COR_ACENTO] * 20


def layout_padrao(fig, altura=420):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans, sans-serif", color="#334155"),
        height=altura,
        margin=dict(l=10, r=10, t=40, b=10),
        title_font=dict(family="Syne, sans-serif", size=15, color="#0f172a"),
        xaxis=dict(gridcolor="#f1f5f9", linecolor="#e2e8f0"),
        yaxis=dict(gridcolor="#f1f5f9", linecolor="#e2e8f0"),
    )
    return fig


# ═══════════════════════════════════════════════
# TAB 1 — EVOLUÇÃO TEMPORAL
# ═══════════════════════════════════════════════
with tab_tempo:
    vendas_mes = (
        df.groupby(df['data'].dt.to_period('M'))['valor']
        .sum()
        .reset_index()
    )
    vendas_mes['mes'] = vendas_mes['data'].astype(str)
    vendas_mes = vendas_mes.sort_values('mes')

    col_a, col_b = st.columns([2, 1])

    with col_a:
        fig = px.bar(
            vendas_mes, x='mes', y='valor',
            title='Faturamento por Mês',
            labels={"mes": "Mês", "valor": "Faturamento (R$)"},
            color_discrete_sequence=[COR_ACENTO],
        )
        fig.update_traces(marker_line_width=0)
        fig = layout_padrao(fig)
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        # Evolução acumulada
        vendas_mes['acumulado'] = vendas_mes['valor'].cumsum()
        fig2 = px.area(
            vendas_mes, x='mes', y='acumulado',
            title='Faturamento Acumulado',
            labels={"mes": "", "acumulado": "R$"},
            color_discrete_sequence=[COR_PRIMARIA],
        )
        fig2 = layout_padrao(fig2)
        st.plotly_chart(fig2, use_container_width=True)

    # Heatmap: mês x produto
    st.markdown('<div class="section-title">Distribuição por Mês e Produto</div>', unsafe_allow_html=True)
    heat_data = df.pivot_table(
        index='produto',
        columns=df['data'].dt.strftime('%m/%Y'),
        values='valor',
        aggfunc='sum',
        fill_value=0,
    )
    fig3 = px.imshow(
        heat_data,
        color_continuous_scale="Blues",
        title="Faturamento por Produto × Mês",
        labels=dict(color="R$"),
        aspect="auto",
    )
    fig3 = layout_padrao(fig3, altura=380)
    st.plotly_chart(fig3, use_container_width=True)


# ═══════════════════════════════════════════════
# TAB 2 — VENDEDORES
# ═══════════════════════════════════════════════
with tab_vendedores:
    col_a, col_b = st.columns(2)

    with col_a:
        top_vend_valor = (
            df.groupby(['id_vendedor', 'nome_vendedor'])['valor']
            .sum()
            .sort_values(ascending=False)
            .head(top_n)
            .reset_index()
        )
        fig = px.bar(
            top_vend_valor,
            x='valor', y='nome_vendedor',
            orientation='h',
            title=f'Top {top_n} Vendedores por Faturamento',
            labels={"nome_vendedor": "", "valor": "Faturamento (R$)"},
            color='valor',
            color_continuous_scale='Blues',
            text_auto='.3s',
        )
        fig.update_layout(yaxis={'categoryorder': 'total ascending'}, coloraxis_showscale=False)
        fig = layout_padrao(fig)
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        top_vend_qtde = (
            df.groupby(['id_vendedor', 'nome_vendedor'])['id_venda']
            .count()
            .sort_values(ascending=False)
            .head(top_n)
            .reset_index()
            .rename(columns={'id_venda': 'qtde_vendas'})
        )
        fig = px.bar(
            top_vend_qtde,
            x='qtde_vendas', y='nome_vendedor',
            orientation='h',
            title=f'Top {top_n} Vendedores por Quantidade',
            labels={"nome_vendedor": "", "qtde_vendas": "Nº de Vendas"},
            color='qtde_vendas',
            color_continuous_scale='Blues',
            text_auto=True,
        )
        fig.update_layout(yaxis={'categoryorder': 'total ascending'}, coloraxis_showscale=False)
        fig = layout_padrao(fig)
        st.plotly_chart(fig, use_container_width=True)

    # Ticket médio por vendedor
    st.markdown('<div class="section-title">Ticket Médio por Vendedor</div>', unsafe_allow_html=True)
    ticket_vend = (
        df.groupby('nome_vendedor')['valor']
        .agg(['sum', 'count'])
        .assign(ticket_medio=lambda x: x['sum'] / x['count'])
        .sort_values('ticket_medio', ascending=False)
        .head(top_n)
        .reset_index()
    )
    fig4 = px.scatter(
        ticket_vend,
        x='count', y='ticket_medio',
        size='sum', color='ticket_medio',
        hover_name='nome_vendedor',
        title="Qtde de Vendas × Ticket Médio (tamanho = faturamento total)",
        labels={"count": "Nº de Vendas", "ticket_medio": "Ticket Médio (R$)"},
        color_continuous_scale='Blues',
    )
    fig4 = layout_padrao(fig4)
    st.plotly_chart(fig4, use_container_width=True)


# ═══════════════════════════════════════════════
# TAB 3 — CLIENTES
# ═══════════════════════════════════════════════
with tab_clientes:
    col_a, col_b = st.columns(2)

    with col_a:
        top_cli_valor = (
            df.groupby(['id_cliente', 'nome_cliente'])['valor']
            .sum()
            .sort_values(ascending=False)
            .head(top_n)
            .reset_index()
        )
        fig = px.bar(
            top_cli_valor,
            x='valor', y='nome_cliente',
            orientation='h',
            title=f'Top {top_n} Clientes por Faturamento',
            labels={"nome_cliente": "", "valor": "Total Comprado (R$)"},
            color='valor',
            color_continuous_scale='Blues',
            text_auto='.3s',
        )
        fig.update_layout(yaxis={'categoryorder': 'total ascending'}, coloraxis_showscale=False)
        fig = layout_padrao(fig)
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        top_cli_qtde = (
            df.groupby(['id_cliente', 'nome_cliente'])['id_venda']
            .count()
            .sort_values(ascending=False)
            .head(top_n)
            .reset_index()
            .rename(columns={'id_venda': 'qtde_compras'})
        )
        fig = px.bar(
            top_cli_qtde,
            x='qtde_compras', y='nome_cliente',
            orientation='h',
            title=f'Top {top_n} Clientes por Frequência',
            labels={"nome_cliente": "", "qtde_compras": "Nº de Compras"},
            color='qtde_compras',
            color_continuous_scale='Blues',
            text_auto=True,
        )
        fig.update_layout(yaxis={'categoryorder': 'total ascending'}, coloraxis_showscale=False)
        fig = layout_padrao(fig)
        st.plotly_chart(fig, use_container_width=True)

    # Distribuição de valor por cliente (histograma)
    st.markdown('<div class="section-title">Distribuição do Valor de Compra</div>', unsafe_allow_html=True)
    valor_por_cliente = df.groupby('id_cliente')['valor'].sum().reset_index()
    fig5 = px.histogram(
        valor_por_cliente, x='valor',
        nbins=40,
        title='Distribuição do Faturamento por Cliente',
        labels={"valor": "Faturamento Total (R$)", "count": "Nº de Clientes"},
        color_discrete_sequence=[COR_ACENTO],
    )
    fig5.update_traces(marker_line_width=0.5, marker_line_color="white")
    fig5 = layout_padrao(fig5)
    st.plotly_chart(fig5, use_container_width=True)


# ═══════════════════════════════════════════════
# TAB 4 — PRODUTOS
# ═══════════════════════════════════════════════
with tab_produtos:
    col_a, col_b = st.columns(2)

    with col_a:
        prod_valor = (
            df.groupby('produto')['valor']
            .sum()
            .sort_values(ascending=False)
            .head(top_n)
            .reset_index()
        )
        fig = px.bar(
            prod_valor,
            x='valor', y='produto',
            orientation='h',
            title=f'Top {top_n} Produtos por Faturamento',
            labels={"produto": "", "valor": "Faturamento (R$)"},
            color='valor',
            color_continuous_scale='Blues',
            text_auto='.3s',
        )
        fig.update_layout(yaxis={'categoryorder': 'total ascending'}, coloraxis_showscale=False)
        fig = layout_padrao(fig)
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        prod_qtde = (
            df.groupby('produto')['id_venda']
            .count()
            .sort_values(ascending=False)
            .head(top_n)
            .reset_index()
            .rename(columns={'id_venda': 'qtde_vendas'})
        )
        fig = px.pie(
            prod_qtde,
            names='produto', values='qtde_vendas',
            title=f'Top {top_n} Produtos — Share de Quantidade',
            color_discrete_sequence=px.colors.sequential.Blues_r,
            hole=0.45,
        )
        fig.update_traces(textinfo='percent+label')
        fig = layout_padrao(fig)
        st.plotly_chart(fig, use_container_width=True)

    # Faturamento por produto ao longo do tempo
    st.markdown('<div class="section-title">Evolução dos Produtos no Tempo</div>', unsafe_allow_html=True)
    top_prods = prod_valor['produto'].tolist()
    df_top_prods = df[df['produto'].isin(top_prods)]
    prod_tempo = (
        df_top_prods.groupby([df_top_prods['data'].dt.to_period('M'), 'produto'])['valor']
        .sum()
        .reset_index()
    )
    prod_tempo['mes'] = prod_tempo['data'].astype(str)
    fig6 = px.line(
        prod_tempo, x='mes', y='valor', color='produto',
        title=f'Faturamento dos Top {top_n} Produtos por Mês',
        labels={"mes": "Mês", "valor": "Faturamento (R$)", "produto": "Produto"},
        markers=True,
    )
    fig6 = layout_padrao(fig6, altura=380)
    st.plotly_chart(fig6, use_container_width=True)


# ═══════════════════════════════════════════════
# TAB 5 — REGIÕES
# ═══════════════════════════════════════════════
with tab_regioes:
    col_a, col_b = st.columns(2)

    with col_a:
        reg_valor = (
            df.groupby('regiao_vendedor')['valor']
            .sum()
            .sort_values(ascending=False)
            .reset_index()
        )
        fig = px.bar(
            reg_valor,
            x='regiao_vendedor', y='valor',
            title='Faturamento por Região',
            labels={"regiao_vendedor": "Região", "valor": "Faturamento (R$)"},
            color='valor',
            color_continuous_scale='Blues',
            text_auto='.3s',
        )
        fig.update_traces(marker_line_width=0)
        fig.update_layout(coloraxis_showscale=False)
        fig = layout_padrao(fig)
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        reg_qtde = (
            df.groupby('regiao_vendedor')['id_venda']
            .count()
            .reset_index()
            .rename(columns={'id_venda': 'qtde_vendas'})
        )
        fig = px.pie(
            reg_qtde,
            names='regiao_vendedor', values='qtde_vendas',
            title='Share de Vendas por Região',
            color_discrete_sequence=px.colors.sequential.Blues_r,
            hole=0.4,
        )
        fig.update_traces(textinfo='percent+label')
        fig = layout_padrao(fig)
        st.plotly_chart(fig, use_container_width=True)

    # Heatmap Região × Produto
    st.markdown('<div class="section-title">Faturamento por Região × Produto</div>', unsafe_allow_html=True)
    heat_reg = df.pivot_table(
        index='regiao_vendedor',
        columns='produto',
        values='valor',
        aggfunc='sum',
        fill_value=0,
    )
    fig7 = px.imshow(
        heat_reg,
        color_continuous_scale='Blues',
        title='Região × Produto — Faturamento (R$)',
        labels=dict(color="R$"),
        aspect="auto",
        text_auto='.3s',
    )
    fig7 = layout_padrao(fig7, altura=380)
    st.plotly_chart(fig7, use_container_width=True)


# ─────────────────────────────────────────────
# RODAPÉ COM TABELA DETALHADA
# ─────────────────────────────────────────────
st.markdown("---")
with st.expander("🔍 Ver dados brutos filtrados"):
    colunas_exibir = ['id_venda', 'data', 'nome_cliente', 'nome_vendedor',
                      'produto', 'valor', 'regiao_vendedor', 'mes_str']
    colunas_exibir = [c for c in colunas_exibir if c in df.columns]
    st.dataframe(
        df[colunas_exibir].sort_values('data', ascending=False),
        use_container_width=True,
        height=300,
    )
    st.caption(f"Exibindo {len(df):,} registros conforme filtros aplicados.")
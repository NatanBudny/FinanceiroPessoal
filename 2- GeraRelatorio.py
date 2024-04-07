import sqlite3
import pandas as pd
import plotly.express as px
import plotly.io as pio
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image, Spacer
import locale
from io import BytesIO

# Definir a localização para o Brasil
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

# Conectar ao banco de dados
conn = sqlite3.connect('fatura_cartao.db')

# Consulta ao banco de dados para obter o último referenceMonth
query_last_month = "SELECT MAX(referenceMonth) FROM faturacartaocredito"
last_month = conn.execute(query_last_month).fetchone()[0]

# Verificar se há algum registro no banco de dados
if last_month:
    # Consulta ao banco de dados a partir do último referenceMonth registrado
    query = f"SELECT * FROM faturacartaocredito WHERE referenceMonth = ? ORDER BY category, date, amount DESC"
    df = pd.read_sql_query(query, conn, params=(last_month,))

    # Agrupar os dados por categoria e somar os valores
    df_grouped = df.groupby('category')['amount'].sum().reset_index()

    # Ordenar os registros de forma descendente
    df_grouped = df_grouped.sort_values(by='amount', ascending=False)

    # Consulta ao banco de dados para obter as metas de gastos
    query_metas = "SELECT category, meta FROM meta_gastos"
    metas_df = pd.read_sql_query(query_metas, conn)

    # Merge entre os DataFrames df_grouped e metas_df para obter as metas de gastos para cada categoria
    df_grouped = df_grouped.merge(metas_df, on='category', how='left')

    # Calcular a diferença entre o valor gasto e a meta para cada categoria
    df_grouped['diferenca'] = df_grouped['meta'] - df_grouped['amount']

    # Fechar a conexão com o banco de dados
    conn.close()

    # Criar gráfico de barras horizontais interativo com o Plotly
    fig = px.bar(df_grouped, x='amount', y='category', title=f'Gastos por Categoria ({last_month})',
                 orientation='h', template='plotly')

    # Adicionando rótulos nas barras
    fig.update_traces(texttemplate='%{x}', textposition='inside')

    # Adicionar texto com a diferença entre a meta e o gasto ao final de cada barra
    for i in range(len(df_grouped)):
        if not pd.isnull(df_grouped['meta'][i]) and df_grouped['diferenca'][i] != 0:  # Verificar se há uma meta cadastrada e a diferença não é zero
            diferenca = df_grouped['diferenca'][i]
            text = ""
            if diferenca < 0:
                text = f"Furo: {locale.currency(abs(diferenca), grouping=True)}"
                color = "red"
            else:
                text = f"Saldo: {locale.currency(diferenca, grouping=True)}"
                color = "green"

            fig.add_annotation(x=df_grouped['amount'][i], y=df_grouped['category'][i],
                               text=text,
                               showarrow=False, xshift=40, font=dict(size=10, color="white"), bgcolor=color)  # Adiciona a cor de fundo ao texto

    # Salvar o gráfico em um buffer de bytes com alta qualidade
    img_buffer = BytesIO()
    pio.write_image(fig, img_buffer, format="png", width=700, height=500, scale=2)

    img_buffer.seek(0)

    # Criar documento PDF
    pdf_filename = f'relatorio_gastos_{last_month}.pdf'
    doc = SimpleDocTemplate(pdf_filename, pagesize=A4)

    elements = []
    # Converter a imagem do gráfico para Image do ReportLab
    chart_image = Image(img_buffer)
    chart_image.drawWidth = 550
    chart_image.drawHeight = 450

    # Adicionar gráfico de barras ao PDF
    elements.append(Spacer(1, 24))
    elements.append(chart_image)

    # Criar e adicionar tabelas para cada categoria
    categories = df['category'].unique()

    for category in categories:
        category_df = df[df['category'] == category]

        # Criar tabela com os detalhes da categoria
        data = [category_df.columns.tolist()] + category_df.values.tolist()
        table = Table(data)

        # Estilo da tabela
        style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), (0.8, 0.8, 0.8)),
                            ('TEXTCOLOR', (0, 0), (-1, 0), (1, 1, 1)),
                            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                            ('BACKGROUND', (0, 1), (-1, -1), (0.9, 0.9, 0.9)),
                            ('GRID', (0, 0), (-1, -1), 1, (0, 0, 0))])

        # Aplicar estilo à tabela
        table.setStyle(style)

        # Adicionar tabela da categoria ao PDF
        elements.append(table)

        # Adicionar soma da categoria
        category_total = category_df['amount'].sum()
        total_data = [['Total da Categoria:', '', '', '', locale.currency(category_total, grouping=True)]]
        total_table = Table(total_data)
        elements.append(total_table)

        # Adicionar duas linhas em branco
        elements.append(Spacer(1, 24))

    # Adicionar elementos ao documento PDF
    doc.build(elements)

    # Imprimir mensagem de conclusão
    print(f"O relatório foi gerado com sucesso em '{pdf_filename}'.")
else:
    print("Não há registros no banco de dados.")

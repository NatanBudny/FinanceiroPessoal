# Instruções para Utilização do Sistema Financeiro Pessoal

1. Baixe a fatura ou extrato do seu banco em formato CSV.
   - As colunas devem seguir o padrão do Nubank: `date`, `category`, `title`, `amount`.
   - Insira o arquivo CSV na mesma pasta que o script e adicione o formato AAAA-MM no nome do arquivo.

   ![image](https://github.com/NatanBudny/financeiropessoal/assets/35115444/c196483b-a4f6-4823-a72d-55068cbf9ef2)

2. Execute o arquivo "1 - ProcessaArquivo.py".

   Isso criará um arquivo SQLite contendo os dados.
   O arquivo original será renomeado para "filename.processed" para evitar duplicatas.
   Se desejar definir metas, você pode inserir na tabela `meta_gastos` as colunas `[category]` e `[meta]`.

3. Execute o arquivo "2- GeraRelatorio.py".

   O arquivo PDF será gerado:
   ![image](https://github.com/NatanBudny/financeiropessoal/assets/35115444/65e2ec4d-7355-4e4b-9abc-b3767782aba9)

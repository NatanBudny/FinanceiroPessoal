Baixe no seu banco a fatura ou extrato em csv.
As colunas devem ser (padrao nubank): date,category,title,amountdate,category,title,amount
![image](https://github.com/NatanBudny/financeiropessoal/assets/35115444/942e48cd-2d84-4b64-b574-12510a4b94aa)

Insira o csv na mesma pasta que o script (insira o AAAA-MM no nome do arquivo)
![image](https://github.com/NatanBudny/financeiropessoal/assets/35115444/c196483b-a4f6-4823-a72d-55068cbf9ef2)

Execute o arquivo "1 - ProcessaArquivo.py"

Será criado um arquivo sqlite contendo os dados. 
O arquivo que você utilizou será renomeado para filename.processed para evitar duplicidades.
Se quiser utilizar metas você pode inserir na tabela meta_gastos colunas [category],[meta].

Execute o arquivo "2- GeraRelatorio.py"

O arquivo PDF será gerado:
![image](https://github.com/NatanBudny/financeiropessoal/assets/35115444/65e2ec4d-7355-4e4b-9abc-b3767782aba9)

# Vaga Track
Organizador de candidaturas no terminal, com armazenamento local em SQLite.

## Problema resolvido
Acompanhar empresas, cargos e etapas de processos seletivos sem perder registros entre execuções.

## Demonstração
```sh
python app.py adicionar "Empresa Exemplo" "Estágio em desenvolvimento"
python app.py listar
python app.py atualizar 1 entrevista
python app.py listar --status entrevista
python app.py resumo
python app.py exportar candidaturas.csv
```
O ID retornado no cadastro é usado na atualização; pode não ser 1 se já existirem dados.
O comando `resumo` mostra total e quantidade por status. Status disponíveis: enviada, entrevista, aprovada e encerrada.
Os dados ficam em `vagas.db`, ao lado do código. Para testes separados: `python app.py --banco teste.db listar`.

## Como funciona
`argparse` lê os comandos; `conectar` cria a tabela; `adicionar`, `listar` e `atualizar` executam SQL parametrizado. O bloco `with db` confirma a transação, e `csv.writer` exporta registros.

## Limitações
Interface de terminal, sem login ou sincronização. Duplicatas são permitidas, pois podem representar processos distintos. Não publique o banco ou CSV com informações pessoais.

## Decisões técnicas
- **SQLite em vez de lista em memória:** os dados continuam salvos depois que o programa fecha, sem precisar instalar um servidor de banco.
- **SQL parametrizado (`?`):** o que a pessoa digita nunca é colado direto no comando SQL, o que evita SQL injection.
- **ID que não existe:** o programa confere quantas linhas foram alteradas e avisa "Candidatura não encontrada." em vez de fingir que deu certo.

## Próximos passos
- Coluna `link` para guardar o endereço da vaga, com um teste confirmando que o link é salvo e lido de volta.

## Requisitos
Python 3.10 ou superior. Usa apenas a biblioteca padrão: não precisa instalar pacotes nem configurar chaves de API.
No Windows, se `python` não funcionar, use `py` nos mesmos comandos.

## Origem
Projeto de estudo que fiz com apoio de IA (ChatGPT). Usei a primeira versão como base para ler, rodar os testes e entender cada parte do código. Não é um sistema em produção.

## Testes
```sh
python -m unittest -v
```

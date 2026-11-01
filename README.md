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

## Sua próxima melhoria
Adicione uma coluna `link` para guardar o endereço da vaga. Depois crie um teste para confirmar que o link é salvo e recuperado.

## Para explicar numa entrevista
- Por que usar SQLite em vez de uma lista em memória?
- Como os parâmetros `?` evitam concatenar entrada do usuário no SQL?
- O que acontece quando o ID informado não existe?

## Requisitos
Python 3.10 ou superior. Usa apenas a biblioteca padrão: não precisa instalar pacotes nem configurar chaves de API.
No Windows, se `python` não funcionar, use `py` nos mesmos comandos.
Abra a pasta do projeto no VS Code e escolha Terminal > Novo Terminal.

## Origem e aprendizado
Projeto de estudo preparado com apoio do ChatGPT. A versão inicial foi gerada com assistência de IA; este repositório serve como base para leitura, testes e melhorias próprias. Não representa experiência profissional nem um sistema em produção.
Antes de apresentar numa entrevista, execute os exemplos e implemente uma melhoria que consiga explicar.

## Testes
```sh
python -m unittest -v
```

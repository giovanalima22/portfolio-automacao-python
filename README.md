# Automação de Relatórios com Python

## Contexto

Uma equipe recebe arquivos CSV de vendas diariamente. O processo manual envolve consolidar arquivos, limpar dados, calcular indicadores e gerar um relatório.

Este projeto automatiza o processo.

## Fluxo

```text
CSV de vendas
     ↓
Leitura com Pandas
     ↓
Padronização
     ↓
Tratamento de nulos/duplicidades
     ↓
Cálculo dos indicadores
     ↓
Excel consolidado
     ↓
Resumo CSV
```

## Como executar

```bash
pip install -r requirements.txt
python src/generate_data.py
python src/main.py
```

Saída:

```text
output/
├── relatorio_vendas.xlsx
└── resumo_mensal.csv
```

## Regras de negócio

- receita = quantidade × preço unitário;
- registros duplicados são removidos;
- datas são padronizadas;
- vendas são agrupadas por mês;
- ranking de produtos é calculado;
- relatório Excel possui abas de dados, resumo mensal e produtos.

## Competências

`Python` `Pandas` `Excel` `ETL` `Data Quality` `Automation`

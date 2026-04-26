# Job Trend Analytics & Scraper

Um ecossistema em Python desenvolvido para análise inteligente do mercado de trabalho. O projeto vagas de emprego em tempo real via API.

Projeto academico (Global Solutions) - desenvolvida em 2025.

## Objetivo do Projeto
Este projeto foi criado para procurar vagas de empregos, podendo editar os campos de cargos e localização

##  Tecnologias e Conceitos Utilizados
* **Python **: Linguagem base.
* **JSearch API (via RapidAPI)**: Para captura de dados de vagas reais.
* **PyTrends & Pandas**: Para extração e tratamento de médias móveis de interesse de busca.
* **Recursividade**: Implementação de algoritmos recursivos para cálculo de taxas de crescimento.
* **Persistência em JSON**: Estruturação de banco de dados local para armazenamento de resultados filtrados.
* **Tratamento de Exceções**: Robustez no consumo de APIs externas.

##  Funcionalidades
1.  **Menu Interativo**: Permite editar Cargo, Localização e Página de busca antes da execução.
2.  **Cálculo de Tendência**: Analisa a popularidade do cargo nos últimos 5 anos.
3.  **Filtro de Vagas Promissoras**: Separa automaticamente oportunidades de tempo integral (Full-time).
4.  **Relatório Final**: Soma recursiva de taxas de relevância e exportação para `BD.json`.

##  Como Executar
1.  Instale as dependências necessárias:
    ```bash
    pip install requests pytrends pandas
    ```
2.  Obtenha sua chave de API no [JSearch - RapidAPI](https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch/playground/endpoint_f2b4c6e5-2763-450a-a8b2-1e80961e880d).
3.  Substitua a variável `headers` no código com sua chave pessoal.
4.  Execute o script:
    ```bash
    python main.py
    ```

##  Estrutura de Saída
* `BD.json`: Lista completa de vagas com nome, empresa, salário (quando disponível) e link direto.
* `BD_promissoras.json`: Apenas as vagas filtradas com melhores condições de contrato.

---
**Desenvolvido por Rafael Seiji Aoke Arakaki** *Estudante de Engenharia de Software - FIAP*

import warnings
import requests
import json
from pytrends.request import TrendReq
import time

# ignora todos os avisos futuros do Pandas (FutureWarning)
warnings.simplefilter('ignore', FutureWarning)


def obterTendenciasEmprego(cargo, localizacao, pagina, numPaginas="10", dataPostada="all"):
    """
    obtendo as tendencias de empregos
    """

    url = "https://jsearch.p.rapidapi.com/search"

    querystring = {
        "query": f"{cargo}",
        "page": pagina,
        "num_pages": numPaginas,
        "country": localizacao,
        "date_posted": dataPostada
    }

    headers = {
        #key da api
        #ADICINE A SUA KEY NESSAS ASPAS
        "x-rapidapi-key": "",
        "x-rapidapi-host": "jsearch.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, params=querystring)

        if response.status_code == 200:
            dadosApi = response.json()
            listaDeVagas = dadosApi.get("data", [])
            return listaDeVagas

        else:
            print(f"Erro ao fazer a requisição: {response.status_code}")
            print(response.text)
            return []

    except requests.exceptions.RequestException as e:
        print(f"Erro de conexão: {e}")
        return []


def filtrarProfissoes(listaDeVagas):
    vagasPromissoras = []

    for vaga in listaDeVagas:
        tipoContrato = vaga.get("tipo_contrato")

        if tipoContrato and tipoContrato.lower() in ["fulltime", "tempo integral"]:
            vagasPromissoras.append(vaga)

    if not vagasPromissoras:
        print("Nenhuma vaga promissora encontrada :(")

    return vagasPromissoras


def calcular_crescimento_total(cargo, localizacao):
    """
    Obtém e imprime a tabela de interesse de busca do Google Trends
    para um cargo específico nos últimos 5 anos.
    """
    print()

    if localizacao.upper() == 'BR':
        idioma = 'pt-BR'
    else:
        idioma = 'en-US'

    try:

        pytrends = TrendReq(hl=idioma, tz=180, retries=0)

        listaEmprego = [cargo]

        pytrends.build_payload(
            listaEmprego,
            cat=0,
            timeframe='today 5-y',
            geo=localizacao.upper()
        )

        time.sleep(1)

        # Obtém os dados
        df = pytrends.interest_over_time()

        if not df.empty:


            media = df[cargo].mean()
            print(f"--- Tabela de Tendência para '{cargo}' ({localizacao}) ---")
            print(f"Popularidade média de busca de 2020 até 2025 (Escala 0-1): {media/100:.2f}")
            print()


            if media/100 > 0.5:
                print(" O interesse no Cargo está em **CRESCIMENTO**!")
            elif media/100 < 0.5:
                print(" O interesse no Cargo está em **DECLÍNIO**.")
            else:
                print(" O interesse no Cargo está **ESTÁVEL**.")

        else:
            print(f"Não foram encontrados dados de tendência para '{cargo}' no Google Trends.")

    except Exception as e:
        print(f"Erro ao obter dados do Google Trends para '{cargo}'. Verifique o termo de busca ou a localização.")


def somar_taxas_recursivo(lista_com_taxas):
    """
    Calcula a soma total das taxas de crescimento usando recursão.
    """
    # Caso base: Lista vazia, soma é 0.
    if not lista_com_taxas:
        return 0

    taxa_atual = lista_com_taxas[0][1]

    return taxa_atual + somar_taxas_recursivo(lista_com_taxas[1:])


def calcular_taxa_de_crescimento(cargo, localizacao):
    """
    Busca a popularidade média de busca do cargo no Google Trends (0-100)
    e a converte em uma 'taxa' entre 0 e 1.
    """

    if localizacao.upper() == 'BR':
        idioma = 'pt-BR'
    else:
        idioma = 'en-US'

    try:
        pytrends = TrendReq(hl=idioma, tz=180, retries=0)

        listaEmprego = [cargo]

        pytrends.build_payload(
            listaEmprego,
            cat=0,
            timeframe='today 5-y',
            geo=localizacao.upper()
        )

        time.sleep(1)  # Corrigido: Adicionado delay para estabilidade

        df = pytrends.interest_over_time()

        if not df.empty and cargo in df.columns:
            # Obtém a média de popularidade (0-100)
            media = df[cargo].mean()

            taxa_final = media / 100

            return taxa_final
        else:
            return 0.0

    except Exception as e:
        print(f"Atenção: Falha ao obter tendência do Google Trends para '{cargo}': {e}")
        return 0.0


def scriptPrincipal():
    """
    Script principal para interagir com o usuário e chamar a função.
    """

    cargoPadrao = "Desenvolvedor React"
    localizacaoPadrao = "BR"
    paginaPadrao = "1"
    numPaginasPadrao = "10"

    print()
    print("-----------Campos Atuais------------------------------")
    print(f"Cargo: {cargoPadrao}")
    print(f"Localização: {localizacaoPadrao}")
    print(f"Pagina de pesquisa: <{paginaPadrao}>")
    print("------------------------------------------------------")
    print()

    # --- Menu Interativo ---
    while True:
        try:
            editar = int(input("Deseja editar algum campo? \n(1)-SIM\n(2)-NÃO\n\nInsira o código aqui:"))
            if editar == 1:
                # Lógica de edição
                try:
                    print()
                    print("Qual campo deseja editar?")
                    print("------------------------------------------------------")
                    print(f"(1) - Cargo (Atual: {cargoPadrao})")
                    print(f"(2) - Localização (Atual: {localizacaoPadrao})")
                    print(f"(3) - Pagina (Atual: {paginaPadrao})")
                    print("------------------------------------------------------")

                    campoEditar = int(input("Insira o código aqui: "))
                    print()

                    match campoEditar:
                        case 1:
                            cargoPadrao = input("Digite o novo Cargo: ")
                        case 2:
                            localizacaoPadrao = input("Digite a nova Localização (ex: BR, US,): ")
                        case 3:
                            paginaPadrao = str(input("Digite a nova Página: "))
                        case _:
                            print("Opção de campo inválida.")

                except ValueError:
                    print("Erro: Você deve digitar um NÚMERO (1, 2 ou 3).")

            elif editar == 2:
                print()
                print("Iniciando busca com os parâmetros definidos...")
                break
            else:
                print("Código não encontrado")
        except ValueError:
            print("\nCódigo não encontrado\n")

    print(f"Buscando vagas para '{cargoPadrao}'...")

    # Transformas os parametros da função
    listaDeVagasRetornadas = obterTendenciasEmprego(
        cargoPadrao,
        localizacaoPadrao,
        paginaPadrao,
        numPaginas=numPaginasPadrao
    )

    vagasFiltradas = []
    lista_de_taxas_recursiva = []

    # Obtém a taxa base do Google Trends ANTES do loop
    taxa_base_tendencia = calcular_taxa_de_crescimento(cargoPadrao, localizacaoPadrao)

    if listaDeVagasRetornadas:
        for vaga in listaDeVagasRetornadas:
            # Oq sera filtradado como parametro
            vagaFiltrada = {
                "nome_emprego": vaga.get("job_title"),
                "nome_empresa": vaga.get("employer_name"),
                "descricao": vaga.get("job_description"),
                "tipo_contrato": vaga.get("job_employment_type"),
                "salario_min": vaga.get("job_min_salary") or "valor nao informado",
                "salario_max": vaga.get("job_max_salary") or "valor nao informado",
                "data_postagem": vaga.get("job_posted_at_datetime_utc") or "data nao informado",
                "cidade": vaga.get("job_city") or "cidade nao informada",
                "estado": vaga.get("job_state") or "Estado nao informada",
                "pais": vaga.get("job_country"),
                "link_postagem": vaga.get("job_apply_link") or "link nao informado"
            }
            vagasFiltradas.append(vagaFiltrada)

            # Cálculo da Taxa para a Soma Recursiva
            tipo_contrato = vagaFiltrada["tipo_contrato"].lower() if vagaFiltrada["tipo_contrato"] else ""


            taxa_final = taxa_base_tendencia + 0.01 if tipo_contrato in ["fulltime", "tempo integral"] else taxa_base_tendencia

            lista_de_taxas_recursiva.append((vagaFiltrada["nome_emprego"], taxa_final))

    if vagasFiltradas:

        numeroVagaEstimada = len(vagasFiltradas)  #
        soma_taxas = somar_taxas_recursivo(lista_de_taxas_recursiva)  # Cálculo Recursivo

        print("--------------RELATORIO----------------------------------------------")
        print(f"Cargo pesquisado: {cargoPadrao}")
        print(f"Localização: {localizacaoPadrao}")
        print(f"Pagina < {paginaPadrao} >")
        print(f"Número de vagas retornadas: {numeroVagaEstimada}")
        print(f"SOMA TOTAL DAS TAXAS (Recursiva): {soma_taxas:.4f}")  # Exibição Recursiva
        print("-------------------------------------------------------------------")

        try:
            with open("BD.json", "w", encoding="utf-8") as f:
                json.dump(vagasFiltradas, f, indent=4, ensure_ascii=False)
            print(f"Sucesso! {numeroVagaEstimada} vagas (filtradas) salvas em BD.json")

            print()
            selecionar = input("Deseja filtrar as vagas promissoras?\n(1)-SIM\n(2)-NAO\nColoque o codigo aqui:")
            if selecionar == "1":

                listaPromissoras = filtrarProfissoes(vagasFiltradas)
                numPromissoras = len(listaPromissoras)

                with open("BD_promissoras.json", "w", encoding="utf-8") as f:
                    json.dump(listaPromissoras, f, indent=4, ensure_ascii=False)
                print(f"{numPromissoras} vagas promissoras salvas em BD_promissoras.json")

            else:
                print("Ok. Nenhuma filtragem adicional aplicada.")

        except IOError as e:
            print(f"Erro ao salvar arquivo: {e}")
    else:
        print("Nenhuma vaga foi encontrada com esses critérios.")

    print()
    calculo = input(
        f"deseja ver os calculos de crescimento medio para {cargoPadrao}?\n(1) - SIM\n(2) - NÃO\nDigite aqui: ")
    if calculo == "1":
        print("Carregando...")
        calcular_crescimento_total(cargoPadrao, localizacaoPadrao)
    else:
        print("Fechando")

scriptPrincipal()
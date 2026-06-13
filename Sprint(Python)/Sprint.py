import json
import datetime
import uuid

# Dados em memória
clientes = []
apolices = []
sinistros = []

# Arquivos
ARQ_CLIENTES = "clientes.json"
ARQ_APOLICES = "apolices.json"
ARQ_SINISTROS = "sinistros.json"

# -------------------- FUNÇÕES UTILITÁRIAS --------------------

def salvar_dados():
    with open(ARQ_CLIENTES, "w") as f: json.dump(clientes, f, indent=4)
    with open(ARQ_APOLICES, "w") as f: json.dump(apolices, f, indent=4)
    with open(ARQ_SINISTROS, "w") as f: json.dump(sinistros, f, indent=4)

def carregar_dados():
    global clientes, apolices, sinistros
    try:
        with open(ARQ_CLIENTES) as f: clientes = json.load(f)
        with open(ARQ_APOLICES) as f: apolices = json.load(f)
        with open(ARQ_SINISTROS) as f: sinistros = json.load(f)
    except FileNotFoundError:
        pass

def gerar_numero_apolice():
    return str(uuid.uuid4())[:8]  # Apólice com 8 caracteres únicos

def encontrar_cliente_por_cpf(cpf):
    for cliente in clientes:
        if cliente["cpf"] == cpf:
            return cliente
    return None

# -------------------- CADASTROS --------------------

def cadastrar_cliente():
    nome = input("Nome: ")
    cpf = input("CPF: ")
    nascimento = input("Data de Nascimento (dd/mm/aaaa): ")
    endereco = input("Endereço: ")
    telefone = input("Telefone: ")
    email = input("E-mail: ")
    clientes.append({
        "nome": nome, "cpf": cpf, "nascimento": nascimento,
        "endereco": endereco, "telefone": telefone, "email": email
    })
    print("Cliente cadastrado com sucesso!")

def cadastrar_seguro():
    cpf = input("CPF do cliente: ")
    cliente = encontrar_cliente_por_cpf(cpf)
    if not cliente:
        print("Cliente não encontrado.")
        return

    print("Tipos de seguro: 1 - Automóvel | 2 - Residencial | 3 - Vida")
    tipo = input("Escolha o tipo: ")

    dados = {"cliente_cpf": cpf, "numero": gerar_numero_apolice(), "tipo": "", "mensalidade": 0, "dados": {}}

    if tipo == "1":
        dados["tipo"] = "Automóvel"
        modelo = input("Modelo do carro: ")
        ano = input("Ano: ")
        placa = input("Placa: ")
        valor = float(input("Valor do veículo: "))
        dados["mensalidade"] = round(valor * 0.03, 2)
        dados["dados"] = {"modelo": modelo, "ano": ano, "placa": placa, "valor": valor}

    elif tipo == "2":
        dados["tipo"] = "Residencial"
        endereco = input("Endereço do imóvel: ")
        valor = float(input("Valor do imóvel: "))
        dados["mensalidade"] = round(valor * 0.02, 2)
        dados["dados"] = {"endereco": endereco, "valor": valor}

    elif tipo == "3":
        dados["tipo"] = "Vida"
        valor = float(input("Valor segurado: "))
        beneficiarios = input("Beneficiários (separados por vírgula): ").split(",")
        dados["mensalidade"] = round(valor * 0.01, 2)
        dados["dados"] = {"valor": valor, "beneficiarios": beneficiarios}

    else:
        print("Tipo inválido.")
        return

    apolices.append(dados)
    print(f"Apólice {dados['numero']} emitida com sucesso.")

# -------------------- SINISTRO --------------------

def registrar_sinistro():
    numero = input("Número da apólice: ")
    cliente = input("CPF do cliente: ")
    descricao = input("Descrição do ocorrido: ")
    data = datetime.datetime.today().strftime("%d/%m/%Y")
    status = "Aberto"
    sinistros.append({
        "apolice_num": numero,
        "cliente_cpf": cliente,
        "descricao": descricao,
        "data": data,
        "status": status
    })
    print("Sinistro registrado com sucesso.")

# -------------------- RELATÓRIOS --------------------

def listar_apolices_ativas():
    print("\n--- Apólices Ativas ---")
    for apolice in apolices:
        cliente = encontrar_cliente_por_cpf(apolice["cliente_cpf"])
        print(f"Apólice: {apolice['numero']} | Tipo: {apolice['tipo']} | Cliente: {cliente['nome']} | R$ {apolice['mensalidade']}/mês")

def sinistros_por_cliente():
    cpf = input("Digite o CPF do cliente: ")
    print(f"\n--- Sinistros do cliente {cpf} ---")
    for s in sinistros:
        if s["cliente_cpf"] == cpf:
            print(f"{s['data']} - {s['descricao']} ({s['status']})")

def total_premios():
    total = sum(ap["mensalidade"] for ap in apolices)
    print(f"Total de prêmios mensais arrecadados: R$ {total:.2f}")

# -------------------- MENU --------------------

def menu():
    carregar_dados()
    while True:
        print("\n--- SISTEMA DE SEGUROS ---")
        print("1. Cadastrar Cliente")
        print("2. Emitir Apólice de Seguro")
        print("3. Registrar Sinistro")
        print("4. Relatórios")
        print("5. Salvar e Sair")
        opcao = input("Escolha: ")

        if opcao == "1":
            cadastrar_cliente()
        elif opcao == "2":
            cadastrar_seguro()
        elif opcao == "3":
            registrar_sinistro()
        elif opcao == "4":
            print("1. Listar Apólices Ativas")
            print("2. Ver Sinistros por Cliente")
            print("3. Total em Prêmios Mensais")
            subopcao = input("Escolha: ")
            if subopcao == "1":
                listar_apolices_ativas()
            elif subopcao == "2":
                sinistros_por_cliente()
            elif subopcao == "3":
                total_premios()
        elif opcao == "5":
            salvar_dados()
            print("Dados salvos. Até logo!")
            break
        else:
            print("Opção inválida.")

# -------------------- INICIAR --------------------

if __name__ == "__main__":
    menu()

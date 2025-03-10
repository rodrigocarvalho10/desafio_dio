import textwrap

def menu():
    menu = """\n
    ======= Banco RCarvalho ========

    Digite a opção desejada:

    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair

    => """
    return input(textwrap.dedent(menu))

def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
        print(f"O depósito de R$ {valor:.2f} foi efetuado")
    else:
        print("Operação falhou! O valor informado é inválido.")

    return saldo, extrato

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("\nFault: Operação Falhou! Não há saldo suficiente para a operação")
    elif excedeu_limite:
        print("\nFault: Operação Falhou! Não há limite suficiente para a operação")
    elif excedeu_saques:
        print("\nFault: Operação Falhou! Números de saques diários excedidos")
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque:\t\tR$ {valor:.2f}\n"
        numero_saques += 1
        print("\nSucess: Saque realizado com sucesso")
    else:
        print("\nFault: Operação Falhou! Valor informado inválido, refaça a operação")
    
    return saldo, extrato

def exibir_extrato(saldo, /, *, extrato):
     print("\n================ EXTRATO ================")
     print("Não foram realizadas movimentações." if not extrato else extrato)
     print(f"\nSaldo: R$ {saldo:.2f}")
     print("==========================================")

def criar_usuario(usuarios):
    cpf = input("Informe o CPF (formato: 99999999999): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario: 
        print("\nFault: Usuário já cadastrado com o CPF informado")
        return
    
    nome = input("Nome completo: ")
    data_nascimento = input("Data de Nascimento (dd-mm-yyyy): ")
    endereco = input("Endereço (logradouro, nro - Bairro - Cidade/sigla do Estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereço": endereco})

    print("Sucess: Usuário cadastro com sucesso")

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\nSucess: Conta criada com sucesso")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
    print("\nFault: Usuário não encontrado, conta não pode ser criada")

def listar_contas(contas):
    if not contas:
        print("Não temos nenhuma conta cadastrada")
    else:
        for conta in contas:
            linha = f"""\
                Agência:\t{conta['agencia']}
                Nro Conta:\t{conta['numero_conta']}
                Titular:\t{conta['usuario']['nome']}
            """
            print("=" * 100)
            print(textwrap.dedent(linha))

def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"
    
    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    LIMITE_SAQUES = 3
    usuarios = []
    contas = []
    numero_conta = 1

    while True:

        opcao = menu()

        if opcao == "d":
            valor = float(input("Digite o valor do depósito: "))
            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "s":
            valor = float(input("Informe o valor do saque: "))

            saldo, extrato = sacar(
                 saldo=saldo,
                 valor=valor,
                 extrato=extrato,
                 limite=limite,
                 numero_saques=numero_saques,
                 limite_saques=LIMITE_SAQUES,
            )

        elif opcao == "e":
            exibir_extrato(saldo, extrato=extrato)
        elif opcao == "nu":
             criar_usuario(usuarios)

        elif opcao == "nc":
            conta = criar_conta(AGENCIA, numero_conta, usuarios)
            
            if conta:
                contas.append(conta)
                numero_conta += 1

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

main()
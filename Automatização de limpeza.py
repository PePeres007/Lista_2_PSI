import time
import random
import os

# Nome da lista que guardará os cómodos da casa
ARQUIVO_COMODOS = "comodos_casa.txt"

# Estado inicial simulado do robô.
bateria_ok = True
depositos_ok = True
produto_limpeza_ok = True


# --- Funções Auxiliares de Validação ---

def nome_comodo_valido(nome):
    """
    Verifica se o nome de um cómodo é válido.
    Retorna True se contiver apenas letras e espaços e não estiver vazio.
    """
    # 1. Verifica se a string está vazia ou contém apenas espaços
    if not nome.strip():
        return False

    # 2. Verifica cada caractere da string
    for caractere in nome:
        if not (caractere.isalpha() or caractere.isspace()):
            return False

    # 3. Se passou por todas as verificações, o nome é válido
    return True


# --- Funções de Configuração ---

def configurar_primeiro_uso():
    """
    Função executada apenas na primeira utilização.
    Pede ao utilizador para inserir todos os cómodos e guarda-os num ficheiro.
    """
    print("Bem-vindo ao sistema de limpeza automatizada!")
    print("Parece que esta é a primeira utilização.")
    print("Vamos registar todos os cómodos da sua casa.")

    todos_os_comodos = []
    while True:
        nome_comodo = input("Digite o nome de um cómodo (ou 'fim' para terminar): ")

        # Condição de saída do loop
        if nome_comodo.lower() == 'fim':
            if not todos_os_comodos:
                print("!! Nenhum cómodo foi inserido. Tente novamente.")
                continue
            break

        if not nome_comodo_valido(nome_comodo):
            print("!! ERRO: Nome inválido. Use apenas letras e espaços, e não deixe em branco.")
            continue  # Pula para a próxima iteração do loop

        todos_os_comodos.append(nome_comodo.strip().capitalize())
        print(f"'{nome_comodo.capitalize()}' adicionado. Cómodos atuais: {', '.join(todos_os_comodos)}")

    with open(ARQUIVO_COMODOS, 'w', encoding='utf-8') as f:
        for comodo in todos_os_comodos:
            f.write(f"{comodo}\n")

    print("\nCómodos registados com sucesso!")
    # Na primeira vez, limpamos todos os cómodos registados
    return todos_os_comodos


def configurar_rota_diaria():
    """
    Função executada nas utilizações seguintes.
    Lê os cómodos do ficheiro, mostra ao utilizador e pergunta quais limpar.
    """
    print("Bem-vindo de volta!")

    with open(ARQUIVO_COMODOS, 'r', encoding='utf-8') as f:
        todos_os_comodos = [linha.strip() for linha in f.readlines()]

    print("Estes são os cómodos registados:")
    for i, comodo in enumerate(todos_os_comodos):
        print(f"  {i + 1}: {comodo}")

    rota_de_hoje = []
    while True:
        try:
            escolha = input("\nQuais cómodos deseja limpar hoje? Digite os números separados por vírgula (ex: 1, 3); "
                            "\n se desejar não limpar nenhum comodo aperte enter: ")
            if not escolha:
                print("Nenhuma seleção feita. A encerrar a limpeza de hoje.")
                return []

            numeros_escolhidos = [int(num.strip()) for num in escolha.split(',')]

            rota_de_hoje = []
            valido = True
            for num in numeros_escolhidos:
                if 1 <= num <= len(todos_os_comodos):
                    rota_de_hoje.append(todos_os_comodos[num - 1])
                else:
                    print(f"!! ERRO: O número {num} é inválido. Por favor, escolha números da lista.")
                    valido = False
                    break

            if valido:
                rota_de_hoje = list(dict.fromkeys(rota_de_hoje))  # Remove duplicados
                break

        except ValueError:
            print("!! ERRO: Entrada inválida. Por favor, digite apenas números separados por vírgula.")

    print(f"\nRota de limpeza definida para hoje: {', '.join(rota_de_hoje)}")
    return rota_de_hoje


# --- Funções de Limpeza ---

def verificar_estado_robo():
    """Verifica as condições iniciais do robô (bateria, depósitos)."""
    global bateria_ok, depositos_ok
    if not bateria_ok:
        print("!! ERRO: Bateria fraca. A iniciar recarga...")
        time.sleep(2)
        bateria_ok = True
        print(">> Bateria carregada!")
    if not depositos_ok:
        print("!! ERRO: Depósito de lixo cheio. Por favor, esvazie para continuar.")
        time.sleep(2)
        depositos_ok = True
        print(">> Depósito esvaziado pelo utilizador.")
    return True


def limpar_comodo(comodo):
    """Executa a sequência de limpeza para um único cómodo."""
    print(f"\n--- A iniciar a limpeza do(a): {comodo} ---")
    print(f"[{comodo}] A organizar e a mover pequenos obstáculos...")
    time.sleep(2.5)
    if random.random() < 0.2:
        print(f"!! AVISO: [{comodo}] Obstáculo pesado encontrado. A contornar.")
    print(f"[{comodo}] A aspirar o chão...")
    time.sleep(2)
    if comodo.lower() != "quarto" and produto_limpeza_ok:
        print(f"[{comodo}] A lavar o chão com pano húmido...")
        time.sleep(2)
    elif not produto_limpeza_ok:
        print(f"!! AVISO: [{comodo}] A lavagem foi pulada por falta de produto.")
    else:
        print(f"!! AVISO: [{comodo}] A lavagem foi pulada (chão de tapete).")
    print(f">>> {comodo} limpo! <<<")
    return True


# --- Corpo Principal do Programa (main) ---
if __name__ == "__main__":
    comodos_para_limpar = []

    if not os.path.exists(ARQUIVO_COMODOS):
        # Primeira vez: registra os cómodos e define a rota para limpar todos.
        os.system('cls')
        configurar_primeiro_uso()

        comodos_para_limpar = configurar_rota_diaria()
    else:
        # Outras vezes: pergunta ao utilizador quais cómodos limpar.
        os.system('cls')
        comodos_para_limpar = configurar_rota_diaria()

    # Prossegue com a limpeza apenas se houver cómodos selecionados e o robô estiver OK
    if comodos_para_limpar:
        print("\n### INICIANDO SISTEMA DE LIMPEZA AUTOMATIZADA ###")
        if verificar_estado_robo():
            print("\nRobô pronto para iniciar a limpeza.")
            comodos_limpos = []
            for comodo in comodos_para_limpar:
                if limpar_comodo(comodo):
                    comodos_limpos.append(comodo)

            print("\n### LIMPEZA FINALIZADA! ###")
            print(f"Cómodos limpos hoje: {', '.join(comodos_limpos)}")
            print("Robô a voltar para a base e a entrar em modo de espera.")
    else:
        print("\nNenhum cómodo foi selecionado para limpeza. Programa encerrado.")

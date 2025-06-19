import time
import random
import os

# --- Constantes e Configuração ---
# Nome do ficheiro que guardará os comodos da casa
ARQUIVO_COMODOS = "comodos_casa.txt"

# Estado do robô.
bateria_ok = True
depositos_ok = True
produto_limpeza_ok = True

# --- Funções de Configuração ---
def ConfigurarPrimeiroUso():
    """
    Função executada apenas na primeira utilização.
    Pede ao utilizador para inserir todos os cómodos e os guarda em uma lista.
    """
    print("Bem-vindo ao seu Robô de Limpeza!")
    print("Parece que esta é a primeira utilização.")
    print("Vamos registar todos os cómodos da sua casa.")
    
    todos_os_comodos = []
    while True:
        # Pede para inserir o nome do cómodo
        nome_comodo = input("Digite o nome de um cómodo (ou 'fim' para terminar): ")
        if nome_comodo.lower() == 'fim':
            if not todos_os_comodos:
                print("!! Nenhum cómodo foi inserido. Tente novamente.")
                continue
            break
        todos_os_comodos.append(nome_comodo.strip().capitalize())
        print(f"'{nome_comodo}' adicionado. Cómodos atuais: {', '.join(todos_os_comodos)}")

    # Guarda a lista de cómodos no ficheiro de texto
    with open(ARQUIVO_COMODOS, 'a', encoding='utf-8') as lista:
        for comodo in todos_os_comodos:
            lista.write(f"{comodo}\n")
            
    print("\n Cómodos registados com sucesso!")
    # Na primeira vez, limpamos todos os cómodos registados
    return todos_os_comodos

def ConfigurarRotaDiaria():
    """
    Função executada nas utilizações seguintes.
    Lê os cómodos do ficheiro, mostra ao utilizador e pergunta quais limpar.
    """
    print("Bem-vindo de volta!")
    
    # Lê os cómodos registados a partir do ficheiro
    with open(ARQUIVO_COMODOS, 'r', encoding='utf-8') as f:
        todos_os_comodos = [linha.strip() for linha in f.readlines()]

    print("Estes são os cómodos registados:")
    for i, comodo in enumerate(todos_os_comodos):
        print(f"  {i + 1}: {comodo}")

    rota_de_hoje = []
    while True:
        try:
            escolha = input("\nQuais cómodos deseja limpar hoje? Digite os números separados por vírgula (ex: 1, 3): ")
            if not escolha:
                print("Nenhuma seleção feita. A encerrar a limpeza de hoje.")
                time.sleep(2)
                return []
            
            numeros_escolhidos = [int(num.strip()) for num in escolha.split(',')]
            
            # Valida os números inseridos pelo utilizador
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
                # Remove duplicados caso o utilizador digite "1, 1"
                rota_de_hoje = list(dict.fromkeys(rota_de_hoje)) 
                break

        except ValueError:
            print("!! ERRO: Entrada inválida. Por favor, digite apenas números separados por vírgula.")

    print(f"\nRota de limpeza definida para hoje: {', '.join(rota_de_hoje)}")
    return rota_de_hoje

# --- Funções de Limpeza ---

def VerificarEstadoRobo():
    """
    Verifica as condições iniciais do robô (bateria, depósitos).
    Retorna True se tudo estiver OK, senão, lida com o erro e retorna False.
    """
    global bateria_ok, depositos_ok
    if not bateria_ok:
        print("!! ERRO: Bateria fraca. A iniciar recarga...")
        time.sleep(3)
        bateria_ok = True
        print(">> Bateria carregada!")
    if not depositos_ok:
        print("!! ERRO: Depósito de lixo cheio. Por favor, esvazie para continuar.")
        time.sleep(2)
        depositos_ok = True
        print(">> Depósito esvaziado pelo utilizador.")
    return True

def LimparComodo(comodo):
    """
    Executa a sequência de limpeza para um único cómodo.
    """
    print(f"\n--- A iniciar a limpeza do(a): {comodo} ")
    print(f"[{comodo}] A organizar e a mover pequenos obstáculos...")
    time.sleep(2)
    if random.random() < 0.2: # utilizado apenas para fazer uma simulação de problema
        print(f"!! AVISO: [{comodo}] Obstáculo pesado encontrado. Marcando localização e contornando.")
    print(f"[{comodo}] A aspirar o chão...")
    time.sleep(3)
    if comodo.lower() != "quarto" and produto_limpeza_ok:
        print(f"[{comodo}] A lavar o chão com pano húmido...")
        time.sleep(2)
    elif not produto_limpeza_ok:
        print(f"!! AVISO: [{comodo}] A lavagem foi pulada por falta de produto.")
    else:
        print(f"[{comodo}] A lavagem foi pulada (chão de tapete).")
    print(f">>> {comodo} limpo! <<<")
    return True

# --- Corpo Principal do Programa (main) ---
if __name__ == "__main__":
    comodos_para_limpar = []
    
    # A biblioteca 'os' ajuda a interagir com o sistema operativo, como verificar se um ficheiro existe.
    if not os.path.exists(ARQUIVO_COMODOS):
        ConfigurarPrimeiroUso() 
        comodos_para_limpar = ConfigurarRotaDiaria()
    else:
        comodos_para_limpar = ConfigurarRotaDiaria()

    # Prossegue com a limpeza apenas se houver cómodos selecionados e o robô estiver OK
    if comodos_para_limpar:
        print("\n### INICIANDO SISTEMA DE LIMPEZA AUTOMATIZADA ###")
        if VerificarEstadoRobo():
            print("\nRobô pronto para iniciar a limpeza.")
            comodos_limpos = []
            for comodo in comodos_para_limpar:
                if LimparComodo(comodo):
                    comodos_limpos.append(comodo)
            
            print("\n### LIMPEZA FINALIZADA! ###")
            print(f"Cómodos limpos hoje: {', '.join(comodos_limpos)}")
            print("Robô a voltar para a base e a entrar em modo de espera.")
    else:
        print("\nNenhum cómodo foi selecionado para limpeza. Programa encerrado.")
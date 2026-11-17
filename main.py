import sys
import os
import time
import sqlite3

from database import inicializar_banco
from plantas import Plantas
from familias import Familias
from categorias import Categorias
from regioes import Regioes


def limpar():
    time.sleep(2)
    os.system('cls' if os.name == 'nt' else 'clear')


def pausar():
    input("\nPressione ENTER para continuar...")
    limpar()

def menu():
    print("CATÁLOGO DE PLANTAS\n")
    print("1 - Gerenciar plantas")
    print("2 - Gerenciar famílias")
    print("3 - Gerenciar categorias")
    print("4 - Gerenciar regiões")
    print("5 - Encerrar programa")

    print("\n\n*Antes de cadastrar uma planta cadastre sua Família Botânica, sua Categoria e sua Região.")

def menu_crud(nome):
    print(f"\nGERENCIAR {nome.upper()}\n")
    print("1 - Cadastrar")
    print("2 - Consultar")
    print("3 - Atualizar")
    print("4 - Excluir")
    print("5 - Voltar")

def cadastrar_relacionamentos(id_planta):

    print("\nCATEGORIAS DISPONÍVEIS:")

    categorias = Categorias.select()

    for categoria in categorias:
        print(f"{categoria[0]} - {categoria[1]}")

    if categorias:
        escolha = input(
            "\nDigite o ID da categoria (ENTER para pular): "
        ).strip()

        if escolha.isdigit():
            Plantas.vincular_categoria(id_planta, int(escolha))

    print("\nREGIÕES DISPONÍVEIS:")

    regioes = Regioes.select()

    for regiao in regioes:
        print(f"{regiao[0]} - {regiao[1]}")

    if regioes:
        escolha = input(
            "\nDigite o ID da região (ENTER para pular): "
        ).strip()

        if escolha.isdigit():
            Plantas.vincular_regiao(id_planta, int(escolha))


def cadastrar_planta():

    print("\nCADASTRAR PLANTA\n")

    nome = input("Nome científico: ")
    populares = input("Nomes populares: ")
    descricao = input("Descrição: ")

    familias = Familias.select()

    if not familias:
        print("\nCadastre uma família antes de cadastrar plantas.")
        return

    print("\nFAMÍLIAS DISPONÍVEIS:")

    for familia in familias:
        print(f"{familia[0]} - {familia[1]}")

    id_familia = input("\nDigite o ID da família: ")

    if not id_familia.isdigit():
        print("ID inválido.")
        return

    familia_existe = any(
        familia[0] == int(id_familia)
        for familia in familias
    )

    if not familia_existe:
        print("Família não encontrada.")
        return

    planta = Plantas(nome, populares, descricao)
    planta.insert(int(id_familia))

    plantas = Plantas.select()
    id_planta = next(
        planta[0] for planta in plantas
        if planta[1] == nome.strip().upper()
    )

    print("\nPlanta cadastrada com sucesso!")

    cadastrar_relacionamentos(id_planta)


def consultar_plantas():

    plantas = Plantas.select()

    if not plantas:
        print("\nNenhuma planta cadastrada.")
        return 1

    print("\nPLANTAS CADASTRADAS\n")

    for planta in plantas:
        print(f"ID: {planta[0]}")
        print(f"Nome científico: {planta[1]}")
        print(f"Nomes populares: {planta[2]}")
        print(f"Descrição: {planta[3]}")
        print(f"Família: {planta[4]}")

        categorias, regioes = Plantas.consultar_relacionamentos(planta[0])

        nomes_categorias = [item[0] for item in categorias]
        nomes_regioes = [item[0] for item in regioes]

        print(f"Categorias: {', '.join(nomes_categorias) or 'Nenhuma'}")
        print(f"Regiões: {', '.join(nomes_regioes) or 'Nenhuma'}")
        print("-" * 40)


def atualizar_planta():

    retorno_atualizar = consultar_plantas()

    if retorno_atualizar ==1:
        return

    id_planta = input("\nDigite o ID da planta que deseja atualizar: ")

    if not id_planta.isdigit():
        print("ID inválido.")
        return

    id_planta = int(id_planta)

    plantas = Plantas.select()
    planta = next(
        (p for p in plantas if p[0] == id_planta),
        None
    )

    if planta is None:
        print("Planta não encontrada.")
        return

    print("\nDigite as novas informações:")

    nome = input(f"Nome científico [{planta[1]}]: ").strip()
    populares = input(f"Nomes populares [{planta[2]}]: ").strip()
    descricao = input(f"Descrição [{planta[3]}]: ").strip()

    familias = Familias.select()

    print("\nFAMÍLIAS DISPONÍVEIS:")

    for familia in familias:
        print(f"{familia[0]} - {familia[1]}")

    id_familia = input(
        f"\nID da família [{next(f[0] for f in familias if f[1] == planta[4])}]: ").strip()

    if not nome:
        nome = planta[1]

    if not populares:
        populares = planta[2]

    if not descricao:
        descricao = planta[3]

    if not id_familia:
        id_familia = next(
            f[0] for f in familias if f[1] == planta[4]
        )
    elif not id_familia.isdigit() or not any(
        f[0] == int(id_familia) for f in familias
    ):
        print("Família inválida.")
        return
    else:
        id_familia = int(id_familia)

    resultado = Plantas.update(
        id_planta, nome, populares, descricao, id_familia
    )

    if resultado:
        print("\nPlanta atualizada com sucesso!")
    else:
        print("\nNenhuma alteração realizada.")


def excluir_planta():

    retorno_excluir = consultar_plantas()

    if retorno_excluir ==1:
        return

    id_planta = input("\nDigite o ID da planta que deseja excluir: ")

    if not id_planta.isdigit():
        print("ID inválido.")
        return

    confirmacao = input(
        "\nTem certeza que deseja excluir? (S/N): "
    ).strip().upper()

    if confirmacao == "S":
        resultado = Plantas.delete(int(id_planta))

        if resultado:
            print("\nPlanta excluída com sucesso!")
        else:
            print("Planta não encontrada.")


def gerenciar_entidade(classe, nome):

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        menu_crud(nome)
        escolha = input("\n=> ")
        limpar()

        try:
            if escolha == "1":

                print(f"\nCADASTRAR {nome.upper()}\n")

                if classe == Familias:
                    nome_item = input("Nome da família: ")
                    descricao = input("Descrição: ")
                    item = Familias(nome_item, descricao)

                elif classe == Categorias:
                    nome_item = input("Nome da categoria: ")
                    item = Categorias(nome_item)

                else:
                    nome_item = input("Nome da região: ")
                    item = Regioes(nome_item)

                item.insert()
                print("\nCadastro realizado com sucesso!")

            elif escolha == "2":

                registros = classe.select()

                if not registros:
                    print("\nNenhum registro encontrado.")
                else:
                    print(f"\nCADASTROS DE {nome.upper()}\n")

                    for registro in registros:
                        print(registro)

            elif escolha == "3":

                registros = classe.select()

                if not registros:
                    print("\nNenhum registro encontrado.")
                else:
                    for registro in registros:
                        print(registro)

                    id_item = input("\nDigite o ID que deseja atualizar: ")

                    if not id_item.isdigit():
                        print("ID inválido.")
                        pausar()
                        continue

                    registro = next(
                        (r for r in registros if r[0] == int(id_item)),
                        None
                    )

                    if registro is None:
                        print("Registro não encontrado.")

                    elif classe == Familias:
                        nome_item = input(
                            f"Novo nome [{registro[1]}]: "
                        ).strip()

                        descricao = input(
                            f"Nova descrição [{registro[2] or ''}]: "
                        ).strip()

                        if not nome_item:
                            nome_item = registro[1]

                        if not descricao:
                            descricao = registro[2] or ""

                        resultado = Familias.update(
                            int(id_item), nome_item, descricao
                        )

                        print(
                            "Família atualizada!"
                            if resultado else "Nenhuma alteração realizada."
                        )

                    else:
                        nome_item = input(
                            f"Novo nome [{registro[1]}]: "
                        ).strip()

                        if not nome_item:
                            nome_item = registro[1]

                        resultado = classe.update(
                            int(id_item), nome_item
                        )

                        print(
                            "Cadastro atualizado!"
                            if resultado else "Nenhuma alteração realizada."
                        )

            elif escolha == "4":

                registros = classe.select()

                if not registros:
                    print("\nNenhum registro encontrado.")
                else:
                    for registro in registros:
                        print(registro)

                    id_item = input("\nDigite o ID que deseja excluir: ")

                    if not id_item.isdigit():
                        print("\nID inválido.")
                        pausar()
                        continue

                    confirmacao = input(
                        "\nConfirma a exclusão? (S/N): "
                    ).strip().upper()

                    if confirmacao == "S":
                        resultado = classe.delete(int(id_item))

                        if resultado:
                            print("\nRegistro excluído com sucesso!")
                        else:
                            print("\nRegistro não encontrado.")

            elif escolha == "5":
                break

            else:
                print("Opção inválida.")

        except sqlite3.IntegrityError as erro:
            print(f"\nNão foi possível realizar a operação: {erro}")

        except sqlite3.Error as erro:
            print(f"\nErro no banco de dados: {erro}")

        except ValueError:
            print("\nInforme um valor válido.")

        pausar()


def gerenciar_plantas():

    while True:
        menu_crud("plantas")
        escolha = input("\n=> ")
        limpar()

        try:
            if escolha == "1":
                cadastrar_planta()

            elif escolha == "2":
                consultar_plantas()

            elif escolha == "3":
                atualizar_planta()

            elif escolha == "4":
                excluir_planta()

            elif escolha == "5":
                break

            else:
                print("Opção inválida.")

        except sqlite3.IntegrityError as erro:
            print(f"\nNão foi possível realizar a operação: {erro}")

        except sqlite3.Error as erro:
            print(f"\nErro no banco de dados: {erro}")

        pausar()


def encerrar_programa():

    while True:
        confirmacao = input("Deseja realmente encerrar o programa? (S/N): ").strip().upper()

        if confirmacao == "S":
            print("\nEncerrando o programa... Até logo!")
            limpar()
            sys.exit()
        elif confirmacao == "N":
            print("\nVoltando ao menu principal...")
            limpar()
            break
        else:
            print("\nDigite apenas S ou N.")
            limpar()


def main():

    inicializar_banco()

    while True:

        os.system('cls' if os.name == 'nt' else 'clear')
        print("SEJA BEM-VINDO AO CATÁLOGO DE PLANTAS! 🌳🌿🌱\n")
        menu()

        escolha = input("\n=> ")

        match escolha:

            case "1":
                os.system('cls' if os.name == 'nt' else 'clear')
                print("Você escolheu a opção 01: GERENCIAR PLANTAS. 🌺")
                limpar()
                gerenciar_plantas()

            case "2":
                os.system('cls' if os.name == 'nt' else 'clear')
                print("Você escolheu a opção 02: GERENCIAR FAMILIAS. 🌻")
                limpar()
                gerenciar_entidade(Familias, "famílias")

            case "3":
                os.system('cls' if os.name == 'nt' else 'clear')
                print("Você escolheu a opção 03: GERENCIAR CATEGORIAS. 🌹")
                limpar()
                gerenciar_entidade(Categorias, "categorias")

            case "4":
                os.system('cls' if os.name == 'nt' else 'clear')
                print("Você escolheu a opção 04: GERENCIAR REGIÕES. 🌼")
                limpar()
                gerenciar_entidade(Regioes, "regiões")

            case "5":
                os.system('cls' if os.name == 'nt' else 'clear')
                print("Você escolheu a opção 05: ENCERRAR PROGRAMA. 🍂")
                limpar()
                encerrar_programa()

            case _:
                print("Opção inválida! Escolha um número entre 1 e 5.")
                pausar()


if __name__ == "__main__":
    main()


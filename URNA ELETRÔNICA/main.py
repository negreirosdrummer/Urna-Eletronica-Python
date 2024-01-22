import pickle
import matplotlib.pyplot as plt
import pygame
from time import sleep


def ler_candidatos():
    dict_candidatos = {}

    while True:
        txt_candidatos = input("Informe a localização dos dados dos candidatos: ")

        # tenta abrir o arquivo com o nome especificado. caso não exista, mostra mensagem de erro
        try:
            with open(txt_candidatos, "r", encoding='utf-8') as candidatostxt:
                # armazena cada linha como um item na lista candidatos
                candidatos = candidatostxt.readlines()
            break
        except FileNotFoundError:
            print(f"Erro: O arquivo '{txt_candidatos}' não foi encontrado. Tente novamente.\n")

    # itera sobre a lista para remover quebras de linha e criar outra
    # lista usando a vírgula e espaço como delimitadores
    for i in candidatos:
        dados = i.strip().split(', ')

        # cria um dicionário com os pares chave-valor para cada item da lista "dados"
        candidato = {
            'Nome': dados[0],
            'Número': int(dados[1]),
            'Partido': dados[2],
            'UF': dados[3],
            'Cargo': dados[4],
        }
        # adiciona pares chave-valor ao dicionário dict_candidatos
        # o número do candidato é a chave e os dados do candidato são o valor
        dict_candidatos[dados[1]] = candidato
    print()
    print("CARREGANDO ARQUIVO DE CANDIDATOS...")
    sleep(0.5)
    print()
    print("-=" * 22)
    print("ARQUIVO DE CANDIDATOS CARREGADO COM SUCESSO!")
    print("-=" * 22)
    sleep(1.5)
    # a variável ok_candidatos com valor "True" é usada para conceder acesso aos menus 3, 4, 5 e 6
    ok_candidatos = True
    return dict_candidatos, ok_candidatos


def ler_eleitores():
    dict_eleitores = {}

    # zera o arquivo de votos
    with open("votos.bin", "ab") as votos_bin:
        votos_bin.truncate(0)

    while True:
        txt_eleitores = input("Informe a localização dos dados dos eleitores: ")

        try:
            with open(txt_eleitores, "r", encoding='utf-8') as eleitorestxt:
                # armazena cada linha como um item na lista eleitores
                eleitores = eleitorestxt.readlines()
            break
        except FileNotFoundError:
            print(f"Erro: O arquivo '{txt_eleitores}' não foi encontrado. Tente novamente.\n")

    # itera sobre a lista para remover quebras de linha e
    # criar outra lista usando a vírgula e espaço como delimitadores
    for i in eleitores:
        dados = i.strip().split(', ')

        # Cria um dicionário com os pares chave-valor para cada item da lista "dados"
        eleitores = {
            'Nome': dados[0],
            'Identidade': dados[1],
            'Título': int(dados[2]),
            'Cidade': dados[3],
            'UF': dados[4]
        }
        # Adiciona pares chave-valor ao dicionário dict_eleitores
        # o número do título de eleitor é a chave e os dados do eleitor são o valor
        dict_eleitores[dados[2]] = eleitores
    print()
    print("CARREGANDO ARQUIVO DE ELEITORES...")
    sleep(0.5)
    print()
    print("-=" * 22)
    print("ARQUIVO DE ELEITORES CARREGADO COM SUCESSO!")
    print("-=" * 22)
    sleep(1.5)
    # a variável ok_eleitores com valor "True" é usada para conceder acesso aos menus 3, 4, 5 e 6
    ok_eleitores = True
    # cria a variável eleitores_aptos para usar na hora de mostrar os resultados
    eleitores_aptos = len(dict_eleitores)
    return dict_eleitores, ok_eleitores, eleitores_aptos


def iniciar_votacao(dict_candidatos, dict_eleitores):
    # variável novo_voto com valor 'S' para poder entrar no laço de repetição da votação
    novo_voto = 'S'
    while novo_voto == 'S':
        # lista de estados que o mesário pode definir na urna
        lista_estados = ["MG", "SP", "RJ", "ES"]
        uf_urna = input("UF onde está localizada a urna: ").upper()
        # não deixa prosseguir caso seja digitado um estado que não estiver na lista_estados
        while uf_urna not in lista_estados:
            print("UF deve ser MG, SP, RJ ou ES.\n")
            uf_urna = input("UF onde está localizada a urna: ").upper()
        # define titulo de eleitor como zero, para poder entrar no laço de repetição da linha 126
        titulo_eleitor = 0
        # cria o dicionário "voto" para armazenar o voto do eleitor atual
        voto = {}
        # não deixa iniciar a votação se o número de eleitores disponíveis no dicionário for zero
        if len(dict_eleitores) == 0:
            print("Todos os eleitores dessa seção já votaram.")
            print("Por favor, realize a apuração dos votos através da opção 4 do menu")
            sleep(2)
            return

        # adiciona a UF inserida no dicionário voto, com a chave sendo "UF"
        voto["UF"] = uf_urna
        # pede o título de eleitor e checa se ele ele existe no dict_eleitores
        # se sim, checa se ele está na mesma UF da urna
        while titulo_eleitor not in dict_eleitores.keys() or dict_eleitores[titulo_eleitor]['UF'] != uf_urna:
            titulo_eleitor = input("Informe o Título de Eleitor: ")
            if titulo_eleitor not in dict_eleitores.keys():
                print("Título de Eleitor não encontrado!\n")
            elif dict_eleitores[titulo_eleitor]['UF'] != uf_urna:
                print("Eleitor não encontrado nessa UF!\n")
        # caso o eleitor exista e esteja na mesma UF da urna, apresenta os dados do eleitor na tela
        if dict_eleitores[titulo_eleitor]['UF'] == uf_urna:
            print()
            print("-=" * 20)
            print(f"Nome do Eleitor: {dict_eleitores[titulo_eleitor]['Nome']}")
            print(f"UF do Eleitor: {dict_eleitores[titulo_eleitor]['UF']}")
            print("-=" * 20)

        # inicia a votação para Deputado Federal
        while True:
            numero_f = input("\nInforme o voto para Deputado Federal: ")
            # checa se o eleitor digitou "B" ou "b" para votar em branco
            if numero_f in "Bb":
                em_branco = input("Voto em Branco. Confirma? [S/N]: ").upper()
                # não deixa prosseguir enquanto o eleitor não responda "S" ou "N"
                while em_branco not in "SN" or em_branco == '':
                    print("Por favor, digite S para votar em branco ou N para voltar e escolher um candidato.")
                    em_branco = input("Voto em Branco. Confirma? [S/N]: ").upper()
                # se confirmar o voto em branco, salva no dicionário "voto" a chave "F" com valor "B", e
                # sai do laço de repetição
                if em_branco == "S":
                    print("Voto em branco confirmado para Deputado Federal")
                    voto["F"] = "B"
                    break
            # checa se o numero digitado se encontra no dicionário
            # se não, pergunta se deseja anular o voto
            elif numero_f not in dict_candidatos.keys():
                anular = input("Candidato inexistente. Deseja anular o voto? [S/N]: ").upper()
                # não deixa prosseguir enquanto o eleitor não responda "S" ou "N"
                while anular not in 'SN':
                    print("Por favor, digite S para anular ou N para voltar e escolher um candidato.")
                    anular = input("Deseja anular o voto? [S/N]: ").upper()
                # se confirmar a anulação do voto, salva no dicionário "voto" a chave "F" com valor "N", e
                # sai do laço de repetição
                if anular == 'S':
                    print("Voto para Deputado Estadual anulado")
                    voto["F"] = "N"
                    break
            # checa se o cargo do candidato digitado corresponde ao cargo de Deputado Federal
            elif dict_candidatos[numero_f]['Cargo'] != "F":
                print("Erro. Número do Deputado Federal deve ter 4 dígitos")
            # checa se a UF do candidato escolhido é diferente da UF da urna. se for, pergunta se deseja anular o voto
            elif dict_eleitores[titulo_eleitor]['UF'] != dict_candidatos[numero_f]['UF']:
                anular = input("Candidato de outro estado. Deseja anular o voto? [S/N]: ").upper()
                # não deixa prosseguir enquanto o eleitor não responda "S" ou "N"
                while anular not in 'SN':
                    print("Por favor, digite S para anular ou N para voltar e escolher um candidato.")
                    anular = input("Candidato de outro estado. Deseja anular o voto? [S/N]: ").upper()
                # se confirmar a anulação do voto, salva no dicionário "voto" a chave "F" com valor "N", e
                # sai do laço de repetição
                if anular == 'S':
                    print("Voto para Deputado Federal anulado")
                    voto["F"] = "N"
                    break
            # checa se o número do candidato escolhido está no dicionário de candidatos
            elif numero_f in dict_candidatos.keys():
                confirma = input(
                    f"Confirma voto no candidato {dict_candidatos[numero_f]['Nome']} | {dict_candidatos[numero_f]['Partido']}? [S/N]: ").upper()
                # não deixa prosseguir enquanto o eleitor não responda "S" ou "N"
                while confirma not in 'SN':
                    print("Por favor, digite S para confirmar ou N para escolher outro candidato.")
                    confirma = input(
                        f"Confirma voto no candidato {dict_candidatos[numero_f]['Nome']} | {dict_candidatos[numero_f]['Partido']}? [S/N]: ").upper()
                # se confirmar o voto, salva no dicionário "voto" a chave "F" e o número do candidato como valor, e
                # sai do laço de repetição
                if confirma == 'S':
                    print(
                        f"Voto confirmado no candidato {dict_candidatos[numero_f]['Nome']} | {dict_candidatos[numero_f]['Partido']}")
                    voto["F"] = numero_f
                    break

        # inicia a votação para Deputado Estadual
        while True:
            numero_e = input("\nInforme o voto para Deputado Estadual: ")
            if numero_e in "Bb":
                em_branco = input("Voto em Branco. Confirma? [S/N]: ").upper()
                while em_branco not in "SN" or em_branco == '':
                    print("Por favor, digite S para votar em branco ou N para voltar e escolher um candidato.")
                    em_branco = input("Voto em Branco. Confirma? [S/N]: ").upper()
                if em_branco == "S":
                    print("Voto em branco confirmado para Deputado Estadual")
                    voto["E"] = "B"
                    break
            elif numero_e not in dict_candidatos.keys():
                anular = input("Candidato inexistente. Deseja anular o voto? [S/N]: ").upper()
                while anular not in 'SN':
                    print("Por favor, digite S para anular ou N para voltar e escolher um candidato.")
                    anular = input("Deseja anular o voto? [S/N]: ").upper()
                if anular == 'S':
                    print("Voto para Deputado Estadual anulado")
                    voto["E"] = "N"
                    break
            elif dict_candidatos[numero_e]['Cargo'] != "E":
                print("Erro. Número do Deputado Estadual deve ter 5 dígitos")
            elif dict_eleitores[titulo_eleitor]['UF'] != dict_candidatos[numero_e]['UF']:
                anular = input("Candidato de outro estado. Deseja anular o voto? [S/N]: ").upper()
                while anular not in 'SN':
                    print("Por favor, digite S para anular ou N para voltar e escolher um candidato.")
                    anular = input("Candidato de outro estado. Deseja anular o voto? [S/N]: ").upper()
                if anular == 'S':
                    print("Voto para Deputado Estadual anulado")
                    voto["E"] = "N"
                    break
            elif numero_e in dict_candidatos.keys():
                confirma = input(
                    f"Confirma voto no candidato {dict_candidatos[numero_e]['Nome']} | {dict_candidatos[numero_e]['Partido']}? [S/N]: ").upper()
                while confirma not in 'SN':
                    print("Por favor, digite S para confirmar ou N para escolher outro candidato.")
                    confirma = input(
                        f"Confirma voto no candidato {dict_candidatos[numero_e]['Nome']} | {dict_candidatos[numero_e]['Partido']}? [S/N]: ").upper()
                if confirma == 'S':
                    print(
                        f"Voto confirmado no candidato {dict_candidatos[numero_e]['Nome']} | {dict_candidatos[numero_e]['Partido']}")
                    voto["E"] = numero_e
                    break

        # inicia a votação para Senador
        while True:
            numero_s = input("\nInforme o voto para Senador: ")
            if numero_s in "Bb":
                em_branco = input("Voto em Branco. Confirma? [S/N]: ").upper()
                while em_branco not in "SN" or em_branco == '':
                    print("Por favor, digite S para votar em branco ou N para voltar e escolher um candidato.")
                    em_branco = input("Voto em Branco. Confirma? [S/N]: ").upper()
                if em_branco == "S":
                    print("Voto em branco confirmado para Senador")
                    voto["S"] = "B"
                    break
            elif numero_s not in dict_candidatos.keys():
                anular = input("Candidato inexistente. Deseja anular o voto? [S/N]: ").upper()
                while anular not in 'SN':
                    print("Por favor, digite S para anular ou N para voltar e escolher um candidato.")
                    anular = input("Deseja anular o voto? [S/N]: ").upper()
                if anular == 'S':
                    print("Voto para Senador anulado")
                    voto["S"] = "N"
                    break
            elif dict_candidatos[numero_s]['Cargo'] != "S":
                print("Erro. Número do Senador deve ter 3 dígitos")
            elif dict_eleitores[titulo_eleitor]['UF'] != dict_candidatos[numero_s]['UF']:
                anular = input("Candidato de outro estado. Deseja anular o voto? [S/N]: ").upper()
                while anular not in 'SN':
                    print("Por favor, digite S para anular ou N para voltar e escolher um candidato.")
                    anular = input("Candidato de outro estado. Deseja anular o voto? [S/N]: ").upper()
                if anular == 'S':
                    print("Voto para Senador anulado")
                    voto["S"] = "N"
                    break
            elif numero_s in dict_candidatos.keys():
                confirma = input(
                    f"Confirma voto no candidato {dict_candidatos[numero_s]['Nome']} | {dict_candidatos[numero_s]['Partido']}? [S/N]: ").upper()
                while confirma not in 'SN':
                    print("Por favor, digite S para confirmar ou N para escolher outro candidato.")
                    confirma = input(
                        f"Confirma voto no candidato {dict_candidatos[numero_s]['Nome']} | {dict_candidatos[numero_s]['Partido']}? [S/N]: ").upper()
                if confirma == 'S':
                    print(
                        f"Voto confirmado no candidato {dict_candidatos[numero_s]['Nome']} | {dict_candidatos[numero_s]['Partido']}")
                    voto["S"] = numero_s
                    break

        # inicia a votação para Governador
        while True:
            numero_g = input("\nInforme o voto para Governador: ")
            if numero_g in "Bb":
                em_branco = input("Voto em Branco. Confirma? [S/N]: ").upper()
                while em_branco not in "SN" or em_branco == '':
                    print("Por favor, digite S para votar em branco ou N para voltar e escolher um candidato.")
                    em_branco = input("Voto em Branco. Confirma? [S/N]: ").upper()
                if em_branco == "S":
                    print("Voto em branco confirmado para Governador")
                    voto["G"] = "B"
                    break
            elif numero_g not in dict_candidatos.keys():
                anular = input("Candidato inexistente. Deseja anular o voto? [S/N]: ").upper()
                while anular not in 'SN':
                    print("Por favor, digite S para anular ou N para voltar e escolher um candidato.")
                    anular = input("Deseja anular o voto? [S/N]: ").upper()
                if anular == 'S':
                    print("Voto para Governador anulado")
                    voto["G"] = "N"
                    break
            elif dict_candidatos[numero_g]['Cargo'] != "G":
                print("Erro. Número do Governador deve ter 2 dígitos")
            elif dict_eleitores[titulo_eleitor]['UF'] != dict_candidatos[numero_g]['UF']:
                anular = input("Candidato de outro estado. Deseja anular o voto? [S/N]: ").upper()
                while anular not in 'SN':
                    print("Por favor, digite S para anular ou N para voltar e escolher um candidato.")
                    anular = input("Candidato de outro estado. Deseja anular o voto? [S/N]: ").upper()
                if anular == 'S':
                    print("Voto para Governador anulado")
                    voto["G"] = "N"
                    break
            elif numero_g in dict_candidatos.keys():
                confirma = input(
                    f"Confirma voto no candidato {dict_candidatos[numero_g]['Nome']} | {dict_candidatos[numero_g]['Partido']}? [S/N]: ").upper()
                while confirma not in 'SN':
                    print("Por favor, digite S para confirmar ou N para escolher outro candidato.")
                    confirma = input(
                        f"Confirma voto no candidato {dict_candidatos[numero_g]['Nome']} | {dict_candidatos[numero_g]['Partido']}? [S/N]: ").upper()
                if confirma == 'S':
                    print(
                        f"Voto confirmado no candidato {dict_candidatos[numero_g]['Nome']} | {dict_candidatos[numero_g]['Partido']}")
                    voto["G"] = numero_g
                    break

        while True:
            # votação para Presidente ocorre da mesma forma que as anteriores, mas a diferença é que
            # não possui verificação de UF
            numero_p = input("\nInforme o voto para Presidente: ")
            if numero_p in "Bb":
                em_branco = input("Voto em Branco. Confirma? [S/N]: ").upper()
                while em_branco not in "SN" or em_branco == '':
                    print("Por favor, digite S para votar em branco ou N para voltar e escolher um candidato.")
                    em_branco = input("Voto em Branco. Confirma? [S/N]: ").upper()
                if em_branco == "S":
                    print("Voto em branco confirmado para Presidente")
                    voto["P"] = "B"
                    break
            elif numero_p not in dict_candidatos.keys():
                anular = input("Candidato inexistente. Deseja anular o voto? [S/N]: ").upper()
                while anular not in 'SN':
                    print("Por favor, digite S para anular ou N para voltar e escolher um candidato.")
                    anular = input("Deseja anular o voto? [S/N]: ").upper()
                if anular == 'S':
                    print("Voto para Presidente anulado")
                    voto["P"] = "N"
                    break
            elif dict_candidatos[numero_p]['Cargo'] != "P":
                print("Erro. Número do Presidente deve ter 2 dígitos")
            elif numero_p in dict_candidatos.keys():
                confirma = input(
                    f"Confirma voto no candidato {dict_candidatos[numero_p]['Nome']} | {dict_candidatos[numero_p]['Partido']}? [S/N]: ").upper()
                while confirma not in 'SN':
                    print("Por favor, digite S para confirmar ou N para escolher outro candidato.")
                    confirma = input(
                        f"Confirma voto no candidato {dict_candidatos[numero_p]['Nome']} | {dict_candidatos[numero_p]['Partido']}? [S/N]: ").upper()
                if confirma == 'S':
                    print(
                        f"Voto confirmado no candidato {dict_candidatos[numero_p]['Nome']} | {dict_candidatos[numero_p]['Partido']}")
                    voto["P"] = numero_p
                    break

        # abre o arquivo binário e salva nele o dicionário com os votos do eleitor atual
        with open("votos.bin", "ab") as votos_bin:
            pickle.dump(voto, votos_bin)

        # apaga o eleitor do dicionario dict_eleitores para que não possa ser possível votar novamente
        del dict_eleitores[titulo_eleitor]

        print('\n-=-=-= FIM =-=-=-')
        beep.play()
        pygame.time.wait(int(beep.get_length() * 1000))

        # pergunta se deseja registrar um novo voto
        print("\nREGISTRAR NOVO VOTO? [S/N]: ")
        novo_voto = input(
            "S = Inicia a votação com outro eleitor\nN = Finaliza a urna e volta ao menu principal (não será possível votar novamente)\n").upper()
        while novo_voto not in "SN" or novo_voto == "":
            novo_voto = input(
                "Por favor, digite S para registrar um novo voto ou N para voltar ao menu principal: ").upper()
        # se a opção for "N", retorna para o menu principal
        # a variável votacao_finalizada recebe o valor True, e será usada para não permitir iniciar a
        # votação novamente, e também para conceder acesso aos menus 4, 5 e 6
        if novo_voto == 'N':
            votacao_finalizada = True
            return votacao_finalizada


def apurar_votos():
    # dicionários para contabilizar os votos
    # separados por estado para poder calcular a porcentagem de
    # votos recebida por cada candidato no seu respectivo estado
    contagem_votos_f = {}
    contagem_votos_f_mg = {}
    contagem_votos_f_sp = {}
    contagem_votos_f_rj = {}
    contagem_votos_f_es = {}
    contagem_votos_e = {}
    contagem_votos_e_mg = {}
    contagem_votos_e_sp = {}
    contagem_votos_e_rj = {}
    contagem_votos_e_es = {}
    contagem_votos_s = {}
    contagem_votos_s_mg = {}
    contagem_votos_s_sp = {}
    contagem_votos_s_rj = {}
    contagem_votos_s_es = {}
    contagem_votos_g = {}
    contagem_votos_g_mg = {}
    contagem_votos_g_sp = {}
    contagem_votos_g_rj = {}
    contagem_votos_g_es = {}
    contagem_votos_p = {}
    contagem_brancos = {}
    contagem_nulos = {}

    # lista que vai receber cada voto registrado no arquivo binário
    lista_de_votos = []

    # abre o arquivo binário para ler os votos de cada eleitor e colocar na lista "lista_de_votos"
    with open("votos.bin", "rb") as votos_bin:
        while True:
            try:
                lista_de_votos.append(pickle.load(votos_bin))
            except EOFError:
                break

    # itera sobre a lista de votos de cada eleitor para adicionar cada voto em um dicionário adequado
    for voto in lista_de_votos:
        # contabiliza votos para Deputado Federal
        # se não for nulo ou branco, contabiliza o voto no dicionario contagem_votos_f (para contagem geral), e também
        # no dicionário do seu respectivo estado
        if voto['F'] not in ['N', 'B']:
            if voto['UF'] == 'MG':
                contagem_votos_f_mg[voto['F']] = contagem_votos_f.get(voto['F'], 0) + 1
            elif voto['UF'] == 'SP':
                contagem_votos_f_sp[voto['F']] = contagem_votos_f.get(voto['F'], 0) + 1
            elif voto['UF'] == 'RJ':
                contagem_votos_f_rj[voto['F']] = contagem_votos_f.get(voto['F'], 0) + 1
            elif voto['UF'] == 'ES':
                contagem_votos_f_es[voto['F']] = contagem_votos_f.get(voto['F'], 0) + 1
            contagem_votos_f[voto['F']] = contagem_votos_f.get(voto['F'], 0) + 1
        elif voto['F'] == 'B':
            contagem_brancos['F'] = contagem_brancos.get('F', 0) + 1
        elif voto['F'] == 'N':
            contagem_nulos['F'] = contagem_nulos.get('F', 0) + 1

        # contabiliza votos para Deputado Estadual
        if voto['E'] not in ['N', 'B']:
            if voto['UF'] == 'MG':
                contagem_votos_e_mg[voto['E']] = contagem_votos_e.get(voto['E'], 0) + 1
            elif voto['UF'] == 'SP':
                contagem_votos_e_sp[voto['E']] = contagem_votos_e.get(voto['E'], 0) + 1
            elif voto['UF'] == 'RJ':
                contagem_votos_e_rj[voto['E']] = contagem_votos_e.get(voto['E'], 0) + 1
            elif voto['UF'] == 'ES':
                contagem_votos_e_es[voto['E']] = contagem_votos_e.get(voto['E'], 0) + 1
            contagem_votos_e[voto['E']] = contagem_votos_e.get(voto['E'], 0) + 1
        elif voto['E'] == 'B':
            contagem_brancos['E'] = contagem_brancos.get('E', 0) + 1
        elif voto['E'] == 'N':
            contagem_nulos['E'] = contagem_nulos.get('E', 0) + 1

        # contabiliza votos para Senador
        if voto['S'] not in ['N', 'B']:
            if voto['UF'] == 'MG':
                contagem_votos_s_mg[voto['S']] = contagem_votos_s.get(voto['S'], 0) + 1
            elif voto['UF'] == 'SP':
                contagem_votos_s_sp[voto['S']] = contagem_votos_s.get(voto['S'], 0) + 1
            elif voto['UF'] == 'RJ':
                contagem_votos_s_rj[voto['S']] = contagem_votos_s.get(voto['S'], 0) + 1
            elif voto['UF'] == 'ES':
                contagem_votos_s_es[voto['S']] = contagem_votos_s.get(voto['S'], 0) + 1
            contagem_votos_s[voto['S']] = contagem_votos_s.get(voto['S'], 0) + 1
        elif voto['S'] == 'B':
            contagem_brancos['S'] = contagem_brancos.get('S', 0) + 1
        elif voto['S'] == 'N':
            contagem_nulos['S'] = contagem_nulos.get('S', 0) + 1

        # contabiliza votos para Governador
        if voto['G'] not in ['N', 'B']:
            if voto['UF'] == 'MG':
                contagem_votos_g_mg[voto['G']] = contagem_votos_g.get(voto['G'], 0) + 1
            elif voto['UF'] == 'SP':
                contagem_votos_g_sp[voto['G']] = contagem_votos_g.get(voto['G'], 0) + 1
            elif voto['UF'] == 'RJ':
                contagem_votos_g_rj[voto['G']] = contagem_votos_g.get(voto['G'], 0) + 1
            elif voto['UF'] == 'ES':
                contagem_votos_g_es[voto['G']] = contagem_votos_g.get(voto['G'], 0) + 1
            contagem_votos_g[voto['G']] = contagem_votos_g.get(voto['G'], 0) + 1
        elif voto['G'] == 'B':
            contagem_brancos['G'] = contagem_brancos.get('G', 0) + 1
        elif voto['G'] == 'N':
            contagem_nulos['G'] = contagem_nulos.get('G', 0) + 1

        # contabiliza votos para Presidente
        if voto['P'] not in ['N', 'B']:
            contagem_votos_p[voto['P']] = contagem_votos_p.get(voto['P'], 0) + 1
        elif voto['P'] == 'B':
            contagem_brancos['P'] = contagem_brancos.get('P', 0) + 1
        elif voto['P'] == 'N':
            contagem_nulos['P'] = contagem_nulos.get('P', 0) + 1

    votos = {'F': contagem_votos_f, 'E': contagem_votos_e, 'S': contagem_votos_s, 'G': contagem_votos_g,
             'P': contagem_votos_p}
    # dicionário vazio que vai receber os votos separados por cargo e estado
    dict_votos = {}
    # adiciona os dicionários contendo o total de votos de cada
    # candidato (separados por estado) e os dicionários contendo brancos e nulos ao dicionário dict_votos
    dict_votos['contagem_votos_f'] = contagem_votos_f
    dict_votos['contagem_votos_f_mg'] = contagem_votos_f_mg
    dict_votos['contagem_votos_f_sp'] = contagem_votos_f_sp
    dict_votos['contagem_votos_f_rj'] = contagem_votos_f_rj
    dict_votos['contagem_votos_f_es'] = contagem_votos_f_es
    dict_votos['contagem_votos_e'] = contagem_votos_e
    dict_votos['contagem_votos_e_mg'] = contagem_votos_e_mg
    dict_votos['contagem_votos_e_sp'] = contagem_votos_e_sp
    dict_votos['contagem_votos_e_rj'] = contagem_votos_e_rj
    dict_votos['contagem_votos_e_es'] = contagem_votos_e_es
    dict_votos['contagem_votos_s'] = contagem_votos_s
    dict_votos['contagem_votos_s_mg'] = contagem_votos_s_mg
    dict_votos['contagem_votos_s_sp'] = contagem_votos_s_sp
    dict_votos['contagem_votos_s_rj'] = contagem_votos_s_rj
    dict_votos['contagem_votos_s_es'] = contagem_votos_s_es
    dict_votos['contagem_votos_g'] = contagem_votos_g
    dict_votos['contagem_votos_g_mg'] = contagem_votos_g_mg
    dict_votos['contagem_votos_g_sp'] = contagem_votos_g_sp
    dict_votos['contagem_votos_g_rj'] = contagem_votos_g_rj
    dict_votos['contagem_votos_g_es'] = contagem_votos_g_es
    dict_votos['contagem_votos_p'] = contagem_votos_p
    dict_votos['contagem_brancos'] = contagem_brancos
    dict_votos['contagem_nulos'] = contagem_nulos

    # faz a soma dos votos separados por por cargo e estado, para calcular a porcentagem de cada candidato no seu estado
    # soma para o cargo de Deputado Federal
    soma_f = 0
    for i in dict_votos['contagem_votos_f'].values():
        soma_f += i
    dict_votos['soma_f'] = soma_f
    soma_f_mg = 0
    for i in dict_votos['contagem_votos_f_mg'].values():
        soma_f_mg += i
    dict_votos['soma_f_mg'] = soma_f_mg
    soma_f_sp = 0
    for i in dict_votos['contagem_votos_f_sp'].values():
        soma_f_sp += i
    dict_votos['soma_f_sp'] = soma_f_sp
    soma_f_rj = 0
    for i in dict_votos['contagem_votos_f_rj'].values():
        soma_f_rj += i
    dict_votos['soma_f_rj'] = soma_f_rj
    soma_f_es = 0
    for i in dict_votos['contagem_votos_f_es'].values():
        soma_f_es += i
    dict_votos['soma_f_es'] = soma_f_es

    # soma para o cargo de Deputado Estadual
    soma_e = 0
    for i in dict_votos['contagem_votos_e'].values():
        soma_e += i
    dict_votos['soma_e'] = soma_e
    soma_e_mg = 0
    for i in dict_votos['contagem_votos_e_mg'].values():
        soma_e_mg += i
    dict_votos['soma_e_mg'] = soma_e_mg
    soma_e_sp = 0
    for i in dict_votos['contagem_votos_e_sp'].values():
        soma_e_sp += i
    dict_votos['soma_e_sp'] = soma_e_sp
    soma_e_rj = 0
    for i in dict_votos['contagem_votos_e_rj'].values():
        soma_e_rj += i
    dict_votos['soma_e_rj'] = soma_e_rj
    soma_e_es = 0
    for i in dict_votos['contagem_votos_e_es'].values():
        soma_e_es += i
    dict_votos['soma_e_es'] = soma_e_es

    # soma para o cargo de Senador
    soma_s = 0
    for i in dict_votos['contagem_votos_s'].values():
        soma_s += i
    dict_votos['soma_s'] = soma_s
    soma_s_mg = 0
    for i in dict_votos['contagem_votos_s_mg'].values():
        soma_s_mg += i
    dict_votos['soma_s_mg'] = soma_s_mg
    soma_s_sp = 0
    for i in dict_votos['contagem_votos_s_sp'].values():
        soma_s_sp += i
    dict_votos['soma_s_sp'] = soma_s_sp
    soma_s_rj = 0
    for i in dict_votos['contagem_votos_s_rj'].values():
        soma_s_rj += i
    dict_votos['soma_s_rj'] = soma_s_rj
    soma_s_es = 0
    for i in dict_votos['contagem_votos_s_es'].values():
        soma_s_es += i
    dict_votos['soma_s_es'] = soma_s_es

    # soma para o cargo de Governador
    soma_g = 0
    for i in dict_votos['contagem_votos_g'].values():
        soma_g += i
    dict_votos['soma_g'] = soma_g
    soma_g_mg = 0
    for i in dict_votos['contagem_votos_g_mg'].values():
        soma_g_mg += i
    dict_votos['soma_g_mg'] = soma_g_mg
    soma_g_sp = 0
    for i in dict_votos['contagem_votos_g_sp'].values():
        soma_g_sp += i
    dict_votos['soma_g_sp'] = soma_g_sp
    soma_g_rj = 0
    for i in dict_votos['contagem_votos_g_rj'].values():
        soma_g_rj += i
    dict_votos['soma_g_rj'] = soma_g_rj
    soma_g_es = 0
    for i in dict_votos['contagem_votos_g_es'].values():
        soma_g_es += i
    dict_votos['soma_g_es'] = soma_g_es

    # soma para o cargo de Presidente
    soma_p = 0
    for i in dict_votos['contagem_votos_p'].values():
        soma_p += i
    dict_votos['soma_p'] = soma_p

    # soma para votos brancos
    soma_brancos = 0
    for i in dict_votos['contagem_brancos'].values():
        soma_brancos += i
    dict_votos['soma_brancos'] = soma_brancos

    # soma para votos nulos
    soma_nulos = 0
    for i in dict_votos['contagem_nulos'].values():
        soma_nulos += i
    dict_votos['soma_nulos'] = soma_nulos

    # soma para votos nominais
    votos_nominais = soma_f + soma_e + soma_s + soma_g + soma_p
    dict_votos['Nominais'] = votos_nominais

    print()
    print("REALIZANDO APURAÇÃO DOS VOTOS...")
    sleep(1)
    print()
    print("-=" * 30)
    print("APURAÇÃO REALIZADA COM SUCESSO! VOLTANDO AO MENU PRINCIPAL...")
    print("SELECIONE A OPÇÃO 5 PARA MOSTRAR OS RESULTADOS.")
    print("-=" * 30)
    sleep(3)

    # a variável ok_apuracao com valor "True" é usada para conceder acesso aos menus 5 e 6
    ok_apuracao = True

    return dict_votos, votos, ok_apuracao


def mostrar_resultados(dict_votos):
    # a função mostrar resultados EXIBE os resultados na tela
    # logo abaixo existe uma chamada para outra função salvar_resultados
    # a função salvar_resultados SALVA os resultados no arquivo resultados.txt
    # a saída é a mesma tanto na tela quanto no arquivo resultados.txt
    salvar_resultados()
    print()
    print("GERANDO RESULTADOS...")
    sleep(1)
    print()
    print("-=" * 6)
    print("RESULTADOS:")
    print("-=" * 6)
    print()
    print(f"Eleitores aptos: {eleitores_aptos}")
    print(f"Total de Votos Nominais: {dict_votos['Nominais']}")
    print(f"Brancos: {dict_votos['soma_brancos']}")
    print(f"Nulos: {dict_votos['soma_nulos']}")
    print()

    # mostra a tabela de resultados para cada candidato a Deputado Federal
    for k in dict_votos['contagem_votos_f'].keys():
        if dict_candidatos[k]['UF'] == 'MG':
            porcentagem_f_mg = dict_votos['contagem_votos_f'][k] / dict_votos['soma_f_mg'] * 100
            print(
                f"Candidato: {dict_candidatos[k]['Nome']:<20}| Cargo: Deputado Federal \t| Estado: {dict_candidatos[k]['UF']:<6}| Votos: {dict_votos['contagem_votos_f'][k]} ({porcentagem_f_mg:.2f}%)")
        elif dict_candidatos[k]['UF'] == 'SP':
            porcentagem_f_sp = dict_votos['contagem_votos_f'][k] / dict_votos['soma_f_sp'] * 100
            print(
                f"Candidato: {dict_candidatos[k]['Nome']:<20}| Cargo: Deputado Federal \t| Estado: {dict_candidatos[k]['UF']:<6}| Votos: {dict_votos['contagem_votos_f'][k]} ({porcentagem_f_sp:.2f}%)")
        elif dict_candidatos[k]['UF'] == 'RJ':
            porcentagem_f_rj = dict_votos['contagem_votos_f'][k] / dict_votos['soma_f_rj'] * 100
            print(
                f"Candidato: {dict_candidatos[k]['Nome']:<20}| Cargo: Deputado Federal \t| Estado: {dict_candidatos[k]['UF']:<6}| Votos: {dict_votos['contagem_votos_f'][k]} ({porcentagem_f_rj:.2f}%)")
        elif dict_candidatos[k]['UF'] == 'ES':
            porcentagem_f_es = dict_votos['contagem_votos_f'][k] / dict_votos['soma_f_es'] * 100
            print(
                f"Candidato: {dict_candidatos[k]['Nome']:<20}| Cargo: Deputado Federal \t| Estado: {dict_candidatos[k]['UF']:<6}| Votos: {dict_votos['contagem_votos_f'][k]} ({porcentagem_f_es:.2f}%)")

    # mostra a tabela de resultados para cada candidato a Deputado Estadual
    for k in dict_votos['contagem_votos_e'].keys():
        if dict_candidatos[k]['UF'] == 'MG':
            porcentagem_e_mg = dict_votos['contagem_votos_e'][k] / dict_votos['soma_e_mg'] * 100
            print(
                f"Candidato: {dict_candidatos[k]['Nome']:<20}| Cargo: Deputado Estadual \t| Estado: {dict_candidatos[k]['UF']:<6}| Votos: {dict_votos['contagem_votos_e'][k]} ({porcentagem_e_mg:.2f}%)")
        elif dict_candidatos[k]['UF'] == 'SP':
            porcentagem_e_sp = dict_votos['contagem_votos_e'][k] / dict_votos['soma_e_sp'] * 100
            print(
                f"Candidato: {dict_candidatos[k]['Nome']:<20}| Cargo: Deputado Estadual \t| Estado: {dict_candidatos[k]['UF']:<6}| Votos: {dict_votos['contagem_votos_e'][k]} ({porcentagem_e_sp:.2f}%)")
        elif dict_candidatos[k]['UF'] == 'RJ':
            porcentagem_e_rj = dict_votos['contagem_votos_e'][k] / dict_votos['soma_e_rj'] * 100
            print(
                f"Candidato: {dict_candidatos[k]['Nome']:<20}| Cargo: Deputado Estadual \t| Estado: {dict_candidatos[k]['UF']:<6}| Votos: {dict_votos['contagem_votos_e'][k]} ({porcentagem_e_rj:.2f}%)")
        elif dict_candidatos[k]['UF'] == 'ES':
            porcentagem_e_es = dict_votos['contagem_votos_e'][k] / dict_votos['soma_e_es'] * 100
            print(
                f"Candidato: {dict_candidatos[k]['Nome']:<20}| Cargo: Deputado Estadual \t| Estado: {dict_candidatos[k]['UF']:<6}| Votos: {dict_votos['contagem_votos_e'][k]} ({porcentagem_e_es:.2f}%)")

    # mostra a tabela de resultados para cada candidato a Senador
    for k in dict_votos['contagem_votos_s'].keys():
        if dict_candidatos[k]['UF'] == 'MG':
            porcentagem_s_mg = dict_votos['contagem_votos_s'][k] / dict_votos['soma_s_mg'] * 100
            print(
                f"Candidato: {dict_candidatos[k]['Nome']:<20}| Cargo: Senador \t\t\t| Estado: {dict_candidatos[k]['UF']:<6}| Votos: {dict_votos['contagem_votos_s'][k]} ({porcentagem_s_mg:.2f}%)")
        elif dict_candidatos[k]['UF'] == 'SP':
            porcentagem_s_sp = dict_votos['contagem_votos_s'][k] / dict_votos['soma_s_sp'] * 100
            print(
                f"Candidato: {dict_candidatos[k]['Nome']:<20}| Cargo: Senador \t\t\t| Estado: {dict_candidatos[k]['UF']:<6}| Votos: {dict_votos['contagem_votos_s'][k]} ({porcentagem_s_sp:.2f}%)")
        elif dict_candidatos[k]['UF'] == 'RJ':
            porcentagem_s_rj = dict_votos['contagem_votos_s'][k] / dict_votos['soma_s_rj'] * 100
            print(
                f"Candidato: {dict_candidatos[k]['Nome']:<20}| Cargo: Senador \t\t\t| Estado: {dict_candidatos[k]['UF']:<6}| Votos: {dict_votos['contagem_votos_s'][k]} ({porcentagem_s_rj:.2f}%)")
        elif dict_candidatos[k]['UF'] == 'ES':
            porcentagem_s_es = dict_votos['contagem_votos_s'][k] / dict_votos['soma_s_es'] * 100
            print(
                f"Candidato: {dict_candidatos[k]['Nome']:<20}| Cargo: Senador \t\t\t| Estado: {dict_candidatos[k]['UF']:<6}| Votos: {dict_votos['contagem_votos_s'][k]} ({porcentagem_s_es:.2f}%)")

    # mostra a tabela de resultados para cada candidato a Governador
    for k in dict_votos['contagem_votos_g'].keys():
        if dict_candidatos[k]['UF'] == 'MG':
            porcentagem_g_mg = dict_votos['contagem_votos_g'][k] / dict_votos['soma_g_mg'] * 100
            print(
                f"Candidato: {dict_candidatos[k]['Nome']:<20}| Cargo: Governador \t\t\t| Estado: {dict_candidatos[k]['UF']:<6}| Votos: {dict_votos['contagem_votos_g'][k]} ({porcentagem_g_mg:.2f}%)")
        elif dict_candidatos[k]['UF'] == 'SP':
            porcentagem_g_sp = dict_votos['contagem_votos_g'][k] / dict_votos['soma_g_sp'] * 100
            print(
                f"Candidato: {dict_candidatos[k]['Nome']:<20}| Cargo: Governador \t\t\t| Estado: {dict_candidatos[k]['UF']:<6}| Votos: {dict_votos['contagem_votos_g'][k]} ({porcentagem_g_sp:.2f}%)")
        elif dict_candidatos[k]['UF'] == 'RJ':
            porcentagem_g_rj = dict_votos['contagem_votos_g'][k] / dict_votos['soma_g_rj'] * 100
            print(
                f"Candidato: {dict_candidatos[k]['Nome']:<20}| Cargo: Governador \t\t\t| Estado: {dict_candidatos[k]['UF']:<6}| Votos: {dict_votos['contagem_votos_g'][k]} ({porcentagem_g_rj:.2f}%)")
        elif dict_candidatos[k]['UF'] == 'ES':
            porcentagem_g_es = dict_votos['contagem_votos_g'][k] / dict_votos['soma_g_es'] * 100
            print(
                f"Candidato: {dict_candidatos[k]['Nome']:<20}| Cargo: Governador \t\t\t| Estado: {dict_candidatos[k]['UF']:<6}| Votos: {dict_votos['contagem_votos_g'][k]} ({porcentagem_g_es:.2f}%)")

    # mostra a tabela de resultados para cada candidato a Presidente
    for k in dict_votos['contagem_votos_p'].keys():
        porcentagem_p = dict_votos['contagem_votos_p'][k] / dict_votos['soma_p'] * 100
        print(
            f"Candidato: {dict_candidatos[k]['Nome']:<20}| Cargo: Presidente \t\t\t| Estado: {dict_candidatos[k]['UF']:<6}| Votos: {dict_votos['contagem_votos_p'][k]} ({porcentagem_p:.2f}%)")

    print()
    print("-=" * 32)
    print("CANDIDATOS QUE NÃO RECEBERAM VOTOS NÃO APARECEM NESSA LISTAGEM.")
    print("O RESULTADO FOI SALVO NO ARQUIVO RESULTADOS.TXT")
    print("-=" * 32)

    # a variável ok_resultados com valor "True" é usada para conceder acesso ao menu 6
    ok_resultados = True
    return ok_resultados


def salvar_resultados():
    # a função salvar_resultados SALVA os resultados no arquivo resultados.txt
    # é diferete da função mostrar_resultados que só EXIBE os resultados na tela
    # a saída é a mesma tanto na tela quanto no arquivo resultados.txt
    resultados = open("boletim.txt", "w")
    resultados.write("-=" * 5)
    resultados.write("\nRESULTADOS:\n")
    resultados.write("-=" * 5)
    resultados.write("\n\n")
    resultados.write(f"Eleitores aptos: {eleitores_aptos}")
    resultados.write(f"\nTotal de Votos Nominais: {dict_votos['Nominais']}")
    resultados.write(f"\nBrancos: {dict_votos['soma_brancos']}")
    resultados.write(f"\nNulos: {dict_votos['soma_nulos']}")
    resultados.write("\n")

    # salva a tabela de resultados para cada candidato a Deputado Federal
    for k in dict_votos['contagem_votos_f'].keys():
        if dict_candidatos[k]['UF'] == 'MG':
            porcentagem_f_mg = dict_votos['contagem_votos_f'][k] / dict_votos['soma_f_mg'] * 100
            resultados.write(
                f"\nCandidato: {dict_candidatos[k]['Nome']:<20}| Cargo: Deputado Federal \t| Estado: {dict_candidatos[k]['UF']:<6}| Votos: {dict_votos['contagem_votos_f'][k]} ({porcentagem_f_mg:.2f}%)")
        elif dict_candidatos[k]['UF'] == 'SP':
            porcentagem_f_sp = dict_votos['contagem_votos_f'][k] / dict_votos['soma_f_sp'] * 100
            resultados.write(
                f"\nCandidato: {dict_candidatos[k]['Nome']:<20}| Cargo: Deputado Federal \t| Estado: {dict_candidatos[k]['UF']:<6}| Votos: {dict_votos['contagem_votos_f'][k]} ({porcentagem_f_sp:.2f}%)")
        elif dict_candidatos[k]['UF'] == 'RJ':
            porcentagem_f_rj = dict_votos['contagem_votos_f'][k] / dict_votos['soma_f_rj'] * 100
            resultados.write(
                f"\nCandidato: {dict_candidatos[k]['Nome']:<20}| Cargo: Deputado Federal \t| Estado: {dict_candidatos[k]['UF']:<6}| Votos: {dict_votos['contagem_votos_f'][k]} ({porcentagem_f_rj:.2f}%)")
        elif dict_candidatos[k]['UF'] == 'ES':
            porcentagem_f_es = dict_votos['contagem_votos_f'][k] / dict_votos['soma_f_es'] * 100
            resultados.write(
                f"\nCandidato: {dict_candidatos[k]['Nome']:<20}| Cargo: Deputado Federal \t| Estado: {dict_candidatos[k]['UF']:<6}| Votos: {dict_votos['contagem_votos_f'][k]} ({porcentagem_f_es:.2f}%)")

    # salva a tabela de resultados para cada candidato a Deputado Estadual
    for k in dict_votos['contagem_votos_e'].keys():
        if dict_candidatos[k]['UF'] == 'MG':
            porcentagem_e_mg = dict_votos['contagem_votos_e'][k] / dict_votos['soma_e_mg'] * 100
            resultados.write(
                f"\nCandidato: {dict_candidatos[k]['Nome']:<20}| Cargo: Deputado Estadual \t| Estado: {dict_candidatos[k]['UF']:<6}| Votos: {dict_votos['contagem_votos_e'][k]} ({porcentagem_e_mg:.2f}%)")
        elif dict_candidatos[k]['UF'] == 'SP':
            porcentagem_e_sp = dict_votos['contagem_votos_e'][k] / dict_votos['soma_e_sp'] * 100
            resultados.write(
                f"\nCandidato: {dict_candidatos[k]['Nome']:<20}| Cargo: Deputado Estadual \t| Estado: {dict_candidatos[k]['UF']:<6}| Votos: {dict_votos['contagem_votos_e'][k]} ({porcentagem_e_sp:.2f}%)")
        elif dict_candidatos[k]['UF'] == 'RJ':
            porcentagem_e_rj = dict_votos['contagem_votos_e'][k] / dict_votos['soma_e_rj'] * 100
            resultados.write(
                f"\nCandidato: {dict_candidatos[k]['Nome']:<20}| Cargo: Deputado Estadual \t| Estado: {dict_candidatos[k]['UF']:<6}| Votos: {dict_votos['contagem_votos_e'][k]} ({porcentagem_e_rj:.2f}%)")
        elif dict_candidatos[k]['UF'] == 'ES':
            porcentagem_e_es = dict_votos['contagem_votos_e'][k] / dict_votos['soma_e_es'] * 100
            resultados.write(
                f"\nCandidato: {dict_candidatos[k]['Nome']:<20}| Cargo: Deputado Estadual \t| Estado: {dict_candidatos[k]['UF']:<6}| Votos: {dict_votos['contagem_votos_e'][k]} ({porcentagem_e_es:.2f}%)")

    # salva a tabela de resultados para cada candidato a Senador
    for k in dict_votos['contagem_votos_s'].keys():
        if dict_candidatos[k]['UF'] == 'MG':
            porcentagem_s_mg = dict_votos['contagem_votos_s'][k] / dict_votos['soma_s_mg'] * 100
            resultados.write(
                f"\nCandidato: {dict_candidatos[k]['Nome']:<20}| Cargo: Senador \t\t\t| Estado: {dict_candidatos[k]['UF']:<6}| Votos: {dict_votos['contagem_votos_s'][k]} ({porcentagem_s_mg:.2f}%)")
        elif dict_candidatos[k]['UF'] == 'SP':
            porcentagem_s_sp = dict_votos['contagem_votos_s'][k] / dict_votos['soma_s_sp'] * 100
            resultados.write(
                f"\nCandidato: {dict_candidatos[k]['Nome']:<20}| Cargo: Senador \t\t\t| Estado: {dict_candidatos[k]['UF']:<6}| Votos: {dict_votos['contagem_votos_s'][k]} ({porcentagem_s_sp:.2f}%)")
        elif dict_candidatos[k]['UF'] == 'RJ':
            porcentagem_s_rj = dict_votos['contagem_votos_s'][k] / dict_votos['soma_s_rj'] * 100
            resultados.write(
                f"\nCandidato: {dict_candidatos[k]['Nome']:<20}| Cargo: Senador \t\t\t| Estado: {dict_candidatos[k]['UF']:<6}| Votos: {dict_votos['contagem_votos_s'][k]} ({porcentagem_s_rj:.2f}%)")
        elif dict_candidatos[k]['UF'] == 'ES':
            porcentagem_s_es = dict_votos['contagem_votos_s'][k] / dict_votos['soma_s_es'] * 100
            resultados.write(
                f"\nCandidato: {dict_candidatos[k]['Nome']:<20}| Cargo: Senador \t\t\t| Estado: {dict_candidatos[k]['UF']:<6}| Votos: {dict_votos['contagem_votos_s'][k]} ({porcentagem_s_es:.2f}%)")

    # salva a tabela de resultados para cada candidato a Governador
    for k in dict_votos['contagem_votos_g'].keys():
        if dict_candidatos[k]['UF'] == 'MG':
            porcentagem_g_mg = dict_votos['contagem_votos_g'][k] / dict_votos['soma_g_mg'] * 100
            resultados.write(
                f"\nCandidato: {dict_candidatos[k]['Nome']:<20}| Cargo: Governador \t\t\t| Estado: {dict_candidatos[k]['UF']:<6}| Votos: {dict_votos['contagem_votos_g'][k]} ({porcentagem_g_mg:.2f}%)")
        elif dict_candidatos[k]['UF'] == 'SP':
            porcentagem_g_sp = dict_votos['contagem_votos_g'][k] / dict_votos['soma_g_sp'] * 100
            resultados.write(
                f"\nCandidato: {dict_candidatos[k]['Nome']:<20}| Cargo: Governador \t\t\t| Estado: {dict_candidatos[k]['UF']:<6}| Votos: {dict_votos['contagem_votos_g'][k]} ({porcentagem_g_sp:.2f}%)")
        elif dict_candidatos[k]['UF'] == 'RJ':
            porcentagem_g_rj = dict_votos['contagem_votos_g'][k] / dict_votos['soma_g_rj'] * 100
            resultados.write(
                f"\nCandidato: {dict_candidatos[k]['Nome']:<20}| Cargo: Governador \t\t\t| Estado: {dict_candidatos[k]['UF']:<6}| Votos: {dict_votos['contagem_votos_g'][k]} ({porcentagem_g_rj:.2f}%)")
        elif dict_candidatos[k]['UF'] == 'ES':
            porcentagem_g_es = dict_votos['contagem_votos_g'][k] / dict_votos['soma_g_es'] * 100
            resultados.write(
                f"\nCandidato: {dict_candidatos[k]['Nome']:<20}| Cargo: Governador \t\t\t| Estado: {dict_candidatos[k]['UF']:<6}| Votos: {dict_votos['contagem_votos_g'][k]} ({porcentagem_g_es:.2f}%)")

    # salva a tabela de resultados para cada candidato a Presidente
    for k in dict_votos['contagem_votos_p'].keys():
        porcentagem_p = dict_votos['contagem_votos_p'][k] / dict_votos['soma_p'] * 100
        resultados.write(
            f"\nCandidato: {dict_candidatos[k]['Nome']:<20}| Cargo: Presidente \t\t\t| Estado: {dict_candidatos[k]['UF']:<6}| Votos: {dict_votos['contagem_votos_p'][k]} ({porcentagem_p:.2f}%)")

    resultados.write("\n\n")
    resultados.write("-=" * 32)
    resultados.write("\nCANDIDATOS QUE NÃO RECEBERAM VOTOS NÃO APARECEM NESSA LISTAGEM.\n")
    resultados.write("-=" * 32)
    resultados.close()


def gera_grafico(titulo, votos, uf_candidatos):
    # cria o dicionário vazio dict_votos_grafico para receber as chaves e valores corretos de outros dicionários
    dict_votos_grafico = {}

    # AS CONDIÇÕES ABAIXO VERIFICAM SE HÁ VOTOS PARA OS CARGOS E ESTADOS SOLICITADOS

    # checa se existe algum voto para Deputado Federal em MG
    if titulo == "F" and uf_candidatos == 'MG':
        # se não existe, imprime a mensagem de erro
        if not votos['contagem_votos_f_mg']:
            print("Erro: Não há votos para candidatos a esse cargo nessa UF")
            sleep(1)
            return
        # se existe, adiciona no dicionário dict_votos_grafico os dados adequados que serão usados para gerar o gráfico
        else:
            dict_votos_grafico[titulo] = votos['contagem_votos_f_mg']
            numeros_candidato = list(dict_votos_grafico[titulo].keys())
            for i in numeros_candidato:
                numeros_candidato[numeros_candidato.index(i)] = dict_candidatos[i]["Nome"]
            quantidade_votos = list(dict_votos_grafico[titulo].values())
            titulo = "Apuração - Eleições para Deputado Federal - MG"

    elif titulo == "F" and uf_candidatos == 'SP':
        if not votos['contagem_votos_f_sp']:
            print("Erro: Não há votos para candidatos a esse cargo nessa UF")
            sleep(1)
            return
        else:
            dict_votos_grafico[titulo] = votos['contagem_votos_f_sp']
            numeros_candidato = list(dict_votos_grafico[titulo].keys())
            for i in numeros_candidato:
                numeros_candidato[numeros_candidato.index(i)] = dict_candidatos[i]["Nome"]
            quantidade_votos = list(dict_votos_grafico[titulo].values())
            titulo = "Apuração - Eleições para Deputado Federal - SP"

    elif titulo == "F" and uf_candidatos == 'RJ':
        if not votos['contagem_votos_f_rj']:
            print("Erro: Não há votos para candidatos a esse cargo nessa UF")
            sleep(1)
            return
        else:
            dict_votos_grafico[titulo] = votos['contagem_votos_f_rj']
            numeros_candidato = list(dict_votos_grafico[titulo].keys())
            for i in numeros_candidato:
                numeros_candidato[numeros_candidato.index(i)] = dict_candidatos[i]["Nome"]
            quantidade_votos = list(dict_votos_grafico[titulo].values())
            titulo = "Apuração - Eleições para Deputado Federal - RJ"

    elif titulo == "F" and uf_candidatos == 'ES':
        if not votos['contagem_votos_f_es']:
            print("Erro: Não há votos para candidatos a esse cargo nessa UF")
            sleep(1)
            return
        else:
            dict_votos_grafico[titulo] = votos['contagem_votos_f_es']
            numeros_candidato = list(dict_votos_grafico[titulo].keys())
            for i in numeros_candidato:
                numeros_candidato[numeros_candidato.index(i)] = dict_candidatos[i]["Nome"]
            quantidade_votos = list(dict_votos_grafico[titulo].values())
            titulo = "Apuração - Eleições para Deputado Federal - ES"

    elif titulo == "E" and uf_candidatos == 'MG':
        if not votos['contagem_votos_e_mg']:
            print("Erro: Não há votos para candidatos a esse cargo nessa UF")
            sleep(1)
            return
        else:
            dict_votos_grafico[titulo] = votos['contagem_votos_e_mg']
            numeros_candidato = list(dict_votos_grafico[titulo].keys())
            for i in numeros_candidato:
                numeros_candidato[numeros_candidato.index(i)] = dict_candidatos[i]["Nome"]
            quantidade_votos = list(dict_votos_grafico[titulo].values())
            titulo = "Apuração - Eleições para Deputado Estadual - MG"

    elif titulo == "E" and uf_candidatos == 'SP':
        if not votos['contagem_votos_e_sp']:
            print("Erro: Não há votos para candidatos a esse cargo nessa UF")
            sleep(1)
            return
        else:
            dict_votos_grafico[titulo] = votos['contagem_votos_e_sp']
            numeros_candidato = list(dict_votos_grafico[titulo].keys())
            for i in numeros_candidato:
                numeros_candidato[numeros_candidato.index(i)] = dict_candidatos[i]["Nome"]
            quantidade_votos = list(dict_votos_grafico[titulo].values())
            titulo = "Apuração - Eleições para Deputado Estadual - SP"

    elif titulo == "E" and uf_candidatos == 'RJ':
        if not votos['contagem_votos_e_rj']:
            print("Erro: Não há votos para candidatos a esse cargo nessa UF")
            sleep(1)
            return
        else:
            dict_votos_grafico[titulo] = votos['contagem_votos_e_rj']
            numeros_candidato = list(dict_votos_grafico[titulo].keys())
            for i in numeros_candidato:
                numeros_candidato[numeros_candidato.index(i)] = dict_candidatos[i]["Nome"]
            quantidade_votos = list(dict_votos_grafico[titulo].values())
            titulo = "Apuração - Eleições para Deputado Estadual - RJ"

    elif titulo == "E" and uf_candidatos == 'ES':
        if not votos['contagem_votos_e_es']:
            print("Erro: Não há votos para candidatos a esse cargo nessa UF")
            sleep(1)
            return
        else:
            dict_votos_grafico[titulo] = votos['contagem_votos_e_es']
            numeros_candidato = list(dict_votos_grafico[titulo].keys())
            for i in numeros_candidato:
                numeros_candidato[numeros_candidato.index(i)] = dict_candidatos[i]["Nome"]
            quantidade_votos = list(dict_votos_grafico[titulo].values())
            titulo = "Apuração - Eleições para Deputado Estadual - ES"

    elif titulo == "S" and uf_candidatos == 'MG':
        if not votos['contagem_votos_s_mg']:
            print("Erro: Não há votos para candidatos a esse cargo nessa UF")
            sleep(1)
            return
        else:
            dict_votos_grafico[titulo] = votos['contagem_votos_s_mg']
            numeros_candidato = list(dict_votos_grafico[titulo].keys())
            for i in numeros_candidato:
                numeros_candidato[numeros_candidato.index(i)] = dict_candidatos[i]["Nome"]
            quantidade_votos = list(dict_votos_grafico[titulo].values())
            titulo = "Apuração - Eleições para Senador - MG"

    elif titulo == "S" and uf_candidatos == 'SP':
        if not votos['contagem_votos_s_sp']:
            print("Erro: Não há votos para candidatos a esse cargo nessa UF")
            sleep(1)
            return
        else:
            dict_votos_grafico[titulo] = votos['contagem_votos_s_sp']
            numeros_candidato = list(dict_votos_grafico[titulo].keys())
            for i in numeros_candidato:
                numeros_candidato[numeros_candidato.index(i)] = dict_candidatos[i]["Nome"]
            quantidade_votos = list(dict_votos_grafico[titulo].values())
            titulo = "Apuração - Eleições para Senador - SP"

    elif titulo == "S" and uf_candidatos == 'RJ':
        if not votos['contagem_votos_s_rj']:
            print("Erro: Não há votos para candidatos a esse cargo nessa UF")
            sleep(1)
            return
        else:
            dict_votos_grafico[titulo] = votos['contagem_votos_s_rj']
            numeros_candidato = list(dict_votos_grafico[titulo].keys())
            for i in numeros_candidato:
                numeros_candidato[numeros_candidato.index(i)] = dict_candidatos[i]["Nome"]
            quantidade_votos = list(dict_votos_grafico[titulo].values())
            titulo = "Apuração - Eleições para Senador - RJ"

    elif titulo == "S" and uf_candidatos == 'ES':
        if not votos['contagem_votos_s_es']:
            print("Erro: Não há votos para candidatos a esse cargo nessa UF")
            sleep(1)
            return
        else:
            dict_votos_grafico[titulo] = votos['contagem_votos_s_es']
            numeros_candidato = list(dict_votos_grafico[titulo].keys())
            for i in numeros_candidato:
                numeros_candidato[numeros_candidato.index(i)] = dict_candidatos[i]["Nome"]
            quantidade_votos = list(dict_votos_grafico[titulo].values())
            titulo = "Apuração - Eleições para Senador - ES"

    elif titulo == "G" and uf_candidatos == 'MG':
        if not votos['contagem_votos_g_mg']:
            print("Erro: Não há votos para candidatos a esse cargo nessa UF")
            sleep(1)
            return
        else:
            dict_votos_grafico[titulo] = votos['contagem_votos_g_mg']
            numeros_candidato = list(dict_votos_grafico[titulo].keys())
            for i in numeros_candidato:
                numeros_candidato[numeros_candidato.index(i)] = dict_candidatos[i]["Nome"]
            quantidade_votos = list(dict_votos_grafico[titulo].values())
            titulo = "Apuração - Eleições para Governador - MG"

    elif titulo == "G" and uf_candidatos == 'SP':
        if not votos['contagem_votos_g_sp']:
            print("Erro: Não há votos para candidatos a esse cargo nessa UF")
            sleep(1)
            return
        else:
            dict_votos_grafico[titulo] = votos['contagem_votos_g_sp']
            numeros_candidato = list(dict_votos_grafico[titulo].keys())
            for i in numeros_candidato:
                numeros_candidato[numeros_candidato.index(i)] = dict_candidatos[i]["Nome"]
            quantidade_votos = list(dict_votos_grafico[titulo].values())
            titulo = "Apuração - Eleições para Governador - SP"

    elif titulo == "G" and uf_candidatos == 'RJ':
        if not votos['contagem_votos_g_rj']:
            print("Erro: Não há votos para candidatos a esse cargo nessa UF")
            sleep(1)
            return
        else:
            dict_votos_grafico[titulo] = votos['contagem_votos_g_rj']
            numeros_candidato = list(dict_votos_grafico[titulo].keys())
            for i in numeros_candidato:
                numeros_candidato[numeros_candidato.index(i)] = dict_candidatos[i]["Nome"]
            quantidade_votos = list(dict_votos_grafico[titulo].values())
            titulo = "Apuração - Eleições para Governador - RJ"

    elif titulo == "G" and uf_candidatos == 'ES':
        if not votos['contagem_votos_g_es']:
            print("Erro: Não há votos para candidatos a esse cargo nessa UF")
            sleep(1)
            return
        else:
            dict_votos_grafico[titulo] = votos['contagem_votos_g_es']
            numeros_candidato = list(dict_votos_grafico[titulo].keys())
            for i in numeros_candidato:
                numeros_candidato[numeros_candidato.index(i)] = dict_candidatos[i]["Nome"]
            quantidade_votos = list(dict_votos_grafico[titulo].values())
            titulo = "Apuração - Eleições para Governador - ES"

    # na checagem de votos para Presidente não há verificação de UF
    elif titulo == "P":
        if not votos['contagem_votos_p']:
            print("Erro: Não há votos para candidatos a Presidente")
            sleep(1)
            return
        else:
            dict_votos_grafico[titulo] = votos['contagem_votos_p']
            numeros_candidato = list(dict_votos_grafico[titulo].keys())
            for i in numeros_candidato:
                numeros_candidato[numeros_candidato.index(i)] = dict_candidatos[i]["Nome"]
            quantidade_votos = list(dict_votos_grafico[titulo].values())
            titulo = "Apuração - Eleições para Presidente"

    # lista de cores que podem ser usadas nas barras do gráfico
    cores = ['green', 'blue', 'red', 'orange', 'yellow', 'cyan', 'purple', 'black', 'grey']

    # cria gráfico de barras
    plt.bar(numeros_candidato, quantidade_votos, color=cores, edgecolor='black')

    # adiciona rótulos e título
    plt.ylabel('Votos')
    plt.title(titulo)
    plt.yticks(range(0, max(quantidade_votos) + 2, 1))

    # mostra o gráfico
    plt.show()


# inicia o mixer da biblioteca pygame
pygame.mixer.init()
# a variável beep recebe o arquivo de áudio que será reproduzido ao final da votação de um eleitor
beep = pygame.mixer.Sound('beep.mp3')

# zera dicionários e variáveis para inicializar o programa corretamente
dict_candidatos = {}
dict_eleitores = {}
dict_votos = {}
votos = {}
eleitores_aptos = 0
ok_candidatos = False
ok_eleitores = False
ok_apuracao = False
ok_resultados = False
votacao_finalizada = False

while True:
    # tratamento de erro caso o usuário digite algo que não seja um número inteiro para selecionar uma opção
    try:
        print("""
=-=-=-= MENU PRINCIPAL =-=-=-=
1 - Ler arquivo de candidatos
2 - Ler arquivo de eleitores
3 - Iniciar votação
4 - Apurar votos
5 - Mostrar resultados
6 - Gerar gráficos
7 - Fechar programa\n""")
        op = int(input("Digite a opção desejada: "))
        if op == 1:
            # checa se o carregamento do arquivo de candidatos já foi feito
            # se não, inicia o carregamento
            if not ok_candidatos:
                dict_candidatos, ok_candidatos = ler_candidatos()
            # se sim, não permite carregar novamente
            elif ok_candidatos:
                print()
                print("-=" * 20)
                print("O ARQUIVO DE CANDIDATOS JÁ FOI CARREGADO.")
                print("-=" * 20)
                sleep(1)
        elif op == 2:
            # checa se o carregamento do arquivo de candidatos já foi feito
            # se não, inicia o carregamento
            if not ok_eleitores:
                dict_eleitores, ok_eleitores, eleitores_aptos = ler_eleitores()
            # se sim, não permite carregar novamente
            elif ok_eleitores:
                print()
                print("-=" * 20)
                print("O ARQUIVO DE ELEITORES JÁ FOI CARREGADO.")
                print("-=" * 20)
                sleep(1)
        elif op == 3:
            # checa se o carregamento do arquivo de candidatos/eleitores já foi feito
            # se não, não permite iniciar a votação
            if not ok_candidatos:
                print("Erro: É necessário ler o arquivo de candidatos primeiro (opção 1)")
                sleep(1)
            elif not ok_eleitores:
                print("Erro: É necessário ler o arquivo de eleitores primeiro (opção 2)")
                sleep(1)
            # se sim, checa se a votação já foi iniciada
            else:
                # se não,inicia a votação
                if not votacao_finalizada:
                    votacao_finalizada = iniciar_votacao(dict_candidatos, dict_eleitores)
                # se sim, não permite iniciar a votação novamente
                elif votacao_finalizada:
                    print()
                    print("-=" * 20)
                    print("A VOTAÇÃO JÁ FOI ENCERRADA PELO MESÁRIO.")
                    print("-=" * 20)
                    sleep(1)
        elif op == 4:
            # checa se os arquivos de candidatos/eleitores já foi carregado
            if not ok_candidatos:
                print("Erro: É necessário ler o arquivo de candidatos primeiro (opção 1)")
                sleep(1)
            elif not ok_eleitores:
                print("Erro: É necessário ler o arquivo de eleitores primeiro (opção 2)")
                sleep(1)
            # checa se a votação já foi iniciada antes de apurar os resultados
            elif not votacao_finalizada:
                print("Erro: É necessário iniciar a votação antes de apurar os resultados")
                sleep(1)
            else:
                dict_votos, votos, ok_apuracao = apurar_votos()
        elif op == 5:
            # checa se os arquivos de candidatos/eleitores já foi carregado
            if not ok_candidatos:
                print("Erro: É necessário ler o arquivo de candidatos primeiro (opção 1)")
                sleep(1)
            elif not ok_eleitores:
                print("Erro: É necessário ler o arquivo de eleitores primeiro (opção 2)")
                sleep(1)
            # checa se a votação já foi iniciada antes de mostrar os resultados
            elif not votacao_finalizada:
                print("Erro: É necessário iniciar a votação (opção 3) antes de exibir os resultados")
                sleep(1)
            # checa se os votos já foram apurados antes de mostrar os resultados
            elif not ok_apuracao:
                print("Erro: É necessário apurar os votos (opção 4) antes de exibir os resultados")
                sleep(1)
            else:
                ok_resultados = mostrar_resultados(dict_votos)
        elif op == 6:
            # lista de estados que podem ser selecionados
            lista_estados = ["MG", "SP", "RJ", "ES"]
            # checa se os arquivos de candidatos/eleitores já foi carregado
            if not ok_candidatos:
                print("Erro: É necessário ler o arquivo de candidatos primeiro (opção 1)")
                sleep(1)
            elif not ok_eleitores:
                print("Erro: É necessário ler o arquivo de eleitores primeiro (opção 2)")
                sleep(1)
            # checa se a votação já foi iniciada antes de gerar os gráficos
            elif not votacao_finalizada:
                print("Erro: É necessário iniciar a votação (opção 3) antes de exibir os gráficos")
                sleep(1)
            # checa se os votos já foram apurados antes de gerar os gráficos
            elif not ok_apuracao:
                print("Erro: É necessário apurar os votos (opção 4) antes de exibir os gráficos")
                sleep(1)
            # checa se os resultados já foram exibidos e salvos no BU antes de gerar os gráficos
            elif not ok_resultados:
                print("Erro: É necessário exibir os resultados (opção 5) antes de exibir os gráficos")
                sleep(1)
            else:
                print("""
=-=-=-= OPÇÕES DE GRÁFICOS =-=-=-=
F - Deputado Federal
E - Deputado Estadual
S - Senador
G - Governador
P - Presidente
""")
                # pergunta para qual cargo deseja exibir os gráficos
                titulo = input("Deseja exibir qual gráfico? ").upper()
                while titulo not in ['F', 'E', 'S', 'G', 'P']:
                    titulo = input(
                        "Por favor, digite a letra correspondente ao cargo para o qual deseja exibir o gráfico: ").upper()
                # se o cargo não for "Presidente", pergunta a UF
                if titulo != 'P':
                    uf_candidatos = input("Digite a UF para a qual deseja exibir resultados: ").upper()
                    # não deixa prosseguir caso seja digitado um estado que não estiver na lista_estados
                    while uf_candidatos not in lista_estados:
                        print("UF deve ser MG, SP, RJ ou ES.")
                        uf_candidatos = input("Digite a UF para a qual deseja exibir resultados: ").upper()
                    gera_grafico(titulo, dict_votos, uf_candidatos)
                elif titulo == 'P':
                    uf_candidatos = ''
                    gera_grafico(titulo, dict_votos, uf_candidatos)

        elif op == 7:
            print("Saindo...")
            sleep(0.5)
            break
        else:
            print("Opção inválida")
            sleep(1)

    # tratamento de erro caso o usuário digite algo que não seja um número inteiro para selecionar uma opção
    except ValueError:
        print("Por favor, digite o número de uma das opções.")
        sleep(1)

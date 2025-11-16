
import os
import hashlib
from models import Aluno, Turma, Aula, Atividade, Nota, Chamada, Professor

# --- Constantes de Arquivos ---
# Os arquivos .txt estão na pasta pai (PIM_PRONTO)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARQUIVO_USUARIOS = os.path.join(BASE_DIR, 'usuarios.txt')
ARQUIVO_ALUNOS = os.path.join(BASE_DIR, 'alunos.txt')
ARQUIVO_PROFESSORES = os.path.join(BASE_DIR, 'professores.txt')
ARQUIVO_TURMAS = os.path.join(BASE_DIR, 'turmas.txt')
ARQUIVO_AULAS = os.path.join(BASE_DIR, 'aulas.txt')
ARQUIVO_ATIVIDADES = os.path.join(BASE_DIR, 'atividades.txt')
ARQUIVO_NOTAS = os.path.join(BASE_DIR, 'notas.txt')
ARQUIVO_CHAMADAS = os.path.join(BASE_DIR, 'chamadas.txt')

# --- Funções de Inicialização e Utilitários ---

def inicializar_arquivos():
    """Cria os arquivos de dados se eles não existirem."""
    arquivos = [
        ARQUIVO_USUARIOS, ARQUIVO_ALUNOS, ARQUIVO_PROFESSORES, ARQUIVO_TURMAS,
        ARQUIVO_AULAS, ARQUIVO_ATIVIDADES, ARQUIVO_NOTAS, ARQUIVO_CHAMADAS
    ]
    for arquivo in arquivos:
        if not os.path.exists(arquivo):
            with open(arquivo, 'w', encoding='utf-8') as f:
                pass  # Cria o arquivo vazio

def _hash_senha(senha):
    """Gera um hash SHA-256 para a senha."""
    return hashlib.sha256(senha.encode()).hexdigest()

def get_proximo_id(arquivo):
    """Lê um arquivo e retorna o próximo ID disponível (inteiro)."""
    try:
        with open(arquivo, 'r', encoding='utf-8') as f:
            linhas = f.readlines()
            if not linhas:
                return 1
            for linha in reversed(linhas):
                try:
                    ultimo_id = int(linha.strip().split(';')[0])
                    return ultimo_id + 1
                except (IndexError, ValueError):
                    continue
            return 1
    except FileNotFoundError:
        return 1
    except (IndexError, ValueError):
        return 1

def _reescrever_arquivo(arquivo, linhas_novas):
    with open(arquivo, 'w', encoding='utf-8') as f:
        f.writelines(linhas_novas)

# --- Funções de Usuário ---

def salvar_usuario(id, username, senha, papel, nome, ra, ativo=True):
    """Salva usuário incluindo flag de ativo (1) ou inativo (0)."""
    hash_senha = _hash_senha(senha)
    ra_str = ra if ra is not None else ''
    ativo_flag = '1' if ativo else '0'
    with open(ARQUIVO_USUARIOS, 'a', encoding='utf-8') as f:
        f.write(f"{id};{username};{hash_senha};{papel};{nome};{ra_str};{ativo_flag}\n")

def usuario_existe(username):
    try:
        with open(ARQUIVO_USUARIOS, 'r', encoding='utf-8') as f:
            for linha in f:
                partes = linha.strip().split(';')
                if len(partes) > 1 and partes[1] == username:
                    return True
        return False
    except FileNotFoundError:
        return False

def verificar_usuario(username, senha):
    """
    Retorna (id, papel, nome) apenas se usuário e senha baterem e o usuário estiver ativo.
    Se o registro antigo não tiver o campo 'ativo', assume-se ativo.
    """
    try:
        hash_senha = _hash_senha(senha)
        with open(ARQUIVO_USUARIOS, 'r', encoding='utf-8') as f:
            for linha in f:
                partes = linha.strip().split(';')
                # aceita tanto formatos antigos (6 campos) quanto novo (7 campos)
                if len(partes) >= 5 and partes[1] == username and partes[2] == hash_senha:
                    ativo_flag = '1'
                    if len(partes) >= 7:
                        ativo_flag = partes[6]
                    if ativo_flag == '1':
                        return partes[0], partes[3], partes[4] # id, papel, nome
                    else:
                        return None, None, None
        return None, None, None
    except FileNotFoundError:
        return None, None, None

def listar_usuarios():
    """
    Retorna lista de tuplas representando os usuários.
    Cada tupla: (id, username, hash_senha, papel, nome, ra, ativo_flag)
    Para compatibilidade, se arquivo tiver apenas 6 campos, ativo_flag é assumido '1'.
    """
    usuarios = []
    try:
        with open(ARQUIVO_USUARIOS, 'r', encoding='utf-8') as f:
            for linha in f:
                partes = linha.strip().split(';')
                if len(partes) >= 6:
                    # preenche ativo caso não exista
                    ativo_flag = partes[6] if len(partes) >= 7 else '1'
                    usuarios.append((partes[0], partes[1], partes[2], partes[3], partes[4], partes[5], ativo_flag))
        return usuarios
    except FileNotFoundError:
        return []

def buscar_usuario_por_id(id_usuario):
    """Retorna tupla do usuário (mesmo formato de listar_usuarios) ou None."""
    try:
        with open(ARQUIVO_USUARIOS, 'r', encoding='utf-8') as f:
            for linha in f:
                partes = linha.strip().split(';')
                if len(partes) >= 6 and partes[0] == str(id_usuario):
                    ativo_flag = partes[6] if len(partes) >= 7 else '1'
                    return (partes[0], partes[1], partes[2], partes[3], partes[4], partes[5], ativo_flag)
    except FileNotFoundError:
        pass
    return None

def set_usuario_ativo(id_usuario, ativo):
    """Altera flag 'ativo' do usuário (True/False)."""
    linhas_novas = []
    try:
        with open(ARQUIVO_USUARIOS, 'r', encoding='utf-8') as f:
            for linha in f:
                partes = linha.strip().split(';')
                if len(partes) >= 6:
                    if partes[0] == str(id_usuario):
                        # Garante 7 campos ao reescrever
                        hash_senha = partes[2]
                        papel = partes[3]
                        nome = partes[4]
                        ra = partes[5] if len(partes) > 5 else ''
                        ativo_flag = '1' if ativo else '0'
                        linhas_novas.append(f"{partes[0]};{partes[1]};{hash_senha};{papel};{nome};{ra};{ativo_flag}\n")
                    else:
                        # mantém formato consistente (força 7 campos)
                        ativo_flag = partes[6] if len(partes) >= 7 else '1'
                        ra = partes[5] if len(partes) > 5 else ''
                        linhas_novas.append(f"{partes[0]};{partes[1]};{partes[2]};{partes[3]};{partes[4]};{ra};{ativo_flag}\n")
    except FileNotFoundError:
        return False

    _reescrever_arquivo(ARQUIVO_USUARIOS, linhas_novas)
    return True

def usuario_ativo_por_id(id_usuario):
    u = buscar_usuario_por_id(id_usuario)
    if not u:
        return False
    return u[6] == '1'

# --- Funções de Aluno e Professor (RA) ---

def salvar_aluno(aluno):
    id_turma_str = aluno.id_turma if aluno.id_turma is not None else ''
    with open(ARQUIVO_ALUNOS, 'a', encoding='utf-8') as f:
        f.write(f"{aluno.id};{aluno.nome};{aluno.ra};{id_turma_str}\n")

def salvar_professor(professor):
    with open(ARQUIVO_PROFESSORES, 'a', encoding='utf-8') as f:
        f.write(f"{professor.id};{professor.nome};{professor.ra}\n")

def listar_professores():
    """Retorna apenas professores ativos (para uso em novas operações)."""
    professores = []
    try:
        with open(ARQUIVO_PROFESSORES, 'r', encoding='utf-8') as f:
            for linha in f:
                partes = linha.strip().split(';')
                if len(partes) == 3:
                    pid = partes[0]
                    # verifica se usuário correspondente está ativo
                    if usuario_ativo_por_id(pid):
                        professores.append(Professor(id=pid, nome=partes[1], ra=partes[2]))
        return professores
    except FileNotFoundError:
        return []

def gerar_novo_ra(tipo):
    prefixo = 'A' if tipo == 'aluno' else 'P'
    numero_inicial = 201 if tipo == 'aluno' else 101
    
    ras_existentes = set()
    arquivo = ARQUIVO_ALUNOS if tipo == 'aluno' else ARQUIVO_PROFESSORES
    
    try:
        with open(arquivo, 'r', encoding='utf-8') as f:
            for linha in f:
                partes = linha.strip().split(';')
                if len(partes) > 2:
                    ras_existentes.add(partes[2])
    except FileNotFoundError:
        pass

    novo_numero = numero_inicial
    while True:
        novo_ra = f"{prefixo}{novo_numero}"
        if novo_ra not in ras_existentes:
            return novo_ra
        novo_numero += 1

def listar_alunos(filter_ativos=True):
    """
    Retorna lista de alunos.
    Por padrão (filter_ativos=True) retorna apenas alunos com usuário ativo.
    """
    alunos = []
    try:
        with open(ARQUIVO_ALUNOS, 'r', encoding='utf-8') as f:
            for linha in f:
                partes = linha.strip().split(';')
                if len(partes) >= 3:
                    id, nome, ra = partes[0], partes[1], partes[2]
                    id_turma = partes[3] if len(partes) > 3 and partes[3] else None
                    # se filter_ativos, checa se o usuário está ativo
                    if filter_ativos:
                        if usuario_ativo_por_id(id):
                            alunos.append(Aluno(id=id, nome=nome, ra=ra, id_turma=id_turma))
                    else:
                        alunos.append(Aluno(id=id, nome=nome, ra=ra, id_turma=id_turma))
        return alunos
    except FileNotFoundError:
        return []

def buscar_aluno_por_id(id_aluno):
    # Retorna aluno independentemente do status ativo/inativo para preservar histórico
    for aluno in listar_alunos(filter_ativos=False):
        if aluno.id == str(id_aluno):
            return aluno
    return None
    
def listar_alunos_sem_turma():
    # Para novos registros, só retornamos alunos sem turma e ativos
    return [aluno for aluno in listar_alunos(filter_ativos=True) if not aluno.id_turma]
    
# --- Funções de Turma ---

def salvar_turma(turma):
    ids_alunos_str = ",".join(map(str, turma.id_alunos))
    with open(ARQUIVO_TURMAS, 'a', encoding='utf-8') as f:
        f.write(f"{turma.id};{turma.nome_disciplina};{ids_alunos_str}\n")

def listar_turmas():
    turmas = []
    try:
        with open(ARQUIVO_TURMAS, 'r', encoding='utf-8') as f:
            for linha in f:
                partes = linha.strip().split(';')
                if len(partes) >= 2:
                    id, nome = partes[0], partes[1]
                    ids_alunos = partes[2].split(',') if len(partes) > 2 and partes[2] else []
                    turmas.append(Turma(id=id, nome_disciplina=nome, id_alunos=[i for i in ids_alunos if i]))
        return turmas
    except FileNotFoundError:
        return []

def buscar_turma_por_id(id_turma):
    for turma in listar_turmas():
        if turma.id == str(id_turma):
            return turma
    return None

def adicionar_aluno_a_turma(id_aluno, id_turma):
    id_turma_str = str(id_turma)
    id_aluno_str = str(id_aluno)

    turmas = listar_turmas()
    linhas_novas = []
    for turma in turmas:
        if turma.id == id_turma_str:
            if id_aluno_str not in [str(x) for x in turma.id_alunos]:
                turma.id_alunos.append(id_aluno_str)
        ids_alunos_str = ",".join(map(str, turma.id_alunos))
        linhas_novas.append(f"{turma.id};{turma.nome_disciplina};{ids_alunos_str}\n")
    _reescrever_arquivo(ARQUIVO_TURMAS, linhas_novas)

def atualizar_turma_aluno(id_aluno, id_turma):
    id_aluno_str = str(id_aluno)
    id_turma_str = str(id_turma)

    alunos = listar_alunos(filter_ativos=False)
    linhas_novas = []
    for aluno in alunos:
        if str(aluno.id) == id_aluno_str:
            aluno.id_turma = id_turma_str
        id_turma_write = aluno.id_turma if aluno.id_turma else ''
        linhas_novas.append(f"{aluno.id};{aluno.nome};{aluno.ra};{id_turma_write}\n")
    _reescrever_arquivo(ARQUIVO_ALUNOS, linhas_novas)

def atualizar_turma_alunos(ids_alunos, id_turma):
    for id_aluno in ids_alunos:
        atualizar_turma_aluno(id_aluno, id_turma)

# --- Funções de Aula, Atividade, Nota, Chamada ---

def salvar_aula(aula):
    with open(ARQUIVO_AULAS, 'a', encoding='utf-8') as f:
        f.write(f"{aula.id};{aula.id_turma};{aula.data};{aula.topico};{aula.id_professor}\n")

def listar_aulas():
    aulas = []
    try:
        with open(ARQUIVO_AULAS, 'r', encoding='utf-8') as f:
            for linha in f:
                partes = linha.strip().split(';')
                if len(partes) == 5:
                    aulas.append(Aula(id=partes[0], id_turma=partes[1], data=partes[2], topico=partes[3], id_professor=partes[4]))
    except FileNotFoundError:
        return []
    return aulas

def salvar_atividade(atividade):
    id_professor_str = atividade.id_professor if atividade.id_professor else ''
    with open(ARQUIVO_ATIVIDADES, 'a', encoding='utf-8') as f:
        f.write(f"{atividade.id};{atividade.id_turma};{atividade.descricao};{id_professor_str}\n")

def listar_atividades():
    atividades = []
    try:
        with open(ARQUIVO_ATIVIDADES, 'r', encoding='utf-8') as f:
            for linha in f:
                partes = linha.strip().split(';')
                if len(partes) >= 3:
                    # Compatibilidade: se não tiver id_professor (arquivo antigo), define como None
                    id_professor = partes[3] if len(partes) > 3 and partes[3] else None
                    atividades.append(Atividade(id=partes[0], id_turma=partes[1], 
                                               descricao=partes[2], id_professor=id_professor))
        return atividades
    except FileNotFoundError:
        return []

def salvar_ou_atualizar_nota(nova_nota):
    notas = []
    nota_atualizada = False
    try:
        with open(ARQUIVO_NOTAS, 'r', encoding='utf-8') as f:
            for linha in f:
                partes = linha.strip().split(';')
                if len(partes) == 3 and partes[0] == nova_nota.id_aluno and partes[1] == nova_nota.id_atividade:
                    notas.append(f"{nova_nota.id_aluno};{nova_nota.id_atividade};{nova_nota.nota}\n")
                    nota_atualizada = True
                else:
                    notas.append(linha)
    except FileNotFoundError:
        pass
    
    if not nota_atualizada:
        notas.append(f"{nova_nota.id_aluno};{nova_nota.id_atividade};{nova_nota.nota}\n")
    
    _reescrever_arquivo(ARQUIVO_NOTAS, notas)

def listar_notas_por_aluno(id_aluno):
    notas = []
    try:
        with open(ARQUIVO_NOTAS, 'r', encoding='utf-8') as f:
            for linha in f:
                partes = linha.strip().split(';')
                if len(partes) == 3 and partes[0] == str(id_aluno):
                    notas.append(Nota(id_aluno=partes[0], id_atividade=partes[1], nota=float(partes[2])))
        return notas
    except FileNotFoundError:
        return []

def salvar_chamada(lista_de_chamada):
    with open(ARQUIVO_CHAMADAS, 'a', encoding='utf-8') as f:
        for chamada in lista_de_chamada:
            f.write(f"{chamada.id_aula};{chamada.id_aluno};{chamada.status}\n")

def listar_chamadas_por_aula(id_aula):
    chamadas = []
    try:
        with open(ARQUIVO_CHAMADAS, 'r', encoding='utf-8') as f:
            for linha in f:
                partes = linha.strip().split(';')
                if len(partes) == 3 and partes[0] == str(id_aula):
                    chamadas.append(Chamada(id_aula=partes[0], id_aluno=partes[1], status=partes[2].strip()))
        return chamadas
    except FileNotFoundError:
        return []

def listar_chamadas_por_aluno(id_aluno):
    chamadas = []
    try:
        with open(ARQUIVO_CHAMADAS, 'r', encoding='utf-8') as f:
            for linha in f:
                partes = linha.strip().split(';')
                if len(partes) == 3 and partes[1] == str(id_aluno):
                    chamadas.append(Chamada(id_aula=partes[0], id_aluno=partes[1], status=partes[2].strip()))
        return chamadas
    except FileNotFoundError:
        return []

# --- FUNÇÃO ADICIONADA PARA CORRIGIR O ERRO ---
def sobrescrever_chamada_por_aula(id_aula_alvo, nova_lista_de_chamada):
    """Remove todos os registros de chamada para uma aula e os substitui pelos novos."""
    linhas_finais = []
    try:
        with open(ARQUIVO_CHAMADAS, 'r', encoding='utf-8') as f:
            for linha in f:
                partes = linha.strip().split(';')
                # Mantém as linhas que NÃO são da aula que estamos editando
                if len(partes) > 0 and partes[0] != str(id_aula_alvo):
                    linhas_finais.append(linha)
    except FileNotFoundError:
        pass # O arquivo pode não existir, o que é normal.

    # Adiciona as novas linhas da chamada atualizada
    for chamada in nova_lista_de_chamada:
        linhas_finais.append(f"{chamada.id_aula};{chamada.id_aluno};{chamada.status}\n")
    
    # Reescreve o arquivo com os dados corretos
    _reescrever_arquivo(ARQUIVO_CHAMADAS, linhas_finais)
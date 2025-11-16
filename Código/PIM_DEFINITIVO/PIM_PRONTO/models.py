
class Aluno:
    def __init__(self, id, nome, ra, id_turma=None):
        self.id = str(id)
        self.nome = nome
        self.ra = ra
        self.id_turma = str(id_turma) if id_turma else None

    def __str__(self):
        turma_str = f", ID Turma: {self.id_turma}" if self.id_turma else ", Sem Turma"
        return f"ID: {self.id}, RA: {self.ra}, Nome: {self.nome}{turma_str}"

class Professor:
    def __init__(self, id, nome, ra):
        self.id = str(id)
        self.nome = nome
        self.ra = ra

    def __str__(self):
        return f"ID: {self.id}, RA: {self.ra}, Nome: {self.nome}"

class Turma:
    def __init__(self, id, nome_disciplina, id_alunos=None):
        self.id = str(id)
        self.nome_disciplina = nome_disciplina
        self.id_alunos = id_alunos if id_alunos is not None else []

    def __str__(self):
        num_alunos = len(self.id_alunos)
        return f"ID: {self.id}, Turma: {self.nome_disciplina}, Alunos: {num_alunos}"

class Aula:
    def __init__(self, id, id_turma, data, topico, id_professor):
        self.id = str(id)
        self.id_turma = str(id_turma)
        self.data = data
        self.topico = topico
        self.id_professor = str(id_professor)

    def __str__(self):
        return f"ID: {self.id}, ID Turma: {self.id_turma}, Data: {self.data}, Tópico: {self.topico}, ID Prof: {self.id_professor}"

class Atividade:
    def __init__(self, id, id_turma, descricao, id_professor=None):
        self.id = str(id)
        self.id_turma = str(id_turma)
        self.descricao = descricao
        self.id_professor = str(id_professor) if id_professor else None

    def __str__(self):
        return f"ID: {self.id}, ID Turma: {self.id_turma}, Descrição: {self.descricao}, ID Prof: {self.id_professor}"

class Nota:
    def __init__(self, id_aluno, id_atividade, nota):
        self.id_aluno = str(id_aluno)
        self.id_atividade = str(id_atividade)
        self.nota = float(nota)

    def __str__(self):
        return f"Aluno ID: {self.id_aluno}, Atividade ID: {self.id_atividade}, Nota: {self.nota}"

class Chamada:
    def __init__(self, id_aula, id_aluno, status):
        self.id_aula = str(id_aula)
        self.id_aluno = str(id_aluno)
        self.status = status # 'P' ou 'F'

    def __str__(self):
        status_str = "Presente" if self.status == 'P' else "Falta"
        return f"Aula ID: {self.id_aula}, Aluno ID: {self.id_aluno}, Status: {status_str}"
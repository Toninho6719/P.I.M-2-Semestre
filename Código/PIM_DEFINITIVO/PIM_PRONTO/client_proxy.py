"""
Cliente de Rede para Sistema Acadêmico PIM
Conecta-se ao servidor proxy via LAN
"""

import socket
import json


class AcademicClient:
    def __init__(self, server_host='localhost', server_port=5000):
        self.server_host = server_host
        self.server_port = server_port
        self.socket = None
        self.session_id = None
        self.user_info = None
        self.connected = False
    
    def connect(self):
        """Estabelece conexão com o servidor"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.server_host, self.server_port))
            self.connected = True
            return True
        except Exception as e:
            print(f"Erro ao conectar: {e}")
            self.connected = False
            return False
    
    def disconnect(self):
        """Desconecta do servidor"""
        if self.socket:
            try:
                if self.session_id:
                    self.logout()
                self.socket.close()
            except:
                pass
            finally:
                self.connected = False
                self.socket = None
    
    def send_request(self, action, data=None):
        """Envia requisição ao servidor"""
        if not self.connected:
            if not self.connect():
                return {'status': 'error', 'message': 'Não foi possível conectar ao servidor'}
        
        try:
            request = {
                'action': action,
                'data': data if data else {}
            }
            
            # Adiciona session_id se disponível
            if self.session_id and action not in ['login']:
                request['data']['session_id'] = self.session_id
            
            # Envia requisição
            request_json = json.dumps(request, ensure_ascii=False)
            self.socket.send(request_json.encode('utf-8'))
            
            # Recebe resposta
            response_data = self.socket.recv(8192).decode('utf-8')
            response = json.loads(response_data)
            
            return response
            
        except Exception as e:
            self.connected = False
            return {'status': 'error', 'message': f'Erro de comunicação: {str(e)}'}
    
    # ===== MÉTODOS DE AUTENTICAÇÃO =====
    
    def login(self, username, password):
        """Autentica no servidor"""
        response = self.send_request('login', {
            'username': username,
            'password': password
        })
        
        if response.get('status') == 'success':
            data = response.get('data', {})
            self.session_id = data.get('session_id')
            self.user_info = {
                'id_usuario': data.get('id_usuario'),
                'nome': data.get('nome'),
                'papel': data.get('papel')
            }
            return True, self.user_info
        else:
            return False, response.get('message', 'Erro de autenticação')
    
    def logout(self):
        """Encerra sessão"""
        if self.session_id:
            response = self.send_request('logout', {
                'session_id': self.session_id
            })
            self.session_id = None
            self.user_info = None
            return response.get('status') == 'success'
        return False
    
    def is_authenticated(self):
        """Verifica se está autenticado"""
        return self.session_id is not None
    
    def get_user_info(self):
        """Retorna informações do usuário logado"""
        return self.user_info
    
    # ===== MÉTODOS DE LISTAGEM =====
    
    def listar_usuarios(self):
        """Lista todos os usuários"""
        response = self.send_request('listar_usuarios')
        if response.get('status') == 'success':
            return response.get('data', [])
        return []
    
    def listar_alunos(self, filter_ativos=True):
        """Lista alunos"""
        response = self.send_request('listar_alunos', {
            'filter_ativos': filter_ativos
        })
        if response.get('status') == 'success':
            return response.get('data', [])
        return []
    
    def listar_professores(self):
        """Lista professores"""
        response = self.send_request('listar_professores')
        if response.get('status') == 'success':
            return response.get('data', [])
        return []
    
    def listar_turmas(self):
        """Lista turmas"""
        response = self.send_request('listar_turmas')
        if response.get('status') == 'success':
            return response.get('data', [])
        return []
    
    def listar_aulas(self):
        """Lista aulas"""
        response = self.send_request('listar_aulas')
        if response.get('status') == 'success':
            return response.get('data', [])
        return []
    
    def listar_atividades(self):
        """Lista atividades"""
        response = self.send_request('listar_atividades')
        if response.get('status') == 'success':
            return response.get('data', [])
        return []
    
    def listar_notas_aluno(self, id_aluno):
        """Lista notas de um aluno"""
        response = self.send_request('listar_notas_aluno', {
            'id_aluno': id_aluno
        })
        if response.get('status') == 'success':
            return response.get('data', [])
        return []
    
    def listar_chamadas_aluno(self, id_aluno):
        """Lista chamadas de um aluno"""
        response = self.send_request('listar_chamadas_aluno', {
            'id_aluno': id_aluno
        })
        if response.get('status') == 'success':
            return response.get('data', [])
        return []
    
    # ===== MÉTODOS DE CADASTRO =====
    
    def cadastrar_usuario(self, username, senha, papel, nome, ra=None):
        """Cadastra novo usuário"""
        response = self.send_request('cadastrar_usuario', {
            'username': username,
            'senha': senha,
            'papel': papel,
            'nome': nome,
            'ra': ra
        })
        return response.get('status') == 'success', response.get('message', '')
    
    def cadastrar_aluno(self, id, nome, ra, id_turma=None):
        """Cadastra aluno"""
        response = self.send_request('cadastrar_aluno', {
            'id': id,
            'nome': nome,
            'ra': ra,
            'id_turma': id_turma
        })
        return response.get('status') == 'success', response.get('message', '')
    
    def cadastrar_professor(self, id, nome, ra):
        """Cadastra professor"""
        response = self.send_request('cadastrar_professor', {
            'id': id,
            'nome': nome,
            'ra': ra
        })
        return response.get('status') == 'success', response.get('message', '')
    
    def cadastrar_turma(self, id, nome_disciplina, id_alunos=None):
        """Cadastra turma"""
        response = self.send_request('cadastrar_turma', {
            'id': id,
            'nome_disciplina': nome_disciplina,
            'id_alunos': id_alunos if id_alunos else []
        })
        return response.get('status') == 'success', response.get('message', '')
    
    def registrar_aula(self, id, id_turma, data, topico, id_professor):
        """Registra aula"""
        response = self.send_request('registrar_aula', {
            'id': id,
            'id_turma': id_turma,
            'data': data,
            'topico': topico,
            'id_professor': id_professor
        })
        return response.get('status') == 'success', response.get('message', '')
    
    def registrar_atividade(self, id, id_turma, descricao, id_professor=None):
        """Registra atividade"""
        response = self.send_request('registrar_atividade', {
            'id': id,
            'id_turma': id_turma,
            'descricao': descricao,
            'id_professor': id_professor
        })
        return response.get('status') == 'success', response.get('message', '')
    
    def lancar_nota(self, id_aluno, id_atividade, nota):
        """Lança nota"""
        response = self.send_request('lancar_nota', {
            'id_aluno': id_aluno,
            'id_atividade': id_atividade,
            'nota': nota
        })
        return response.get('status') == 'success', response.get('message', '')
    
    def registrar_chamada(self, chamadas):
        """Registra chamada (lista de dicionários)"""
        response = self.send_request('registrar_chamada', {
            'chamadas': chamadas
        })
        return response.get('status') == 'success', response.get('message', '')
    
    def ativar_desativar_usuario(self, id_usuario, ativo):
        """Ativa ou desativa usuário"""
        response = self.send_request('ativar_desativar_usuario', {
            'id_usuario': id_usuario,
            'ativo': ativo
        })
        return response.get('status') == 'success', response.get('message', '')
    
    def buscar_aluno(self, id_aluno):
        """Busca aluno por ID"""
        response = self.send_request('buscar_aluno', {
            'id_aluno': id_aluno
        })
        if response.get('status') == 'success':
            return response.get('data')
        return None
    
    def buscar_turma(self, id_turma):
        """Busca turma por ID"""
        response = self.send_request('buscar_turma', {
            'id_turma': id_turma
        })
        if response.get('status') == 'success':
            return response.get('data')
        return None


# Teste do cliente (executar apenas se chamado diretamente)
if __name__ == "__main__":
    print("=" * 60)
    print("TESTE DO CLIENTE DE REDE")
    print("=" * 60)
    
    # Configurar endereço do servidor
    SERVER_HOST = input("Digite o IP do servidor (Enter para localhost): ").strip()
    if not SERVER_HOST:
        SERVER_HOST = 'localhost'
    
    SERVER_PORT = 5000
    
    # Cria cliente
    client = AcademicClient(server_host=SERVER_HOST, server_port=SERVER_PORT)
    
    # Tenta conectar
    print(f"\n🔌 Conectando ao servidor {SERVER_HOST}:{SERVER_PORT}...")
    if client.connect():
        print("✅ Conectado com sucesso!\n")
        
        # Tenta fazer login
        username = input("Username: ")
        password = input("Password: ")
        
        print("\n🔑 Autenticando...")
        success, result = client.login(username, password)
        
        if success:
            print(f"✅ Login bem-sucedido!")
            print(f"   Nome: {result['nome']}")
            print(f"   Papel: {result['papel']}")
            print(f"   ID: {result['id_usuario']}")
            
            # Testa listagem
            print("\n📋 Testando listagem de turmas...")
            turmas = client.listar_turmas()
            print(f"   Total de turmas: {len(turmas)}")
            for turma in turmas[:3]:  # Mostra até 3
                print(f"   - {turma['id']}: {turma['nome_disciplina']}")
            
            # Logout
            print("\n🚪 Fazendo logout...")
            client.logout()
            print("✅ Logout realizado")
        else:
            print(f"❌ Erro no login: {result}")
        
        client.disconnect()
        print("\n🔌 Desconectado do servidor")
    else:
        print("❌ Não foi possível conectar ao servidor")
    
    print("\n" + "=" * 60)

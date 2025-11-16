"""
Servidor Proxy para Sistema Acadêmico PIM
Gerencia múltiplas conexões de clientes em uma rede LAN
"""

import socket
import threading
import json
import hashlib
import sys
import os
from datetime import datetime

# Adiciona o diretório ao path para importar os módulos
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import database as db
from models import Aluno, Turma, Aula, Atividade, Nota, Chamada, Professor

class AcademicServerProxy:
    def __init__(self, host='0.0.0.0', port=5000):
        self.host = host
        self.port = port
        self.server_socket = None
        self.clients = []
        self.sessions = {}  # Armazena sessões ativas {session_id: {user_info}}
        self.active_connections = 0
        
    def start(self):
        """Inicia o servidor proxy"""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(10)
            
            print("=" * 60)
            print("🚀 SERVIDOR PROXY - SISTEMA ACADÊMICO PIM")
            print("=" * 60)
            print(f"📡 Servidor iniciado em: {self.host}:{self.port}")
            print(f"⏰ Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
            print(f"📁 Banco de dados: Arquivos .txt")
            print("=" * 60)
            print("✅ Aguardando conexões de clientes...\n")
            
            while True:
                try:
                    client_socket, address = self.server_socket.accept()
                    self.active_connections += 1
                    
                    print(f"✅ [{datetime.now().strftime('%H:%M:%S')}] Cliente conectado: {address[0]}:{address[1]}")
                    print(f"   Total de conexões ativas: {self.active_connections}\n")
                    
                    # Cria thread para cada cliente
                    client_thread = threading.Thread(
                        target=self.handle_client,
                        args=(client_socket, address),
                        daemon=True
                    )
                    client_thread.start()
                    
                    self.clients.append((client_socket, address))
                    
                except KeyboardInterrupt:
                    break
                except Exception as e:
                    print(f"❌ Erro ao aceitar conexão: {e}")
                    
        except Exception as e:
            print(f"❌ Erro ao iniciar servidor: {e}")
        finally:
            self.shutdown()
    
    def handle_client(self, client_socket, address):
        """Gerencia requisições de um cliente específico"""
        try:
            while True:
                # Recebe dados do cliente
                data = client_socket.recv(8192).decode('utf-8')
                
                if not data:
                    break
                
                # Processa requisição
                request = json.loads(data)
                action = request.get('action')
                
                print(f"📨 [{datetime.now().strftime('%H:%M:%S')}] {address[0]} -> {action}")
                
                response = self.process_request(request, address)
                
                # Envia resposta
                response_json = json.dumps(response, ensure_ascii=False)
                client_socket.send(response_json.encode('utf-8'))
                
        except ConnectionResetError:
            pass
        except Exception as e:
            print(f"❌ Erro com cliente {address}: {str(e)}")
        finally:
            client_socket.close()
            if (client_socket, address) in self.clients:
                self.clients.remove((client_socket, address))
            self.active_connections -= 1
            print(f"🔌 [{datetime.now().strftime('%H:%M:%S')}] Cliente desconectado: {address[0]}:{address[1]}")
            print(f"   Total de conexões ativas: {self.active_connections}\n")
    
    def process_request(self, request, address):
        """Processa diferentes tipos de requisições"""
        action = request.get('action')
        data = request.get('data', {})
        
        try:
            # Autenticação
            if action == 'login':
                return self.handle_login(data, address)
            elif action == 'logout':
                return self.handle_logout(data)
            
            # Validar sessão para ações protegidas
            session_id = data.get('session_id')
            if not self.validate_session(session_id):
                return {'status': 'error', 'message': 'Sessão inválida ou expirada'}
            
            # Roteamento de ações
            handlers = {
                'listar_usuarios': self.handle_listar_usuarios,
                'listar_alunos': self.handle_listar_alunos,
                'listar_professores': self.handle_listar_professores,
                'listar_turmas': self.handle_listar_turmas,
                'listar_aulas': self.handle_listar_aulas,
                'listar_atividades': self.handle_listar_atividades,
                'listar_notas_aluno': self.handle_listar_notas_aluno,
                'listar_chamadas_aluno': self.handle_listar_chamadas_aluno,
                'cadastrar_usuario': self.handle_cadastrar_usuario,
                'cadastrar_aluno': self.handle_cadastrar_aluno,
                'cadastrar_professor': self.handle_cadastrar_professor,
                'cadastrar_turma': self.handle_cadastrar_turma,
                'registrar_aula': self.handle_registrar_aula,
                'registrar_atividade': self.handle_registrar_atividade,
                'lancar_nota': self.handle_lancar_nota,
                'registrar_chamada': self.handle_registrar_chamada,
                'ativar_desativar_usuario': self.handle_ativar_desativar_usuario,
                'buscar_aluno': self.handle_buscar_aluno,
                'buscar_turma': self.handle_buscar_turma,
            }
            
            handler = handlers.get(action)
            if handler:
                return handler(data)
            else:
                return {'status': 'error', 'message': f'Ação desconhecida: {action}'}
                
        except Exception as e:
            return {'status': 'error', 'message': f'Erro no servidor: {str(e)}'}
    
    def validate_session(self, session_id):
        """Valida se a sessão existe e está ativa"""
        return session_id in self.sessions
    
    # ===== HANDLERS DE AUTENTICAÇÃO =====
    
    def handle_login(self, data, address):
        """Autentica usuário"""
        username = data.get('username')
        password = data.get('password')
        
        id_usuario, papel, nome = db.verificar_usuario(username, password)
        
        if papel:
            # Cria sessão única
            session_id = hashlib.sha256(
                f"{username}{address}{datetime.now().timestamp()}".encode()
            ).hexdigest()
            
            self.sessions[session_id] = {
                'id_usuario': id_usuario,
                'nome': nome,
                'papel': papel,
                'address': address,
                'login_time': datetime.now().isoformat()
            }
            
            print(f"   ✓ Login bem-sucedido: {nome} ({papel})")
            
            return {
                'status': 'success',
                'data': {
                    'session_id': session_id,
                    'id_usuario': id_usuario,
                    'nome': nome,
                    'papel': papel
                }
            }
        else:
            print(f"   ✗ Tentativa de login falhou: {username}")
            return {'status': 'error', 'message': 'Usuário ou senha inválidos'}
    
    def handle_logout(self, data):
        """Encerra sessão"""
        session_id = data.get('session_id')
        if session_id in self.sessions:
            user_info = self.sessions[session_id]
            del self.sessions[session_id]
            print(f"   ✓ Logout: {user_info['nome']}")
            return {'status': 'success', 'message': 'Logout realizado'}
        return {'status': 'error', 'message': 'Sessão inválida'}
    
    # ===== HANDLERS DE LISTAGEM =====
    
    def handle_listar_usuarios(self, data):
        """Lista todos os usuários"""
        usuarios = db.listar_usuarios()
        usuarios_list = [
            {
                'id': u[0],
                'username': u[1],
                'papel': u[3],
                'nome': u[4],
                'ra': u[5] if u[5] else '',
                'ativo': u[6]
            }
            for u in usuarios
        ]
        return {'status': 'success', 'data': usuarios_list}
    
    def handle_listar_alunos(self, data):
        """Lista alunos"""
        filter_ativos = data.get('filter_ativos', True)
        alunos = db.listar_alunos(filter_ativos=filter_ativos)
        alunos_list = [
            {
                'id': a.id,
                'nome': a.nome,
                'ra': a.ra,
                'id_turma': a.id_turma if a.id_turma else ''
            }
            for a in alunos
        ]
        return {'status': 'success', 'data': alunos_list}
    
    def handle_listar_professores(self, data):
        """Lista professores"""
        professores = db.listar_professores()
        prof_list = [
            {
                'id': p.id,
                'nome': p.nome,
                'ra': p.ra
            }
            for p in professores
        ]
        return {'status': 'success', 'data': prof_list}
    
    def handle_listar_turmas(self, data):
        """Lista turmas"""
        turmas = db.listar_turmas()
        turmas_list = [
            {
                'id': t.id,
                'nome_disciplina': t.nome_disciplina,
                'id_alunos': t.id_alunos
            }
            for t in turmas
        ]
        return {'status': 'success', 'data': turmas_list}
    
    def handle_listar_aulas(self, data):
        """Lista aulas"""
        aulas = db.listar_aulas()
        aulas_list = [
            {
                'id': a.id,
                'id_turma': a.id_turma,
                'data': a.data,
                'topico': a.topico,
                'id_professor': a.id_professor
            }
            for a in aulas
        ]
        return {'status': 'success', 'data': aulas_list}
    
    def handle_listar_atividades(self, data):
        """Lista atividades"""
        atividades = db.listar_atividades()
        ativ_list = [
            {
                'id': a.id,
                'id_turma': a.id_turma,
                'descricao': a.descricao,
                'id_professor': a.id_professor if a.id_professor else ''
            }
            for a in atividades
        ]
        return {'status': 'success', 'data': ativ_list}
    
    def handle_listar_notas_aluno(self, data):
        """Lista notas de um aluno"""
        id_aluno = data.get('id_aluno')
        notas = db.listar_notas_por_aluno(id_aluno)
        notas_list = [
            {
                'id_aluno': n.id_aluno,
                'id_atividade': n.id_atividade,
                'nota': n.nota
            }
            for n in notas
        ]
        return {'status': 'success', 'data': notas_list}
    
    def handle_listar_chamadas_aluno(self, data):
        """Lista chamadas de um aluno"""
        id_aluno = data.get('id_aluno')
        chamadas = db.listar_chamadas_por_aluno(id_aluno)
        chamadas_list = [
            {
                'id_aula': c.id_aula,
                'id_aluno': c.id_aluno,
                'status': c.status
            }
            for c in chamadas
        ]
        return {'status': 'success', 'data': chamadas_list}
    
    # ===== HANDLERS DE CADASTRO =====
    
    def handle_cadastrar_usuario(self, data):
        """Cadastra novo usuário"""
        id_usuario = db.get_proximo_id(db.ARQUIVO_USUARIOS)
        db.salvar_usuario(
            id=id_usuario,
            username=data['username'],
            senha=data['senha'],
            papel=data['papel'],
            nome=data['nome'],
            ra=data.get('ra'),
            ativo=True
        )
        return {'status': 'success', 'message': 'Usuário cadastrado', 'id': id_usuario}
    
    def handle_cadastrar_aluno(self, data):
        """Cadastra aluno"""
        aluno = Aluno(
            id=data['id'],
            nome=data['nome'],
            ra=data['ra'],
            id_turma=data.get('id_turma')
        )
        db.salvar_aluno(aluno)
        return {'status': 'success', 'message': 'Aluno cadastrado'}
    
    def handle_cadastrar_professor(self, data):
        """Cadastra professor"""
        professor = Professor(
            id=data['id'],
            nome=data['nome'],
            ra=data['ra']
        )
        db.salvar_professor(professor)
        return {'status': 'success', 'message': 'Professor cadastrado'}
    
    def handle_cadastrar_turma(self, data):
        """Cadastra turma"""
        turma = Turma(
            id=data['id'],
            nome_disciplina=data['nome_disciplina'],
            id_alunos=data.get('id_alunos', [])
        )
        db.salvar_turma(turma)
        return {'status': 'success', 'message': 'Turma cadastrada'}
    
    def handle_registrar_aula(self, data):
        """Registra aula"""
        aula = Aula(
            id=data['id'],
            id_turma=data['id_turma'],
            data=data['data'],
            topico=data['topico'],
            id_professor=data['id_professor']
        )
        db.salvar_aula(aula)
        return {'status': 'success', 'message': 'Aula registrada'}
    
    def handle_registrar_atividade(self, data):
        """Registra atividade"""
        atividade = Atividade(
            id=data['id'],
            id_turma=data['id_turma'],
            descricao=data['descricao'],
            id_professor=data.get('id_professor')
        )
        db.salvar_atividade(atividade)
        return {'status': 'success', 'message': 'Atividade registrada'}
    
    def handle_lancar_nota(self, data):
        """Lança nota"""
        nota = Nota(
            id_aluno=data['id_aluno'],
            id_atividade=data['id_atividade'],
            nota=float(data['nota'])
        )
        db.salvar_ou_atualizar_nota(nota)
        return {'status': 'success', 'message': 'Nota lançada'}
    
    def handle_registrar_chamada(self, data):
        """Registra chamada"""
        lista_chamadas = [
            Chamada(
                id_aula=c['id_aula'],
                id_aluno=c['id_aluno'],
                status=c['status']
            )
            for c in data['chamadas']
        ]
        db.salvar_chamada(lista_chamadas)
        return {'status': 'success', 'message': 'Chamada registrada'}
    
    def handle_ativar_desativar_usuario(self, data):
        """Ativa ou desativa usuário"""
        success = db.set_usuario_ativo(data['id_usuario'], data['ativo'])
        if success:
            return {'status': 'success', 'message': 'Status atualizado'}
        return {'status': 'error', 'message': 'Erro ao atualizar'}
    
    def handle_buscar_aluno(self, data):
        """Busca aluno por ID"""
        aluno = db.buscar_aluno_por_id(data['id_aluno'])
        if aluno:
            return {
                'status': 'success',
                'data': {
                    'id': aluno.id,
                    'nome': aluno.nome,
                    'ra': aluno.ra,
                    'id_turma': aluno.id_turma if aluno.id_turma else ''
                }
            }
        return {'status': 'error', 'message': 'Aluno não encontrado'}
    
    def handle_buscar_turma(self, data):
        """Busca turma por ID"""
        turma = db.buscar_turma_por_id(data['id_turma'])
        if turma:
            return {
                'status': 'success',
                'data': {
                    'id': turma.id,
                    'nome_disciplina': turma.nome_disciplina,
                    'id_alunos': turma.id_alunos
                }
            }
        return {'status': 'error', 'message': 'Turma não encontrada'}
    
    def shutdown(self):
        """Encerra o servidor"""
        print("\n" + "=" * 60)
        print("🛑 Encerrando servidor...")
        
        for client_socket, address in self.clients:
            try:
                client_socket.close()
            except:
                pass
        
        if self.server_socket:
            self.server_socket.close()
        
        print(f"✅ Servidor encerrado às {datetime.now().strftime('%H:%M:%S')}")
        print("=" * 60)


def main():
    """Função principal"""
    print("\n")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║     SERVIDOR PROXY - SISTEMA ACADÊMICO PIM                ║")
    print("║            Modelo Cliente-Servidor com Proxy              ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print("\n")
    
    # Inicializa banco de dados
    db.inicializar_arquivos()
    
    # Configuração do servidor
    HOST = '0.0.0.0'  # Aceita conexões de qualquer IP
    PORT = 5000
    
    print(f"📝 Configuração:")
    print(f"   Host: {HOST} (todas as interfaces)")
    print(f"   Porta: {PORT}")
    print(f"   Protocolo: TCP/IP")
    print(f"   Encoding: UTF-8")
    print("\n")
    
    server = AcademicServerProxy(host=HOST, port=PORT)
    
    try:
        server.start()
    except KeyboardInterrupt:
        print("\n")
        server.shutdown()
    except Exception as e:
        print(f"\n❌ Erro fatal: {e}")
        server.shutdown()


if __name__ == "__main__":
    main()

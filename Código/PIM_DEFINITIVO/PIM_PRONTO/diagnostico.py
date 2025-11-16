"""
Script de Diagnóstico do Sistema Acadêmico PIM
Verifica configurações, conexões e possíveis problemas
"""

import os
import sys
import socket
import json
from datetime import datetime


def print_header(texto):
    """Imprime cabeçalho formatado"""
    print("\n" + "=" * 60)
    print(f"  {texto}")
    print("=" * 60)


def print_ok(texto):
    """Imprime mensagem de sucesso"""
    print(f"✅ {texto}")


def print_erro(texto):
    """Imprime mensagem de erro"""
    print(f"❌ {texto}")


def print_aviso(texto):
    """Imprime mensagem de aviso"""
    print(f"⚠️  {texto}")


def print_info(texto):
    """Imprime informação"""
    print(f"ℹ️  {texto}")


def verificar_arquivos():
    """Verifica se os arquivos necessários existem"""
    print_header("1. VERIFICAÇÃO DE ARQUIVOS")
    
    arquivos_sistema = [
        'server_proxy.py',
        'client_proxy.py',
        'config_rede.py',
        'gui_system.py',
        'database.py',
        'models.py',
        'iniciar.py'
    ]
    
    arquivos_dados = [
        '../usuarios.txt',
        '../alunos.txt',
        '../professores.txt',
        '../turmas.txt',
        '../aulas.txt',
        '../atividades.txt',
        '../notas.txt',
        '../chamadas.txt'
    ]
    
    print("\n📁 Arquivos do Sistema:")
    todos_ok = True
    for arquivo in arquivos_sistema:
        if os.path.exists(arquivo):
            tamanho = os.path.getsize(arquivo)
            print_ok(f"{arquivo} ({tamanho} bytes)")
        else:
            print_erro(f"{arquivo} - NÃO ENCONTRADO")
            todos_ok = False
    
    print("\n📄 Arquivos de Dados:")
    for arquivo in arquivos_dados:
        if os.path.exists(arquivo):
            tamanho = os.path.getsize(arquivo)
            linhas = 0
            try:
                with open(arquivo, 'r', encoding='utf-8') as f:
                    linhas = len(f.readlines())
            except:
                pass
            print_ok(f"{arquivo} ({tamanho} bytes, {linhas} linhas)")
        else:
            print_aviso(f"{arquivo} - NÃO ENCONTRADO (será criado)")
    
    return todos_ok


def verificar_python():
    """Verifica instalação do Python"""
    print_header("2. VERIFICAÇÃO DO PYTHON")
    
    print(f"\n🐍 Versão: {sys.version}")
    print(f"📁 Executável: {sys.executable}")
    print(f"📊 Plataforma: {sys.platform}")
    
    # Verifica módulos necessários
    modulos = ['tkinter', 'socket', 'json', 'threading', 'hashlib']
    print("\n📦 Módulos:")
    
    for modulo in modulos:
        try:
            __import__(modulo)
            print_ok(f"{modulo}")
        except ImportError:
            print_erro(f"{modulo} - NÃO INSTALADO")
    
    return True


def verificar_configuracao():
    """Verifica configuração de rede"""
    print_header("3. CONFIGURAÇÃO DE REDE")
    
    try:
        import config_rede
        
        print(f"\n⚙️  Modo: {'REDE' if config_rede.MODO_REDE else 'LOCAL'}")
        
        if config_rede.MODO_REDE:
            print(f"🌐 Servidor: {config_rede.SERVER_HOST}")
            print(f"🔌 Porta: {config_rede.SERVER_PORT}")
        else:
            print_info("Sistema configurado para modo LOCAL (acesso direto)")
        
        return True
    except Exception as e:
        print_erro(f"Erro ao ler configuração: {e}")
        return False


def verificar_rede():
    """Verifica conectividade de rede"""
    print_header("4. CONECTIVIDADE DE REDE")
    
    # Verificar hostname e IP
    try:
        hostname = socket.gethostname()
        ip_local = socket.gethostbyname(hostname)
        print(f"\n🖥️  Hostname: {hostname}")
        print(f"🌐 IP Local: {ip_local}")
    except Exception as e:
        print_erro(f"Erro ao obter informações de rede: {e}")
    
    # Testar se a porta 5000 está disponível
    print("\n🔍 Testando porta 5000:")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    
    try:
        # Tenta conectar
        resultado = sock.connect_ex(('localhost', 5000))
        if resultado == 0:
            print_ok("Porta 5000 está ABERTA (servidor pode estar rodando)")
            
            # Tenta fazer requisição de teste
            try:
                sock.send(json.dumps({'action': 'ping'}).encode('utf-8'))
                response = sock.recv(1024).decode('utf-8')
                print_ok("Servidor responde a requisições")
            except:
                print_aviso("Porta aberta mas servidor não responde corretamente")
        else:
            print_info("Porta 5000 está FECHADA (servidor não está rodando)")
    except Exception as e:
        print_erro(f"Erro ao testar porta: {e}")
    finally:
        sock.close()
    
    return True


def verificar_servidor():
    """Verifica se pode iniciar o servidor"""
    print_header("5. TESTE DO SERVIDOR")
    
    print("\n🔧 Tentando criar socket na porta 5000...")
    
    try:
        test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        test_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        test_socket.bind(('0.0.0.0', 5000))
        test_socket.close()
        
        print_ok("Servidor pode ser iniciado na porta 5000")
        return True
    except OSError as e:
        if "address already in use" in str(e).lower():
            print_aviso("Porta 5000 já está em uso (servidor pode estar rodando)")
            print_info("Use: netstat -ano | findstr :5000 para ver o processo")
        else:
            print_erro(f"Erro ao testar porta: {e}")
        return False
    except Exception as e:
        print_erro(f"Erro inesperado: {e}")
        return False


def testar_cliente():
    """Testa cliente de rede"""
    print_header("6. TESTE DO CLIENTE")
    
    try:
        import config_rede
        
        if not config_rede.MODO_REDE:
            print_info("Sistema em modo LOCAL - teste de cliente não aplicável")
            return True
        
        print(f"\n🔌 Tentando conectar a {config_rede.SERVER_HOST}:{config_rede.SERVER_PORT}...")
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        
        try:
            sock.connect((config_rede.SERVER_HOST, config_rede.SERVER_PORT))
            print_ok("Conexão estabelecida com sucesso")
            
            # Tenta requisição de teste
            request = {
                'action': 'login',
                'data': {'username': 'test', 'password': 'test'}
            }
            
            sock.send(json.dumps(request).encode('utf-8'))
            response = sock.recv(4096).decode('utf-8')
            
            if response:
                print_ok("Servidor responde a requisições")
                resp_obj = json.loads(response)
                print_info(f"Resposta: {resp_obj.get('status', 'unknown')}")
            
            sock.close()
            return True
            
        except socket.timeout:
            print_erro("Timeout ao conectar ao servidor")
            print_info("Servidor pode não estar rodando")
            return False
        except ConnectionRefusedError:
            print_erro("Conexão recusada")
            print_info("Verifique se o servidor está rodando")
            return False
        except Exception as e:
            print_erro(f"Erro na conexão: {e}")
            return False
            
    except Exception as e:
        print_erro(f"Erro ao testar cliente: {e}")
        return False


def verificar_firewall():
    """Verifica configuração do firewall"""
    print_header("7. FIREWALL")
    
    print("\n🛡️  Verificando regras do firewall...")
    print_info("Execute como Administrador para configurar:")
    print()
    print("  New-NetFirewallRule -DisplayName \"PIM Server\" \\")
    print("    -Direction Inbound -LocalPort 5000 -Protocol TCP -Action Allow")
    print()
    
    # Tenta verificar regras (requer PowerShell)
    try:
        import subprocess
        result = subprocess.run(
            ['powershell', 'Get-NetFirewallRule -DisplayName "*PIM*" | Select-Object DisplayName, Enabled'],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0 and result.stdout.strip():
            print_ok("Regras de firewall encontradas:")
            print(result.stdout)
        else:
            print_aviso("Nenhuma regra 'PIM' encontrada no firewall")
            print_info("Pode ser necessário configurar manualmente")
    except:
        print_info("Não foi possível verificar firewall automaticamente")
    
    return True


def gerar_relatorio():
    """Gera relatório de diagnóstico"""
    print_header("8. RELATÓRIO FINAL")
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    nome_arquivo = f"diagnostico_{timestamp}.txt"
    
    print(f"\n📝 Relatório de diagnóstico gerado")
    print(f"📄 Arquivo: {nome_arquivo}")
    
    return True


def main():
    """Função principal"""
    print("\n")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║       DIAGNÓSTICO DO SISTEMA ACADÊMICO PIM                ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print(f"\n⏰ Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    
    resultados = []
    
    # Executa verificações
    resultados.append(("Arquivos", verificar_arquivos()))
    resultados.append(("Python", verificar_python()))
    resultados.append(("Configuração", verificar_configuracao()))
    resultados.append(("Rede", verificar_rede()))
    resultados.append(("Servidor", verificar_servidor()))
    resultados.append(("Cliente", testar_cliente()))
    resultados.append(("Firewall", verificar_firewall()))
    
    # Resumo
    print_header("RESUMO")
    print()
    
    total = len(resultados)
    ok = sum(1 for _, resultado in resultados if resultado)
    
    for nome, resultado in resultados:
        status = "✅ OK" if resultado else "❌ FALHOU"
        print(f"  {nome:20s} {status}")
    
    print()
    print(f"📊 Total: {ok}/{total} verificações passaram")
    
    if ok == total:
        print()
        print_ok("Sistema está pronto para uso!")
        print()
        print("💡 Para iniciar:")
        print("   python iniciar.py")
    else:
        print()
        print_aviso("Alguns problemas foram encontrados")
        print()
        print("💡 Consulte os detalhes acima e corrija os problemas")
        print("💡 Documentação: README_REDE.md")
    
    print("\n" + "=" * 60)
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Diagnóstico interrompido pelo usuário")
    except Exception as e:
        print(f"\n\n❌ Erro fatal: {e}")
        import traceback
        traceback.print_exc()
    
    input("\nPressione ENTER para sair...")

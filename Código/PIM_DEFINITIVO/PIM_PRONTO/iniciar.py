"""
Script de Inicialização do Sistema Acadêmico PIM
Facilita a escolha entre servidor e cliente
"""

import os
import sys
import subprocess


def limpar_tela():
    """Limpa a tela do terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')


def exibir_menu():
    """Exibe menu principal"""
    limpar_tela()
    print("╔════════════════════════════════════════════════════════════╗")
    print("║        SISTEMA ACADÊMICO PIM - INICIALIZAÇÃO              ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print()
    print("Escolha uma opção:")
    print()
    print("  1. Iniciar SERVIDOR PROXY (Máquina servidora)")
    print("  2. Iniciar CLIENTE (Interface Gráfica - Modo Local)")
    print("  3. Iniciar CLIENTE (Interface Gráfica - Modo Rede)")
    print("  4. Testar Conexão com Servidor")
    print("  5. Ver Configuração Atual")
    print("  6. Configurar IP do Servidor")
    print("  7. Iniciar Backup (C++)")
    print("  0. Sair")
    print()


def iniciar_servidor():
    """Inicia o servidor proxy"""
    limpar_tela()
    print("═" * 60)
    print("INICIANDO SERVIDOR PROXY...")
    print("═" * 60)
    print()
    print("⚠️  ATENÇÃO:")
    print("   - O servidor ficará rodando até você pressionar Ctrl+C")
    print("   - Mantenha esta janela aberta enquanto os clientes estiverem conectados")
    print("   - Configure o firewall para permitir a porta 5000")
    print()
    input("Pressione ENTER para continuar...")
    
    try:
        # Usa Python do venv se disponível, senão usa o do sistema
        venv_python = os.path.join(os.path.dirname(__file__), 'venv', 'Scripts', 'python.exe')
        python_exe = venv_python if os.path.exists(venv_python) else r'C:\Users\Assupero\AppData\Local\Programs\Python\Python313\python.exe'
        subprocess.run([python_exe, 'server_proxy.py'])
    except KeyboardInterrupt:
        print("\n\n✅ Servidor encerrado pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro ao iniciar servidor: {e}")
    
    input("\nPressione ENTER para voltar ao menu...")


def iniciar_cliente_local():
    """Inicia cliente em modo local"""
    import config_rede
    
    # Configura modo local
    with open('config_rede.py', 'r', encoding='utf-8') as f:
        conteudo = f.read()
    
    conteudo = conteudo.replace('MODO_REDE = True', 'MODO_REDE = False')
    
    with open('config_rede.py', 'w', encoding='utf-8') as f:
        f.write(conteudo)
    
    limpar_tela()
    print("═" * 60)
    print("INICIANDO CLIENTE - MODO LOCAL")
    print("═" * 60)
    print()
    print("✅ Configurado para acesso direto aos arquivos .txt")
    print()
    
    try:
        venv_python = os.path.join(os.path.dirname(__file__), 'venv', 'Scripts', 'python.exe')
        python_exe = venv_python if os.path.exists(venv_python) else r'C:\Users\Assupero\AppData\Local\Programs\Python\Python313\python.exe'
        subprocess.run([python_exe, 'gui_system.py'])
    except Exception as e:
        print(f"\n❌ Erro ao iniciar cliente: {e}")
    
    input("\nPressione ENTER para voltar ao menu...")


def iniciar_cliente_rede():
    """Inicia cliente em modo rede"""
    import config_rede
    
    limpar_tela()
    print("═" * 60)
    print("CONFIGURAÇÃO DO CLIENTE - MODO REDE")
    print("═" * 60)
    print()
    
    # Lê configuração atual
    with open('config_rede.py', 'r', encoding='utf-8') as f:
        conteudo = f.read()
    
    # Extrai IP atual
    import re
    match = re.search(r"SERVER_HOST = ['\"](.+?)['\"]", conteudo)
    ip_atual = match.group(1) if match else 'localhost'
    
    print(f"IP atual do servidor: {ip_atual}")
    print()
    novo_ip = input("Digite o novo IP do servidor (ENTER para manter): ").strip()
    
    if novo_ip:
        conteudo = re.sub(r"SERVER_HOST = ['\"](.+?)['\"]", f"SERVER_HOST = '{novo_ip}'", conteudo)
        ip_atual = novo_ip
    
    # Ativa modo rede
    conteudo = conteudo.replace('MODO_REDE = False', 'MODO_REDE = True')
    
    with open('config_rede.py', 'w', encoding='utf-8') as f:
        f.write(conteudo)
    
    limpar_tela()
    print("═" * 60)
    print("INICIANDO CLIENTE - MODO REDE")
    print("═" * 60)
    print()
    print(f"✅ Configurado para conectar ao servidor: {ip_atual}:5000")
    print()
    
    try:
        venv_python = os.path.join(os.path.dirname(__file__), 'venv', 'Scripts', 'python.exe')
        python_exe = venv_python if os.path.exists(venv_python) else r'C:\Users\Assupero\AppData\Local\Programs\Python\Python313\python.exe'
        subprocess.run([python_exe, 'gui_system.py'])
    except Exception as e:
        print(f"\n❌ Erro ao iniciar cliente: {e}")
    
    input("\nPressione ENTER para voltar ao menu...")


def testar_conexao():
    """Testa conexão com servidor"""
    limpar_tela()
    print("═" * 60)
    print("TESTE DE CONEXÃO")
    print("═" * 60)
    print()
    
    try:
        venv_python = os.path.join(os.path.dirname(__file__), 'venv', 'Scripts', 'python.exe')
        python_exe = venv_python if os.path.exists(venv_python) else r'C:\Users\Assupero\AppData\Local\Programs\Python\Python313\python.exe'
        subprocess.run([python_exe, 'client_proxy.py'])
    except Exception as e:
        print(f"\n❌ Erro ao executar teste: {e}")
    
    input("\nPressione ENTER para voltar ao menu...")


def ver_configuracao():
    """Mostra configuração atual"""
    limpar_tela()
    print("═" * 60)
    print("CONFIGURAÇÃO ATUAL")
    print("═" * 60)
    print()
    
    try:
        venv_python = os.path.join(os.path.dirname(__file__), 'venv', 'Scripts', 'python.exe')
        python_exe = venv_python if os.path.exists(venv_python) else r'C:\Users\Assupero\AppData\Local\Programs\Python\Python313\python.exe'
        subprocess.run([python_exe, 'config_rede.py'])
    except Exception as e:
        print(f"\n❌ Erro ao ler configuração: {e}")
    
    input("\nPressione ENTER para voltar ao menu...")


def configurar_ip():
    """Configura IP do servidor"""
    limpar_tela()
    print("═" * 60)
    print("CONFIGURAR IP DO SERVIDOR")
    print("═" * 60)
    print()
    
    # Lê configuração atual
    with open('config_rede.py', 'r', encoding='utf-8') as f:
        conteudo = f.read()
    
    # Extrai IP atual
    import re
    match = re.search(r"SERVER_HOST = ['\"](.+?)['\"]", conteudo)
    ip_atual = match.group(1) if match else 'localhost'
    
    print(f"IP atual: {ip_atual}")
    print()
    print("Exemplos:")
    print("  - localhost ou 127.0.0.1 (servidor na mesma máquina)")
    print("  - 192.168.1.100 (servidor em outra máquina da LAN)")
    print()
    
    novo_ip = input("Digite o novo IP do servidor: ").strip()
    
    if novo_ip:
        conteudo = re.sub(r"SERVER_HOST = ['\"](.+?)['\"]", f"SERVER_HOST = '{novo_ip}'", conteudo)
        
        with open('config_rede.py', 'w', encoding='utf-8') as f:
            f.write(conteudo)
        
        print()
        print(f"✅ IP atualizado para: {novo_ip}")
    else:
        print()
        print("⚠️  Nenhuma alteração foi feita")
    
    input("\nPressione ENTER para voltar ao menu...")


def iniciar_backup():
    """Inicia o sistema de backup em C++"""
    limpar_tela()
    print("═" * 60)
    print("SISTEMA DE BACKUP")
    print("═" * 60)
    print()
    
    backup_exe = os.path.join('..', 'backup_system.exe')
    
    if not os.path.exists(backup_exe):
        print("❌ Erro: backup_system.exe não encontrado")
        print()
        print("Você precisa compilar o arquivo backup_system.cpp primeiro:")
        print()
        print("  g++ -o backup_system.exe backup_system.cpp")
        print()
    else:
        print("Executando backup...")
        print()
        try:
            subprocess.run([backup_exe])
        except Exception as e:
            print(f"\n❌ Erro ao executar backup: {e}")
    
    input("\nPressione ENTER para voltar ao menu...")


def main():
    """Função principal"""
    while True:
        exibir_menu()
        
        opcao = input("Digite sua opção: ").strip()
        
        if opcao == '1':
            iniciar_servidor()
        elif opcao == '2':
            iniciar_cliente_local()
        elif opcao == '3':
            iniciar_cliente_rede()
        elif opcao == '4':
            testar_conexao()
        elif opcao == '5':
            ver_configuracao()
        elif opcao == '6':
            configurar_ip()
        elif opcao == '7':
            iniciar_backup()
        elif opcao == '0':
            limpar_tela()
            print("=" * 60)
            print("Obrigado por usar o Sistema Acadêmico PIM!")
            print("=" * 60)
            break
        else:
            input("\n❌ Opção inválida! Pressione ENTER para continuar...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n✅ Programa encerrado pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro fatal: {e}")
        input("\nPressione ENTER para sair...")

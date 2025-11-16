#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <ctime>
#include <filesystem>
#include <sstream>
#include <iomanip>

using namespace std;
namespace fs = std::filesystem;

// Classe para gerenciar o backup do sistema
class BackupSystem {
private:
    string sourceDir;           // Diretório dos arquivos de origem
    string backupDir;           // Diretório de destino do backup
    vector<string> arquivos;    // Lista de arquivos para backup

    // Obtém o caminho da área de trabalho do usuário
    string getDesktopPath() {
        // No Windows, a área de trabalho geralmente está em C:\Users\<username>\Desktop
        char* userProfile = nullptr;
        size_t len = 0;
        _dupenv_s(&userProfile, &len, "USERPROFILE");
        
        if (userProfile != nullptr) {
            string desktopPath = string(userProfile) + "\\Desktop";
            free(userProfile);
            return desktopPath;
        }
        return "";
    }

    // Obtém a data e hora atual formatada para o nome da pasta
    string getDateTime() {
        time_t now = time(0);
        tm timeinfo;
        localtime_s(&timeinfo, &now);
        
        stringstream ss;
        ss << "Backup_"
           << setfill('0') << setw(4) << (timeinfo.tm_year + 1900)
           << setw(2) << (timeinfo.tm_mon + 1)
           << setw(2) << timeinfo.tm_mday << "_"
           << setw(2) << timeinfo.tm_hour
           << setw(2) << timeinfo.tm_min
           << setw(2) << timeinfo.tm_sec;
        
        return ss.str();
    }

    // Copia um arquivo de origem para o destino
    bool copyFile(const string& source, const string& destination) {
        try {
            fs::copy_file(source, destination, fs::copy_options::overwrite_existing);
            return true;
        } catch (const fs::filesystem_error& e) {
            cerr << "Erro ao copiar arquivo: " << e.what() << endl;
            return false;
        }
    }

public:
    // Construtor: inicializa o diretório de origem
    BackupSystem(const string& srcDir) : sourceDir(srcDir) {
        // Lista dos arquivos de texto do sistema acadêmico
        arquivos = {
            "alunos.txt",
            "atividades.txt",
            "aulas.txt",
            "chamadas.txt",
            "notas.txt",
            "professores.txt",
            "turmas.txt",
            "usuarios.txt"
        };
    }

    // Realiza o backup dos arquivos
    bool executarBackup() {
        cout << "=== SISTEMA DE BACKUP ===" << endl;
        cout << "\nIniciando processo de backup...\n" << endl;

        // Obtém o caminho da área de trabalho
        string desktop = getDesktopPath();
        if (desktop.empty()) {
            cerr << "Erro: Não foi possível encontrar a área de trabalho." << endl;
            return false;
        }

        // Cria o diretório de backup com timestamp
        string nomeBackup = getDateTime();
        backupDir = desktop + "\\" + nomeBackup;

        try {
            if (!fs::exists(backupDir)) {
                fs::create_directories(backupDir);
                cout << "Diretório de backup criado: " << backupDir << "\n" << endl;
            }
        } catch (const fs::filesystem_error& e) {
            cerr << "Erro ao criar diretório de backup: " << e.what() << endl;
            return false;
        }

        // Copia cada arquivo para o diretório de backup
        int sucessos = 0;
        int falhas = 0;

        for (const auto& arquivo : arquivos) {
            string arquivoOrigem = sourceDir + "\\" + arquivo;
            string arquivoDestino = backupDir + "\\" + arquivo;

            cout << "Copiando: " << arquivo << "... ";

            if (fs::exists(arquivoOrigem)) {
                if (copyFile(arquivoOrigem, arquivoDestino)) {
                    cout << "[OK]" << endl;
                    sucessos++;
                } else {
                    cout << "[FALHA]" << endl;
                    falhas++;
                }
            } else {
                cout << "[ARQUIVO NÃO ENCONTRADO]" << endl;
                falhas++;
            }
        }

        // Relatório final
        cout << "\n=== RELATÓRIO DO BACKUP ===" << endl;
        cout << "Arquivos copiados com sucesso: " << sucessos << endl;
        cout << "Arquivos com falha: " << falhas << endl;
        cout << "Local do backup: " << backupDir << endl;

        return (falhas == 0);
    }

    // Exibe informações sobre o backup
    void exibirInformacoes() {
        cout << "\n=== INFORMAÇÕES DO SISTEMA ===" << endl;
        cout << "Diretório de origem: " << sourceDir << endl;
        cout << "Arquivos a serem copiados: " << arquivos.size() << endl;
        cout << "\nLista de arquivos:" << endl;
        for (const auto& arquivo : arquivos) {
            cout << "  - " << arquivo << endl;
        }
    }
};

int main() {
    // Configuração do console para exibir corretamente caracteres acentuados
    system("chcp 65001 > nul");

    // Define o diretório onde estão os arquivos de texto
    string diretorioOrigem = "c:\\Users\\Assupero\\Downloads\\PIM_PRONTO\\PIM_PRONTO";

    // Cria a instância do sistema de backup
    BackupSystem backup(diretorioOrigem);

    // Exibe menu
    cout << "\n╔═══════════════════════════════════════════╗" << endl;
    cout << "║   SISTEMA DE BACKUP - PIM ACADÊMICO      ║" << endl;
    cout << "╚═══════════════════════════════════════════╝" << endl;

    backup.exibirInformacoes();

    cout << "\nDeseja realizar o backup? (S/N): ";
    char opcao;
    cin >> opcao;

    if (opcao == 'S' || opcao == 's') {
        if (backup.executarBackup()) {
            cout << "\n✓ Backup concluído com sucesso!" << endl;
        } else {
            cout << "\n✗ Backup concluído com erros." << endl;
        }
    } else {
        cout << "\nBackup cancelado pelo usuário." << endl;
    }

    cout << "\nPressione Enter para sair...";
    cin.ignore();
    cin.get();

    return 0;
}

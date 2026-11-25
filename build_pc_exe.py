import os
import sys
import shutil
import subprocess

def main():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    agenda_pc_dir = os.path.join(root_dir, 'agenda_pc')
    icon_path = os.path.join(agenda_pc_dir, 'favicon.ico')
    releases_dir = os.path.join(root_dir, 'releases')
    os.makedirs(releases_dir, exist_ok=True)

    target_name = "Agenda-PC-v1.1.7"
    dist_dir = os.path.join(root_dir, "dist")
    build_dir = os.path.join(root_dir, "build")

    print("=" * 70)
    print(">> INICIANDO EMPACOTAMENTO DO EXECUTÁVEL WINDOWS (.EXE) PARA PC")
    print(f">> Versão: 1.1.7")
    print(f">> Diretório fonte: {agenda_pc_dir}")
    print(f">> Ícone: {icon_path}")
    print("=" * 70)

    # PyInstaller command
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconfirm",
        "--clean",
        "--onefile",
        "--windowed",
        f"--name={target_name}",
        f"--icon={icon_path}",
        f"--add-data={agenda_pc_dir};agenda_pc",
        "--collect-all=webview",
        "--hidden-import=pythonnet",
        "--hidden-import=clr",
        "--hidden-import=webview.platforms.edgechromium",
        "--hidden-import=webview.platforms.winforms",
        os.path.join(root_dir, "main_desktop.py")
    ]

    print(">> Executando comando PyInstaller:")
    print(" ".join(cmd))
    
    result = subprocess.run(cmd, cwd=root_dir)
    if result.returncode != 0:
        print("[ERRO] Falha no empacotamento com PyInstaller.")
        sys.exit(result.returncode)

    built_exe = os.path.join(dist_dir, f"{target_name}.exe")
    if not os.path.isfile(built_exe):
        print(f"[ERRO] Executável não encontrado em: {built_exe}")
        sys.exit(1)

    exe_size_mb = os.path.getsize(built_exe) / (1024 * 1024)
    print(f">> Executável gerado com sucesso: {built_exe} ({exe_size_mb:.2f} MB)")

    # Copy to releases folder and agenda_pc folder
    final_release_exe = os.path.join(releases_dir, f"{target_name}.exe")
    agenda_pc_exe = os.path.join(agenda_pc_dir, f"{target_name}.exe")

    shutil.copy2(built_exe, final_release_exe)
    shutil.copy2(built_exe, agenda_pc_exe)

    print(f">> Copiado para: {final_release_exe}")
    print(f">> Copiado para: {agenda_pc_exe}")
    print("=" * 70)
    print(">> EMPACOTAMENTO CONCLUÍDO COM SUCESSO!")
    print("=" * 70)

if __name__ == '__main__':
    main()

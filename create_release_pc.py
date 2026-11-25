import subprocess
import urllib.request
import json
import os
import sys

def get_git_token():
    p = subprocess.run(['git', 'credential', 'fill'], input='protocol=https\nhost=github.com\n', capture_output=True, text=True)
    creds = dict(line.split('=', 1) for line in p.stdout.splitlines() if '=' in line)
    token = creds.get('password')
    if not token:
        print("[ERRO] Token do GitHub não encontrado.")
        sys.exit(1)
    return token

def upload_asset_to_release(repo, token, rel_data, file_path, asset_name):
    upload_url_template = rel_data.get('upload_url')
    file_size = os.path.getsize(file_path)
    print(f">> Fazendo upload do binário '{asset_name}' ({file_size:,} bytes)...")

    # Delete existing asset if present
    assets = rel_data.get('assets', [])
    for a in assets:
        if a.get('name') == asset_name:
            print(f">> Asset '{asset_name}' já existe. Excluindo versão anterior...")
            del_req = urllib.request.Request(a.get('url'), headers={
                'Authorization': f'token {token}',
                'User-Agent': 'AgendaOficialBuild',
                'Accept': 'application/vnd.github.v3+json'
            }, method='DELETE')
            urllib.request.urlopen(del_req)
            print(">> Asset anterior excluído.")

    upload_url = upload_url_template.split('{')[0] + f'?name={asset_name}'

    with open(file_path, 'rb') as f:
        file_bytes = f.read()

    up_req = urllib.request.Request(upload_url, data=file_bytes, headers={
        'Authorization': f'token {token}',
        'User-Agent': 'AgendaOficialBuild',
        'Accept': 'application/vnd.github.v3+json',
        'Content-Type': 'application/octet-stream',
        'Content-Length': str(file_size)
    })

    with urllib.request.urlopen(up_req) as resp:
        asset_info = json.loads(resp.read().decode())
        download_url = asset_info.get('browser_download_url')
        print(f">> Upload concluído com sucesso: {download_url}")
        return download_url

def create_or_get_release(repo, token, tag, release_name, release_notes):
    req_check = urllib.request.Request(f'https://api.github.com/repos/{repo}/releases/tags/{tag}', headers={
        'Authorization': f'token {token}',
        'User-Agent': 'AgendaOficialBuild',
        'Accept': 'application/vnd.github.v3+json'
    })
    try:
        with urllib.request.urlopen(req_check) as resp:
            rel_data = json.loads(resp.read().decode())
            print(f">> Release com tag {tag} já existe! ID: {rel_data.get('id')}")
            return rel_data
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f">> Criando nova Release {tag} em {repo}...")
            payload = {
                'tag_name': tag,
                'target_commitish': 'main',
                'name': release_name,
                'body': release_notes,
                'draft': False,
                'prerelease': False
            }
            req = urllib.request.Request(f'https://api.github.com/repos/{repo}/releases', data=json.dumps(payload).encode('utf-8'), headers={
                'Authorization': f'token {token}',
                'User-Agent': 'AgendaOficialBuild',
                'Accept': 'application/vnd.github.v3+json',
                'Content-Type': 'application/json'
            })
            with urllib.request.urlopen(req) as resp:
                rel_data = json.loads(resp.read().decode())
                print(f">> Release {tag} criada com sucesso! ID: {rel_data.get('id')}")
                return rel_data
        else:
            raise

def main():
    token = get_git_token()
    repo = 'Douglas3m/agenda-oficial'
    
    tag_pc = 'v1.1.7-pc'
    release_name_pc = 'Agenda Oficial PC v1.1.7 (Desktop Windows)'
    notes_file_pc = r'D:\agenda_app\RELEASE_NOTES_PC_v1.1.7.md'

    with open(notes_file_pc, 'r', encoding='utf-8') as f:
        release_notes = f.read()

    exe_path = r'D:\agenda_app\releases\Agenda-PC-v1.1.7.exe'
    if not os.path.isfile(exe_path):
        print(f"[ERRO] Arquivo {exe_path} não encontrado!")
        sys.exit(1)

    print("=" * 70)
    print(f">> Publicando Release PC ({tag_pc}) no GitHub...")
    rel_pc = create_or_get_release(repo, token, tag_pc, release_name_pc, release_notes)
    dl_url = upload_asset_to_release(repo, token, rel_pc, exe_path, 'Agenda-PC-v1.1.7.exe')

    # Also upload to v1.1.7 main release for cross-availability
    try:
        print(f">> Vinculando também na Release unificada v1.1.7...")
        rel_unified = create_or_get_release(repo, token, 'v1.1.7', 'Agenda vs 1.1.7', release_notes)
        upload_asset_to_release(repo, token, rel_unified, exe_path, 'Agenda-PC-v1.1.7.exe')
    except Exception as e:
        print(f">> Aviso ao vincular com release v1.1.7: {e}")

    print("=" * 70)
    print(">> TODAS AS RELEASES E BINÁRIOS FORAM PUBLICADOS COM SUCESSO!")
    print(f">> Release URL: {rel_pc.get('html_url')}")
    print(f">> Download Direto PC (.exe): {dl_url}")
    print("=" * 70)

if __name__ == '__main__':
    main()

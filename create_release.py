import subprocess
import urllib.request
import json
import os
import sys

def main():
    print(">> Obtendo credenciais do Git...")
    p = subprocess.run(['git', 'credential', 'fill'], input='protocol=https\nhost=github.com\n', capture_output=True, text=True)
    creds = dict(line.split('=', 1) for line in p.stdout.splitlines() if '=' in line)
    token = creds.get('password')

    if not token:
        print("[ERRO] Token do GitHub nao encontrado.")
        sys.exit(1)

    with open(r'D:\agenda_app\RELEASE_NOTES_v1.1.5.md', 'r', encoding='utf-8') as f:
        release_notes = f.read()

    repo = 'Douglas3m/agenda-oficial'
    print(f">> Verificando se release v1.1.5 ja existe em {repo}...")

    # Check if release already exists
    req_check = urllib.request.Request(f'https://api.github.com/repos/{repo}/releases/tags/v1.1.5', headers={
        'Authorization': f'token {token}',
        'User-Agent': 'AgendaOficialBuild',
        'Accept': 'application/vnd.github.v3+json'
    })
    rel_data = None
    try:
        with urllib.request.urlopen(req_check) as resp:
            rel_data = json.loads(resp.read().decode())
            print(f">> Release v1.1.5 ja existe! ID: {rel_data.get('id')}")
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(">> Criando nova Release oficial v1.1.5...")
            release_payload = {
                'tag_name': 'v1.1.5',
                'target_commitish': 'main',
                'name': 'Agenda vs 1.1.5',
                'body': release_notes,
                'draft': False,
                'prerelease': False
            }
            req = urllib.request.Request(f'https://api.github.com/repos/{repo}/releases', data=json.dumps(release_payload).encode('utf-8'), headers={
                'Authorization': f'token {token}',
                'User-Agent': 'AgendaOficialBuild',
                'Accept': 'application/vnd.github.v3+json',
                'Content-Type': 'application/json'
            })
            with urllib.request.urlopen(req) as resp:
                rel_data = json.loads(resp.read().decode())
                print(f">> Release criada com sucesso! ID: {rel_data.get('id')}")
        else:
            print("Erro:", e)
            sys.exit(1)

    upload_url_template = rel_data.get('upload_url')
    html_url = rel_data.get('html_url')
    print(f">> URL da Release: {html_url}")

    apk_path = r'D:\agenda_app\releases\Agenda-v1.1.5.apk'
    apk_size = os.path.getsize(apk_path)
    apk_name = 'Agenda-v1.1.5.apk'
    print(f">> Fazendo upload do binario APK ({apk_size:,} bytes) para os assets da Release...")

    # Check existing assets to avoid duplication
    assets = rel_data.get('assets', [])
    for a in assets:
        if a.get('name') == apk_name:
            print(f">> Asset {apk_name} ja existe na release! Deletando para re-upload limpo...")
            del_req = urllib.request.Request(a.get('url'), headers={
                'Authorization': f'token {token}',
                'User-Agent': 'AgendaOficialBuild',
                'Accept': 'application/vnd.github.v3+json'
            }, method='DELETE')
            urllib.request.urlopen(del_req)
            print(">> Asset antigo removido.")

    upload_url = upload_url_template.split('{')[0] + f'?name={apk_name}'

    with open(apk_path, 'rb') as f:
        apk_bytes = f.read()

    up_req = urllib.request.Request(upload_url, data=apk_bytes, headers={
        'Authorization': f'token {token}',
        'User-Agent': 'AgendaOficialBuild',
        'Accept': 'application/vnd.github.v3+json',
        'Content-Type': 'application/vnd.android.package-archive',
        'Content-Length': str(apk_size)
    })

    with urllib.request.urlopen(up_req) as resp:
        asset_data = json.loads(resp.read().decode())
        download_url = asset_data.get('browser_download_url')
        print("=" * 70)
        print(">> SUCESSO TOTAL NO UPLOAD DO APK!")
        print(f">> Repositorio: https://github.com/{repo}")
        print(f">> Release:     {html_url}")
        print(f">> Tag:         v1.1.5 (Agenda vs 1.1.5)")
        print(f">> Download APK: {download_url}")
        print("=" * 70)

if __name__ == '__main__':
    main()

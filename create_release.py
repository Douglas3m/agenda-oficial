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

    tag = 'v1.1.7'
    release_name = 'Agenda vs 1.1.7'
    notes_file = r'D:\agenda_app\RELEASE_NOTES_v1.1.7.md'

    with open(notes_file, 'r', encoding='utf-8') as f:
        release_notes = f.read()

    repo = 'Douglas3m/agenda-oficial'
    print(f">> Verificando se release {tag} ja existe em {repo}...")

    # Check if release already exists
    req_check = urllib.request.Request(f'https://api.github.com/repos/{repo}/releases/tags/{tag}', headers={
        'Authorization': f'token {token}',
        'User-Agent': 'AgendaOficialBuild',
        'Accept': 'application/vnd.github.v3+json'
    })
    rel_data = None
    try:
        with urllib.request.urlopen(req_check) as resp:
            rel_data = json.loads(resp.read().decode())
            print(f">> Release {tag} ja existe! ID: {rel_data.get('id')}")
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f">> Criando nova Release oficial {tag}...")
            release_payload = {
                'tag_name': tag,
                'target_commitish': 'main',
                'name': release_name,
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

    apk_path = rf'D:\agenda_app\releases\Agenda-{tag}.apk'
    apk_size = os.path.getsize(apk_path)
    apk_name = f'Agenda-{tag}.apk'
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
        print(f">> Tag:         {tag} ({release_name})")
        print(f">> Download APK: {download_url}")
        print("=" * 70)

if __name__ == '__main__':
    main()

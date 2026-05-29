#!/usr/bin/env python3
# ============================================================
# AXKA BUILDER - app.py
# Setup Menu CLI (dipindah dari server.js)
# ============================================================

import os
import sys
import json
import subprocess
import secrets
import signal

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
CONFIG_FILE = os.path.join(DATA_DIR, 'config.json')
ENV_FILE = os.path.join(BASE_DIR, '.env')

os.makedirs(DATA_DIR, exist_ok=True)


def load_config():
    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except Exception:
        return {
            'domain': 'localhost',
            'admin': 'AXKA',
            'password': 'Asiafone11',
            'email': 'admin@axkabuilder.com'
        }


def save_config(cfg):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(CONFIG_FILE, 'w') as f:
        json.dump(cfg, f, indent=2)


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def pause():
    input('\nTekan Enter untuk kembali...')


def menu():
    clear()
    print("""
=======================================
         AXKA BUILDER SETUP
=======================================

1. Install & Jalankan Website
2. Hanya Jalankan Server
3. Ganti Domain / Config
4. Ganti Admin Password
5. Perbaiki Dependencies (npm install)
6. Stop Website
7. Keluar
""")
    pilih = input('Pilih menu : ').strip()

    if pilih == '1':
        install_and_run()
    elif pilih == '2':
        start_server()
    elif pilih == '3':
        change_domain()
    elif pilih == '4':
        change_admin()
    elif pilih == '5':
        fix_deps()
    elif pilih == '6':
        stop_website()
    elif pilih == '7':
        print('\nSampai jumpa!\n')
        sys.exit(0)
    else:
        menu()


def install_and_run():
    clear()
    print('=== Install Website AXKA Builder ===\n')

    domain = input('[ • ] Domain (contoh: yourdomain.com) : ').strip()
    admin = input('[ • ] Username Admin                   : ').strip()
    password = input('[ • ] Password Admin                   : ').strip()
    email = input('[ • ] Email Admin                      : ').strip()

    print(f"""
╔══════════════════════════════════════╗
║          Konfirmasi Install          ║
╠══════════════════════════════════════╣
║  Domain   : {domain[:24]:<24}║
║  Admin    : {admin[:24]:<24}║
║  Password : {'*' * min(len(password), 24):<24}║
║  Email    : {email[:24]:<24}║
╚══════════════════════════════════════╝
""")

    confirm = input('Yakin menginstal? (y/n) : ').strip().lower()
    if confirm != 'y':
        clear()
        return menu()

    # Save config
    save_config({'domain': domain, 'admin': admin, 'password': password, 'email': email})

    # Create .env if not exists
    if not os.path.exists(ENV_FILE):
        jwt_secret = secrets.token_hex(32)
        admin_key = secrets.token_hex(16)
        env_content = f"""PORT=3000
NODE_ENV=production
JWT_SECRET={jwt_secret}
ADMIN_KEY={admin_key}
LOCAL_BUILD=true
LIMIT_FREE=5
LIMIT_PRO=80
# OpenRouter API Keys (7 key, fallback otomatis)
OR_KEY_1=
OR_KEY_2=
OR_KEY_3=
OR_KEY_4=
OR_KEY_5=
OR_KEY_6=
OR_KEY_7=
"""
        with open(ENV_FILE, 'w') as f:
            f.write(env_content)
        print('\n✅ File .env dibuat otomatis')

    # Install deps
    print('\n📦 Menginstall dependencies...\n')
    try:
        subprocess.run(['npm', 'install', '--production'], cwd=BASE_DIR, check=True)
        print('\n✅ Dependencies berhasil diinstall')
    except Exception as e:
        print(f'\n⚠️  npm install error: {e}')
        print('   Lanjut coba jalankan server...')

    print(f"""
✅ Website berhasil dikonfigurasi!

  Admin  : {admin}
  Pass   : {password}
  Domain : {domain}
  Port   : 3000

Server akan dijalankan sekarang...
""")
    input('Tekan Enter untuk mulai server...')
    start_server()


def start_server():
    print('\n🚀 Menjalankan server Node.js...\n')
    try:
        os.execvp('node', ['node', os.path.join(BASE_DIR, 'server.js'), '--server'])
    except Exception as e:
        print(f'Error menjalankan server: {e}')
        print('Coba jalankan manual: node server.js --server')
        pause()
        menu()


def change_domain():
    cfg = load_config()
    print(f'\nDomain saat ini: {cfg.get("domain", "-")}\n')
    new_domain = input('[ • ] Domain baru : ').strip()
    confirm = input('Yakin ganti domain? (y/n) : ').strip().lower()
    if confirm == 'y':
        cfg['domain'] = new_domain
        save_config(cfg)
        print(f'\n✅ Domain berhasil diubah ke: {new_domain}\n')
    pause()
    clear()
    menu()


def change_admin():
    cfg = load_config()
    new_admin = input(f'[ • ] Username Admin baru ({cfg.get("admin", "")}) : ').strip()
    new_password = input('[ • ] Password Admin baru              : ').strip()
    confirm = input('Yakin ganti data admin? (y/n) : ').strip().lower()
    if confirm == 'y':
        if new_admin:
            cfg['admin'] = new_admin
        if new_password:
            cfg['password'] = new_password
        save_config(cfg)
        print('\n✅ Data admin berhasil diubah\n')
    pause()
    clear()
    menu()


def fix_deps():
    print('\n📦 Menjalankan npm install...\n')
    try:
        subprocess.run(['npm', 'install'], cwd=BASE_DIR, check=True)
        print('\n✅ Dependencies berhasil diperbaiki\n')
    except Exception as e:
        print(f'\n❌ Error: {e}')
    pause()
    clear()
    menu()


def stop_website():
    confirm = input('Yakin ingin mematikan server? (y/n) : ').strip().lower()
    if confirm == 'y':
        print('\nServer dimatikan. Sampai jumpa!\n')
        # Kill node processes
        try:
            subprocess.run(['pkill', '-f', 'node server.js'], cwd=BASE_DIR)
        except Exception:
            pass
        sys.exit(0)
    clear()
    menu()


if __name__ == '__main__':
    # Inisialisasi default config jika belum ada
    if not os.path.exists(CONFIG_FILE):
        save_config({
            'domain': 'localhost',
            'admin': 'AXKA',
            'password': 'Asiafone11',
            'email': 'admin@axkabuilder.com'
        })
    menu()

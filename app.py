#!/usr/bin/env python3
# AXKA BUILDER - Setup Menu CLI (Cross-platform)

import os
import sys
import json
import subprocess
import secrets
import signal
import re
import platform

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
CONFIG_FILE = os.path.join(DATA_DIR, 'config.json')
ENV_FILE = os.path.join(BASE_DIR, '.env')
PID_FILE = os.path.join(DATA_DIR, 'server.pid')

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
    with open(CONFIG_FILE, 'w') as f:
        json.dump(cfg, f, indent=2)

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def pause():
    input('\nTekan Enter untuk kembali...')

def is_tool_available(name):
    """Cek apakah perintah (npm/node) tersedia di PATH"""
    try:
        subprocess.run([name, '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except FileNotFoundError:
        return False

def create_env_safely():
    """Buat .env jika belum ada, atau isi variabel yang hilang"""
    defaults = {
        'PORT': '3000',
        'NODE_ENV': 'production',
        'JWT_SECRET': secrets.token_hex(32),
        'ADMIN_KEY': secrets.token_hex(16),
        'LOCAL_BUILD': 'true',
        'LIMIT_FREE': '5',
        'LIMIT_PRO': '80',
        'OR_KEY_1': '',
        'OR_KEY_2': '',
        'OR_KEY_3': '',
        'OR_KEY_4': '',
        'OR_KEY_5': '',
        'OR_KEY_6': '',
        'OR_KEY_7': ''
    }
    
    if not os.path.exists(ENV_FILE):
        with open(ENV_FILE, 'w') as f:
            for key, val in defaults.items():
                f.write(f"{key}={val}\n")
        print('\n✅ File .env baru dibuat')
        return
    
    # Baca existing .env
    existing = {}
    with open(ENV_FILE, 'r') as f:
        for line in f:
            line = line.strip()
            if '=' in line and not line.startswith('#'):
                k, v = line.split('=', 1)
                existing[k] = v
    
    # Tambahkan yang belum ada
    added = False
    with open(ENV_FILE, 'a') as f:
        for key, val in defaults.items():
            if key not in existing:
                f.write(f"{key}={val}\n")
                added = True
    if added:
        print('\n✅ Variabel tambahan ditambahkan ke .env')

def stop_server_by_port(port=3000):
    """Hentikan proses yang menggunakan port tertentu (cross-platform)"""
    system = platform.system()
    pid = None
    
    try:
        if system == "Windows":
            # Cari PID dengan netstat
            result = subprocess.run(f'netstat -ano | findstr :{port}', shell=True, capture_output=True, text=True)
            for line in result.stdout.splitlines():
                if 'LISTENING' in line:
                    parts = line.split()
                    pid = parts[-1]
                    break
            if pid:
                subprocess.run(f'taskkill /F /PID {pid}', shell=True, capture_output=True)
                print(f"✅ Proses dengan PID {pid} telah dihentikan")
                return True
        else:  # Linux/macOS
            # Coba lsof terlebih dahulu
            result = subprocess.run(f'lsof -ti :{port}', shell=True, capture_output=True, text=True)
            if result.stdout.strip():
                pid = result.stdout.strip()
                subprocess.run(f'kill -9 {pid}', shell=True)
                print(f"✅ Proses dengan PID {pid} telah dihentikan")
                return True
            # Alternatif menggunakan ss atau netstat
            result = subprocess.run(f'ss -lptn | grep ":{port}"', shell=True, capture_output=True, text=True)
            if result.stdout:
                # Ekstrak PID dari output ss (format: users:(("node",pid=1234,fd=...))
                import re
                match = re.search(r'pid=(\d+)', result.stdout)
                if match:
                    pid = match.group(1)
                    subprocess.run(f'kill -9 {pid}', shell=True)
                    print(f"✅ Proses dengan PID {pid} telah dihentikan")
                    return True
    except Exception as e:
        print(f"❌ Gagal menghentikan server: {e}")
        return False
    
    # Coba PID file
    if os.path.exists(PID_FILE):
        try:
            with open(PID_FILE, 'r') as f:
                pid = int(f.read().strip())
                if system == "Windows":
                    subprocess.run(f'taskkill /F /PID {pid}', shell=True)
                else:
                    os.kill(pid, signal.SIGTERM)
                os.remove(PID_FILE)
                print(f"✅ Server dengan PID {pid} dihentikan via PID file")
                return True
        except:
            pass
    
    print(f"❌ Tidak ada proses ditemukan pada port {port}")
    return False

def start_server_background():
    """Jalankan server di background dan simpan PID"""
    if os.path.exists(PID_FILE):
        print("⚠️  Server mungkin sudah berjalan (file PID ada).")
        choice = input("Apakah tetap ingin menjalankan ulang? (y/n): ")
        if choice.lower() != 'y':
            return False
        try:
            with open(PID_FILE, 'r') as f:
                old_pid = int(f.read().strip())
                os.kill(old_pid, signal.SIGTERM)
        except:
            pass
        os.remove(PID_FILE)
    
    try:
        proc = subprocess.Popen(
            ['node', os.path.join(BASE_DIR, 'server.js')],
            cwd=BASE_DIR,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True  # detach
        )
        with open(PID_FILE, 'w') as f:
            f.write(str(proc.pid))
        print(f"\n🚀 Server berjalan di background (PID: {proc.pid})")
        print("   Gunakan menu Stop Website untuk menghentikannya.\n")
        return True
    except Exception as e:
        print(f"❌ Gagal menjalankan server: {e}")
        return False

def menu():
    while True:
        clear()
        print("""
=======================================
         AXKA BUILDER SETUP
=======================================

1. Install & Jalankan Website
2. Hanya Jalankan Server (Background)
3. Hanya Jalankan Server (Foreground - log tampil)
4. Ganti Domain / Config
5. Ganti Admin Password
6. Perbaiki Dependencies (npm install)
7. Stop Website
8. Keluar
""")
        pilih = input('Pilih menu : ').strip()
        
        if pilih == '1':
            install_and_run()
        elif pilih == '2':
            if start_server_background():
                pause()
        elif pilih == '3':
            start_server_foreground()
        elif pilih == '4':
            change_domain()
        elif pilih == '5':
            change_admin()
        elif pilih == '6':
            fix_deps()
        elif pilih == '7':
            stop_website()
        elif pilih == '8':
            print('\nSampai jumpa!\n')
            sys.exit(0)
        else:
            print("Pilihan tidak valid!")
            pause()

def install_and_run():
    clear()
    print('=== Install Website AXKA Builder ===\n')
    
    # Validasi toolchain
    if not is_tool_available('npm'):
        print("❌ npm tidak ditemukan. Pastikan Node.js dan npm sudah terinstal.")
        pause()
        return
    if not is_tool_available('node'):
        print("❌ node tidak ditemukan. Pastikan Node.js sudah terinstal.")
        pause()
        return
    
    while True:
        domain = input('[ • ] Domain (contoh: yourdomain.com) : ').strip()
        if domain and re.match(r'^[a-zA-Z0-9.-]+$', domain):
            break
        print("   Domain tidak valid. Gunakan huruf, angka, titik, atau strip.")
    
    admin = input('[ • ] Username Admin                   : ').strip()
    while not admin:
        admin = input('   Username tidak boleh kosong : ').strip()
    
    password = input('[ • ] Password Admin                   : ').strip()
    while not password:
        password = input('   Password tidak boleh kosong : ').strip()
    
    email = input('[ • ] Email Admin                      : ').strip()
    if not email:
        email = 'admin@axkabuilder.com'
    
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
        return
    
    save_config({'domain': domain, 'admin': admin, 'password': password, 'email': email})
    create_env_safely()
    
    print('\n📦 Menginstall dependencies...\n')
    try:
        subprocess.run(['npm', 'install', '--production'], cwd=BASE_DIR, check=True)
        print('\n✅ Dependencies berhasil diinstall')
    except subprocess.CalledProcessError:
        print('\n⚠️  npm install gagal. Coba jalankan "npm install" manual nanti.')
    
    print(f"""
✅ Website berhasil dikonfigurasi!

  Admin  : {admin}
  Pass   : {password}
  Domain : {domain}
  Port   : 3000

Silakan jalankan server dari menu utama.
""")
    pause()

def start_server_foreground():
    """Jalankan server dengan mengganti proses (seperti asli)"""
    print('\n🚀 Menjalankan server Node.js (foreground)...')
    print('   Tekan Ctrl+C untuk menghentikan server.\n')
    try:
        os.execvp('node', ['node', os.path.join(BASE_DIR, 'server.js')])
    except Exception as e:
        print(f'Error menjalankan server: {e}')
        pause()

def change_domain():
    cfg = load_config()
    print(f'\nDomain saat ini: {cfg.get("domain", "-")}')
    new_domain = input('[ • ] Domain baru : ').strip()
    if new_domain:
        cfg['domain'] = new_domain
        save_config(cfg)
        print(f'\n✅ Domain berhasil diubah ke: {new_domain}')
    else:
        print('\n⏭️  Domain tidak diubah.')
    pause()

def change_admin():
    cfg = load_config()
    new_admin = input(f'[ • ] Username Admin baru ({cfg.get("admin", "")}) : ').strip()
    new_password = input('[ • ] Password Admin baru              : ').strip()
    if new_admin:
        cfg['admin'] = new_admin
    if new_password:
        cfg['password'] = new_password
    if new_admin or new_password:
        save_config(cfg)
        print('\n✅ Data admin berhasil diubah')
    else:
        print('\n⏭️  Tidak ada perubahan.')
    pause()

def fix_deps():
    print('\n📦 Menjalankan npm install...\n')
    try:
        subprocess.run(['npm', 'install'], cwd=BASE_DIR, check=True)
        print('\n✅ Dependencies berhasil diperbaiki')
    except subprocess.CalledProcessError:
        print('\n❌ npm install gagal. Periksa koneksi internet dan file package.json.')
    pause()

def stop_website():
    confirm = input('Yakin ingin mematikan server? (y/n) : ').strip().lower()
    if confirm == 'y':
        if stop_server_by_port(3000):
            print('Server berhasil dihentikan.')
        else:
            print('Tidak ada server yang terdeteksi atau gagal dihentikan.')
        if os.path.exists(PID_FILE):
            try:
                os.remove(PID_FILE)
            except:
                pass
        pause()
    else:
        print('Dibatalkan.')

if __name__ == '__main__':
    if not os.path.exists(CONFIG_FILE):
        save_config({
            'domain': 'localhost',
            'admin': 'AXKA',
            'password': 'Asiafone11',
            'email': 'admin@axkabuilder.com'
        })
    menu()
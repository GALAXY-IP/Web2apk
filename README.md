# AXKA Builder v3.0

Platform lengkap untuk Build APK, Clone Website, AI Assistant, dan berbagai tools lainnya.

## 🚀 Quick Start

### Setup (pertama kali)
```bash
python3 app.py
```
Pilih menu **1. Install & Jalankan Website** dan ikuti instruksinya.

### Jalankan Server
```bash
node server.js
# atau
python3 app.py  → pilih menu 2
```

---

## 🔑 Default Admin
- **Username:** AXKA
- **Password:** Asiafone11

Login admin via tombol **"Admin"** di website, bukan melalui form login biasa.

---

## 🤖 OpenRouter API Keys

Isi minimal 1 key di `.env`. Sistem akan fallback otomatis ke key lain jika ada yang error.

```env
OR_KEY_1=sk-or-v1-xxx
OR_KEY_2=sk-or-v1-xxx
...
OR_KEY_7=sk-or-v1-xxx
```

Daftar gratis di: https://openrouter.ai

---

## 💰 Harga & Paket

| Paket | Harga | Durasi | Limit Build | AI Limit |
|-------|-------|--------|-------------|----------|
| Free  | Rp0   | -      | 5/hari      | 10/2jam  |
| Pro   | Rp2.000 | 1 bulan | 80/hari | 80/2jam  |
| ProMax | Rp5.000 | 2 bulan | Unlimited | Unlimited |

**Pembayaran ke:** 082320884089 (DANA/OVO/GoPay) a/n AXKAPROJECT

---

## 📁 Struktur File

```
axka_builder/
├── server.js          ← Server utama (tanpa menu)
├── app.py             ← Setup menu CLI
├── database.js        ← Database JSON
├── .env               ← Konfigurasi
├── routes/
│   ├── ai.js          ← AI Assistant (OpenRouter, 7 key)
│   ├── admin.js       ← Panel admin
│   ├── auth.js        ← Login/Register
│   ├── chat.js        ← Chat user-admin
│   ├── user.js        ← Profil & riwayat
│   └── ...
└── public/
    └── index.html     ← Frontend
```

---

## ⚙️ Environment Variables

Lihat `.env.example` untuk daftar lengkap.

---

## 🛠️ Admin Panel

Fitur admin (login dengan username AXKA / password Asiafone11):
- 👁️ Lihat semua user, jumlah build, jumlah akun
- 🔄 Ubah role user (free/pro/promax) - real-time
- 🔓 Unlock fitur untuk user
- 🚫 Ban/unban user
- ✅ Verifikasi pembayaran
- 💬 Chat dengan semua user
- ⚙️ Pengaturan limit global

---

BY AXKAPROJECT

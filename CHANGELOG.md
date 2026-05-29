# AXKA Builder v3.1.0 - Changelog

## 🔥 Fitur Baru

### Firebase Real-time Integration
- Chat antara user dan admin sekarang **real-time** via Firebase Realtime Database
- Tidak ada lagi delay 5 detik (polling dihapus untuk user Firebase)
- Status online user tampil di admin panel
- Fallback otomatis ke polling API jika Firebase belum dikonfigurasi

### Google Login (Firebase Auth)
- Login dengan akun Google menggunakan Firebase `signInWithPopup`
- Auto-create akun baru saat login Google pertama kali
- Endpoint baru: `POST /api/auth/google-firebase`

### API Key Universal
- API Key sekarang bisa dipakai untuk **semua tools**, bukan hanya APK Builder:
  - `POST /api/apk/build-api` - Build APK
  - `POST /api/ai/chat` - AI Assistant
  - `POST /api/remove-bg` - Remove Background
  - `POST /api/upscale` - Upscale Gambar
  - `POST /api/scrape-html` - Clone HTML Website
  - `POST /api/download/info` & `/video` - Media Downloader
  - `POST /api/arduino/compile` - Kompilasi Arduino
  - `POST /api/deploy` - Deploy Website (ProMax)
  - `GET /api/user/profile` & `/builds` - Info User
- Gunakan header: `X-API-Key: axkabuilder-xxxxxxxxx`

## 🐛 Bug Fixes

### Admin Panel Tidak Bisa Dibuka
- **Bug**: `adminKeyVal` dan `adminTokenVal` tidak pernah di-set setelah login
- **Fix**: Keduanya sekarang langsung di-set saat `adminLogin()` berhasil
- **Fix**: Admin session di-restore otomatis dari `localStorage` saat buka tab admin

### Profil Lama Masih Muncul Setelah Logout
- **Bug**: Setelah logout, username/email lama masih tampil di profil
- **Fix**: `doLogout()` sekarang me-reset semua field HTML + clear semua variabel
- **Fix**: Form login di-clear nilainya saat logout

### Google Login Tidak Berfungsi
- **Bug**: Fungsi `googleLoginFirebase()` belum didefinisikan
- **Fix**: Fungsi lengkap ditambahkan via Firebase module

### Admin Chat Tidak Real-time
- **Bug**: `adminTokenVal` undefined, semua API call gagal
- **Fix**: Variable diinisialisasi dan disinkronkan dengan benar

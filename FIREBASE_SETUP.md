# 🔥 Panduan Setup Firebase - AXKA Builder

## Mengapa Firebase?
- **Chat Real-time**: Pesan langsung muncul tanpa refresh (tidak perlu polling lagi)
- **Google Login**: Login satu klik via akun Google
- **Status Online**: Admin bisa lihat siapa yang sedang online

---

## Langkah 1: Buat Project Firebase

1. Buka [console.firebase.google.com](https://console.firebase.google.com)
2. Klik **"Add project"** → beri nama (contoh: `axka-builder`)
3. Matikan Google Analytics (opsional) → **Create project**

---

## Langkah 2: Aktifkan Realtime Database

1. Di sidebar kiri → **Build** → **Realtime Database**
2. Klik **"Create Database"**
3. Pilih lokasi: **asia-southeast1 (Singapore)**
4. Mode: **"Start in test mode"** (lalu perbaiki rules di bawah)
5. Klik **Enable**

### Rules Realtime Database (copy-paste ke tab Rules):
```json
{
  "rules": {
    "chats": {
      "$uid": {
        "messages": {
          ".read": "auth != null && (auth.uid == $uid || root.child('admins').child(auth.uid).exists())",
          ".write": "auth != null && (auth.uid == $uid || root.child('admins').child(auth.uid).exists())"
        }
      }
    },
    "presence": {
      "$uid": {
        ".read": "auth != null",
        ".write": "auth != null && auth.uid == $uid"
      }
    }
  }
}
```
> **Note:** Untuk testing awal, boleh pakai rules `".read": true, ".write": true` dulu.

---

## Langkah 3: Aktifkan Google Authentication

1. Di sidebar → **Build** → **Authentication**
2. Klik **"Get started"**
3. Tab **Sign-in method** → klik **Google**
4. Toggle **Enable** → pilih **Support email** → **Save**

---

## Langkah 4: Dapatkan Firebase Config

1. Di sidebar → klik ikon gear ⚙️ → **Project settings**
2. Scroll ke bawah ke **"Your apps"**
3. Klik ikon `</>` (Web app) → beri nama → **Register app**
4. Copy konfigurasi:

```javascript
const firebaseConfig = {
  apiKey: "AIzaSy...",
  authDomain: "axka-builder.firebaseapp.com",
  databaseURL: "https://axka-builder-default-rtdb.asia-southeast1.firebasedatabase.app",
  projectId: "axka-builder",
  storageBucket: "axka-builder.appspot.com",
  messagingSenderId: "123456789",
  appId: "1:123456789:web:abcdef"
};
```

---

## Langkah 5: Pasang Config di AXKA Builder

Edit file `public/index.html`, cari bagian:
```javascript
const firebaseConfig = {
  apiKey: "YOUR_FIREBASE_API_KEY",
  ...
};
```

Ganti dengan config yang didapat dari langkah 4.

---

## ✅ Selesai!

Setelah config diisi:
- Chat langsung **real-time** (tidak ada delay 5 detik)
- **Google Login** berfungsi
- Admin bisa lihat **status online** user
- Jika Firebase TIDAK dikonfigurasi, aplikasi tetap berjalan normal dengan polling API sebagai fallback

---

## 🐛 Troubleshooting

| Masalah | Solusi |
|---------|--------|
| "Firebase belum dikonfigurasi" | Isi `firebaseConfig` di `index.html` |
| Login Google popup langsung tutup | Tambahkan domain ke Authorized domains di Firebase Auth |
| Chat tidak real-time | Periksa Realtime Database rules |
| Error `auth/unauthorized-domain` | Auth → Settings → Authorized domains → tambahkan domain Anda |

---

## Authorized Domains
Jika deploy ke hosting, tambahkan domain ke:
**Firebase Console** → Authentication → Settings → Authorized domains

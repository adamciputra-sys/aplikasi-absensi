from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from datetime import datetime
import os
import urllib.request
import json
import io
from PIL import Image, ImageDraw

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ALLOWED_BSSIDS = ["00:11:22:33:44:55"]
os.makedirs("uploads", exist_ok=True)

# 1. Endpoint Utama: Menyajikan halaman web index.html saat link dibuka di browser
@app.get("/")
async def serve_index():
    return FileResponse("index.html")

def dapatkan_alamat(lat: str, lon: str) -> str:
    """Mengubah Latitude & Longitude menjadi Alamat Ringkas"""
    try:
        url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}"
        req = urllib.request.Request(url, headers={'User-Agent': 'AbsensiApp/1.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            alamat_full = data.get("display_name", "Alamat tidak ditemukan")
            return alamat_full[:60] + "..." if len(alamat_full) > 60 else alamat_full
    except Exception:
        return f"Lat: {lat}, Lon: {lon}"

def tambahkan_watermark(image_bytes: bytes, tanggal: str, alamat: str, tipe_absen: str) -> bytes:
    """Menambahkan Teks Tipe Absen, Tanggal, Jam, dan Alamat ke atas Foto"""
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    draw = ImageDraw.Draw(img)
    
    width, height = img.size
    
    # Latar belakang hitam untuk teks watermark
    banner_height = 65
    draw.rectangle([(0, height - banner_height), (width, height)], fill=(0, 0, 0))
    
    # Tulis teks Tipe Absen, Tanggal & Alamat
    teks = f"[{tipe_absen.upper()}] {tanggal}\nLokasi: {alamat}"
    draw.text((10, height - banner_height + 5), teks, fill=(255, 255, 255))
    
    output_buffer = io.BytesIO()
    img.save(output_buffer, format="JPEG", quality=90)
    return output_buffer.getvalue()

@app.post("/api/absensi")
async def simpan_absensi(
    bssid: str = Form(...),
    user_id: str = Form(...),
    tipe_absen: str = Form("Masuk"),  # Menerima Tipe Absensi (Masuk / Pulang)
    latitude: str = Form(None),
    longitude: str = Form(None),
    foto: UploadFile = File(...)
):
    if bssid not in ALLOWED_BSSIDS:
        raise HTTPException(status_code=403, detail="Gagal: Anda tidak terhubung ke WiFi Resmi Kantor!")

    sekarang = datetime.now()
    waktu_str = sekarang.strftime("%Y-%m-%d_%H-%M-%S")
    tanggal_tampil = sekarang.strftime("%d-%m-%Y %H:%M:%S")

    alamat_lengkap = "Lokasi tidak tersedia"
    if latitude and longitude:
        alamat_lengkap = dapatkan_alamat(latitude, longitude)

    foto_bytes = await foto.read()
    foto_berisi_teks = tambahkan_watermark(foto_bytes, tanggal_tampil, alamat_lengkap, tipe_absen)

    # Nama file foto disesuaikan dengan tipe absensinya
    file_path = f"uploads/absensi_{tipe_absen}_{user_id}_{waktu_str}.jpg"
    with open(file_path, "wb") as buffer:
        buffer.write(foto_berisi_teks)

    return {
        "status": "success",
        "message": f"Absen {tipe_absen} Berhasil pada {tanggal_tampil}!",
        "data": {
            "user_id": user_id,
            "tipe_absen": tipe_absen,
            "waktu_absensi": tanggal_tampil,
            "bssid": bssid,
            "alamat": alamat_lengkap,
            "foto_path": file_path
        }
    }
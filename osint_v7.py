# OSINT V7 - Ultra Fast & Smart Edition
# Fitur: Nama, Email, HLR, WA, Sosmed, Marketplace, Reverse Image, GPS Maps

import requests, re, urllib.parse, time, threading
from bs4 import BeautifulSoup
import os

def format_nomor(n):
    n = n.strip().replace(" ", "").replace("-", "")
    if n.startswith("0"): return "+62" + n[1:]
    if n.startswith("62"): return "+" + n
    return n if n.startswith("+") else "+" + n

def cari_info_google(nomor):
    try:
        q = urllib.parse.quote(nomor)
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(f"https://www.google.com/search?q={q}", headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        text = soup.get_text()
        nama = re.findall(r'([A-Z][a-z]+\s[A-Z][a-z]+)', text)
        email = re.findall(r'[\w.-]+@[\w.-]+', text)
        return nama[0] if nama else "-", list(set(email))[:3] if email else ["-"]
    except:
        return "(Error Nama)", ["(Error Email)"]

def hlr_lookup(n):
    try:
        url = f"https://www.ceebydith.com/operator/cek-hlr-lokasi-hp.php?nomor={n}"
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        hasil = soup.find("tr", class_="table-content")
        if hasil:
            text = hasil.text.strip()
            kota = re.search(r'Kota\s*:\s*(.*)', text)
            lokasi = kota.group(1) if kota else "-"
            maps = f"https://www.google.com/maps/search/{urllib.parse.quote(lokasi)}" if lokasi != "-" else "-"
            return text, maps
        return "-", "-"
    except:
        return "(Error HLR)", "-"

def wa_check(n):
    try:
        url = f"https://wa.me/{n.replace('+','')}"
        r = requests.get(url, allow_redirects=True, timeout=10)
        return "Aktif" if "whatsapp" in r.url else "Tidak Aktif"
    except:
        return "(Error WA)"

def social_check(n):
    user = n.replace("+", "")
    hasil = []
    try:
        if requests.get(f"https://t.me/{user}", timeout=10).status_code == 200:
            hasil.append("Telegram")
        if "facebook" in requests.get(f"https://www.facebook.com/search/top?q={user}", timeout=10).url:
            hasil.append("Facebook")
        if requests.get(f"https://www.instagram.com/{user}/", timeout=10).status_code == 200:
            hasil.append("Instagram")
    except:
        pass
    return hasil if hasil else ["-"]

def cek_olx(n):
    try:
        url = f"https://www.olx.co.id/items/q-{n}"
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=10)
        if n in r.text:
            lokasi_match = re.search(r'"location"\s*:\s*"([^"]+)"', r.text)
            lokasi = lokasi_match.group(1) if lokasi_match else "Ditemukan"
            maps = f"https://www.google.com/maps/search/{urllib.parse.quote(lokasi)}"
            return f"Ada ({lokasi})", maps
        return "Tidak Ada", "-"
    except:
        return "(Error OLX)", "-"

def cek_tokopedia(n):
    try:
        url = f"https://www.tokopedia.com/search?st=product&q={n}"
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        return "Ada" if n in r.text else "Tidak Ada"
    except:
        return "(Error Tokopedia)"

def cek_shopee(n):
    try:
        url = f"https://shopee.co.id/search?keyword={n}"
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        return "Ada" if n in r.text else "Tidak Ada"
    except:
        return "(Error Shopee)"

def proses(n):
    n = format_nomor(n)
    nama, email = cari_info_google(n)
    hlr, hlr_map = hlr_lookup(n)
    wa = wa_check(n)
    sosmed = social_check(n)
    olx, olx_map = cek_olx(n)
    toko = cek_tokopedia(n)
    shopee = cek_shopee(n)
    hasil = f"""📞 Nomor: {n}
👤 Nama: {nama}
📧 Email: {' | '.join(email)}
📍 Lokasi HLR: {hlr}
🗺️ Google Maps: {hlr_map}
💬 WhatsApp: {wa}
👥 Sosial Media: {' | '.join(sosmed)}
🛒 OLX: {olx}
🗺️ Maps OLX: {olx_map}
🏪 Tokopedia: {toko}
🛍️ Shopee: {shopee}"""
    return hasil


# ======= REVERSE IMAGE SEARCH =======
def reverse_image_search_gimage(image_path):
    try:
        search_url = "https://www.google.com/searchbyimage/upload"
        multipart = {
            'encoded_image': (image_path, open(image_path, 'rb')),
            'image_content': ''
        }
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.post(search_url, files=multipart, allow_redirects=False)
        fetch_url = response.headers.get("Location")
        if fetch_url:
            return f"Hasil Google Image:
{fetch_url}"
        return "Gagal mendapatkan hasil dari Google"
    except Exception as e:
        return f"Error Google Reverse Image: {str(e)}"

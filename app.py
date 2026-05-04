import streamlit as st
import pandas as pd
from datetime import datetime
import time

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="KOPASTAMA APP", layout="wide")

# --- CSS CUSTOM (TEMA BIRU MODERN & ANIMASI) ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to bottom, #001f3f, #007bff);
        color: white;
    }
    .stButton>button {
        border-radius: 20px;
        background-color: #00d1ff;
        color: #001f3f;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #ffffff;
        transform: scale(1.05);
    }
    .card {
        background: rgba(255, 255, 255, 0.1);
        padding: 20px;
        border-radius: 15px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- STATE MANAGEMENT (Penyimpanan Sementara) ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.user_name = ""
    st.session_state.kegiatan_aktif = False
    st.session_state.data_kegiatan = {}
    st.session_state.pesan_masuk = []

# --- FUNGSI SAPAAN OTOMATIS ---
def get_greeting(name):
    hour = datetime.now().hour
    if 5 <= hour < 11:
        greet = "Selamat Pagi"
    elif 11 <= hour < 15:
        greet = "Selamat Siang"
    elif 15 <= hour < 19:
        greet = "Selamat Sore"
    else:
        greet = "Selamat Malam"
    return f"Halo {name.capitalize()}, {greet}! 🌟"

# --- HALAMAN 1: LOGIN (GATEKEEPER) ---
if not st.session_state.logged_in:
    st.title("🛡️ KOPASTAMA GATEKEEPER")
    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("Selamat Datang, Silakan Masuk")
        
        input_nama = st.text_input("Nama Lengkap")
        
        # Logika Admin Easter Egg
        if input_nama.lower() == "adminkopastamakeren":
            password = st.text_input("Masukkan Password Admin", type="password")
            if st.button("Login Admin"):
                if password == "123065":
                    st.session_state.logged_in = True
                    st.session_state.role = "admin"
                    st.rerun()
                else:
                    st.error("Password Salah!")
        else:
            tgl_lahir = st.text_input("Tanggal Lahir (DD/MM/YYYY)", placeholder="Contoh: 17/08/1945")
            if st.button("Masuk Ke Akun"):
                # Di sini logika pengecekan database (Sederhana dulu)
                if input_nama and tgl_lahir:
                    st.session_state.logged_in = True
                    st.session_state.role = "user"
                    st.session_state.user_name = input_nama
                    st.rerun()
                else:
                    st.error("Nama atau Tanggal Lahir salah!")
                    with st.expander("Kirim Pesan ke Admin"):
                        pesan_teks = st.text_area("Jelaskan kendala kamu...")
                        if st.button("Kirim Pesan"):
                            st.session_state.pesan_masuk.append({"pengirim": input_nama, "isi": pesan_teks})
                            st.success("Pesan terkirim!")
        st.markdown("</div>", unsafe_allow_html=True)

# --- HALAMAN 2 & 3: DASHBOARD & ADMIN ---
else:
    # Sidebar untuk Logout
    st.sidebar.title("KOPASTAMA")
    st.sidebar.write(f"Login sebagai: {st.session_state.role.upper()}")
    if st.sidebar.button("Keluar (Logout)"):
        st.session_state.logged_in = False
        st.rerun()

    if st.session_state.role == "user":
        # Tampilan Iklan (Sederhana)
        if 'ad_closed' not in st.session_state:
            st.warning("📢 IKLAN: Dukung terus Organisasi Kopastama! [X]")
            if st.button("Tutup Iklan"):
                st.session_state.ad_closed = True
                st.rerun()

        st.markdown(f"### {get_greeting(st.session_state.user_name)}")
        
        tab_user = st.tabs(["📝 Absensi", "🤖 Smart AI", "ℹ️ Informasi"])
        
        with tab_user[0]:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.subheader("Papan Peringkat (Top 3)")
            st.write("🥇 Budi | 🥈 Ani | 🥉 Siti")
            with st.expander("Lihat Lainnya"):
                st.write("4. Agus | 5. Rina")
            
            # Logika Cek Kegiatan
            if st.session_state.kegiatan_aktif:
                st.success(f"Kegiatan Aktif: {st.session_state.data_kegiatan['nama']}")
                with st.form("absen_form"):
                    nama_absen = st.text_input("Nama (Otomatis Kapital)").upper()
                    ket = st.selectbox("Keterangan", ["Hadir", "Sakit", "Izin"])
                    if ket != "Hadir":
                        st.text_input("Keterangan Sakit/Izin")
                    if st.form_submit_button("Kirim Absensi"):
                        st.balloons()
                        st.success("Absensi Selesai!")
            else:
                st.error("Maaf, saat ini tidak ada kegiatan aktif.")
            st.markdown("</div>", unsafe_allow_html=True)

        with tab_user[1]:
            st.subheader("AI Smart Kopastama")
            st.text_input("Tanya AI Kopastama...")
            st.button("Tanya")

    elif st.session_state.role == "admin":
        st.title("Admin Control Panel")
        tab_admin = st.tabs(["👥 Data Anggota", "📊 Rekap", "📅 Tambah Kegiatan", "📩 Pesan"])
        
        with tab_admin[2]: # Tab Kegiatan
            st.subheader("Pengaturan Kegiatan")
            nama_keg = st.text_input("Nama Kegiatan Baru")
            jam_mulai = st.time_input("Mulai")
            jam_akhir = st.time_input("Selesai")
            
            col_admin = st.columns(2)
            if col_admin[0].button("HIDUPKAN KEGIATAN"):
                st.session_state.kegiatan_aktif = True
                st.session_state.data_kegiatan = {"nama": nama_keg, "mulai": jam_mulai, "akhir": jam_akhir}
                st.success("Kegiatan Berhasil Diaktifkan!")
            
            if col_admin[1].button("MATIKAN KEGIATAN"):
                st.session_state.kegiatan_aktif = False
                st.warning("Kegiatan Dihentikan.")

        with tab_admin[3]: # Tab Pesan
            st.subheader("Pesan Bantuan Masuk")
            if st.session_state.pesan_masuk:
                for p in st.session_state.pesan_masuk:
                    st.write(f"**{p['pengirim']}**: {p['isi']}")
            else:
                st.write("Belum ada pesan.")

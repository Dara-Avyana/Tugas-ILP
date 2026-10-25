# Tugas Kelompok Simulator ILP: Mitigasi Data Hazards (RAW, WAR, WAW)

**INF-1316 Organisasi dan Arsitektur Komputer** (Dosen : Pak Agung)

## Anggota Kelompok
1. **Dimas Adhi Prasetyo** (NIM: 51240004)
2. **Intan Cladia Sihombing** (NIM: 51240055) 
3. **Dara Ratu Avyana** (NIM: 51240058)
---

## 📌 Deskripsi Tugas & Jenis Dependensi
Berdasarkan materi perkuliahan, pengembangan simulator ILP pada Notebook ini mencakup deteksi dan simulasi tiga jenis *Data Hazards*:
1. **RAW (*Read After Write* / *True Data Dependence*):** Instruksi $Q$ membaca register yang sebelumnya ditulis oleh instruksi $P$ (Contoh: `I1: R1 = R2 + R3`, `I2: R4 = R1 + R5`).
2. **WAR (*Write After Read* / *Name Dependence - Anti-dependence*):** Instruksi $P$ membaca dari sebuah register, diikuti oleh instruksi $Q$ yang menulis ke register tersebut (Contoh: `I1: R1 = R2 + R3`, `I2: R2 = R4 + R5`).
3. **WAW (*Write After Write* / *Name Dependence - Output dependence*):** Instruksi $P$ dan $Q$ menulis ke register tujuan yang sama (Contoh: `I1: R1 = R2 + R3`, `I2: R1 = R4 + R5`).

## 🚀 Fitur yang Diimplementasikan di Notebook (`ILP.ipynb`)
- Deteksi otomatis dependensi **RAW**, **WAR**, dan **WAW** antar instruksi.
- Simulasi perbandingan siklus eksekusi sekuensial (*Sequential Execution*) vs eksekusi paralel (*ILP Execution*) beserta perhitungan *Speedup* dan *ILP Efficiency*.
- Pembuatan **Dependency Graph** secara visual menggunakan `networkx` dan `matplotlib`.

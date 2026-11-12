from main import muat_kb, forward_chaining, kesimpulan_akhir

kb = muat_kb("kb_lele.json")

KASUS = [
    ("1 rantai 3 tingkat (H2S)", ["DO di bawah 3 mg/L", "bau telur busuk dari dasar kolam", "aerasi kurang"],
     {"perlu aerasi dan sirkulasi untuk menekan H2S"}),
    ("2 negatif (fakta ada, tidak ada aturan cocok)", ["sisa pakan menumpuk", "aerasi kurang"], set()),
    ("3 amonia + hipoksia", ["DO di bawah 3 mg/L", "amonia di atas 0,02 mg/L", "sisa pakan menumpuk"],
     {"amonia berasal dari sisa pakan dan limbah ikan", "kondisi kritis, ikan berisiko stres dan mati"}),
    ("4 nitrit", ["nitrit di atas 0,1 mg/L"], {"nitrit berbahaya"}),
    ("5 mode atau (pH tinggi)", ["pH di atas 8,5"], {"pH di luar batas ideal"}),
    ("6 suhu", ["suhu di luar 25-30 C"], {"suhu di luar batas ideal"}),
]

gagal = 0
for nama, fakta, harapan in KASUS:
    _, asal, _ = forward_chaining(kb["aturan"], fakta)
    hasil = set(kesimpulan_akhir(asal))
    ok = hasil == harapan
    gagal += not ok
    print(("LULUS" if ok else "GAGAL"), nama, "->", sorted(hasil))
raise SystemExit(1 if gagal else 0)
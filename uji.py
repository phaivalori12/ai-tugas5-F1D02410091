from main import muat_kb, forward_chaining, kesimpulan_akhir

kb = muat_kb("kb_penyimpanan.json")

LEMARI = "SIMPAN DI LEMARI PENDINGIN"
KASUS = [
    ("1 sayuran berdaun (rantai R1->R2)", ["bahan sayuran berdaun"],
     {"SIMPAN DI LEMARI PENDINGIN: kantong plastik berlubang di laci sayur, terpisah dari buah"}),
    ("2 negatif (bahan tidak dicakup)", ["makanan tidak akan habis dalam 3-4 hari"], set()),
    ("3 makanan matang, tidak habis 4 hari", ["bahan makanan matang atau sisa makanan", "makanan tidak akan habis dalam 3-4 hari"],
     {"SIMPAN DI FREEZER: wadah tertutup dangkal, bagi dalam porsi kecil"}),
    ("4 makanan matang, habis 4 hari", ["bahan makanan matang atau sisa makanan", "makanan akan habis dalam 3-4 hari"],
     {"SIMPAN DI LEMARI PENDINGIN: wadah tertutup dangkal, habiskan dalam 3-4 hari"}),
    ("5 pisang", ["bahan pisang, tomat, ubi jalar, atau semangka utuh"],
     {"SIMPAN DI SUHU RUANG: jauhkan dari sinar matahari langsung, jangan di kulkas"}),
    ("6 pir belum matang", ["bahan pir belum matang"],
     {"SIMPAN DI SUHU RUANG sampai matang, jauhkan dari sinar matahari langsung"}),
    ("7 pir sudah matang", ["bahan pir sudah matang"], {LEMARI + " dan pakai dalam 1-3 hari"}),
    ("8 terpotong", ["buah atau sayur sudah dipotong atau dikupas"],
     {LEMARI + " segera setelah dipotong atau dikupas"}),
    ("9 kemasan dibuka + label kulkas", ["kemasan sudah dibuka", "label menyatakan simpan di kulkas setelah dibuka"],
     {LEMARI + " sesuai label setelah kemasan dibuka"}),
    ("10 label simpan beku", ["label menyatakan simpan beku"], {"SIMPAN DI FREEZER sesuai label (simpan beku)"}),
    ("11 dua kesimpulan (daun + terpotong)", ["bahan sayuran berdaun", "buah atau sayur sudah dipotong atau dikupas"],
     {"SIMPAN DI LEMARI PENDINGIN: kantong plastik berlubang di laci sayur, terpisah dari buah",
      LEMARI + " segera setelah dipotong atau dikupas"}),
    ("12 kemasan dibuka tanpa label kulkas (tidak ada kesimpulan)", ["kemasan sudah dibuka"], set()),
]

gagal = 0
for nama, fakta, harapan in KASUS:
    _, asal, _ = forward_chaining(kb["aturan"], fakta)
    hasil = set(kesimpulan_akhir(asal))
    ok = hasil == harapan
    gagal += not ok
    print(("LULUS" if ok else "GAGAL"), nama, "->", sorted(hasil))
raise SystemExit(1 if gagal else 0)

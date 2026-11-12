import argparse
import json


def muat_kb(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def syarat_terpenuhi(aturan, memori):
    ada = [s in memori for s in aturan["jika"]]
    return all(ada) if aturan["mode"] == "dan" else any(ada)


def forward_chaining(daftar_aturan, fakta_awal):
    memori = set(fakta_awal)
    asal = {}
    siklus = []
    while True:
        cocok = [r for r in daftar_aturan
                 if syarat_terpenuhi(r, memori) and r["maka"] not in memori]
        if not cocok:
            siklus.append((len(siklus) + 1, None))
            break
        r = cocok[0]  # ambil aturan pertama
        dasar = [s for s in r["jika"] if s in memori]  # bahan "alasan"
        memori.add(r["maka"])
        asal[r["maka"]] = (r, dasar)
        siklus.append((len(siklus) + 1, r))
    return memori, asal, siklus


def kesimpulan_akhir(asal):
    terpakai = set()
    for _, dasar in asal.values():
        terpakai.update(s for s in dasar if s in asal)
    return [k for k in asal if k not in terpakai]


def cetak_alasan(fakta, asal, indent=2):
    r, dasar = asal[fakta]
    sumber = ",".join(r["sumber"])
    print(f"{' ' * indent}{fakta}  <- {r['id']} ({', '.join(dasar)}) [sumber: {sumber}]")
    for s in dasar:
        if s in asal:
            cetak_alasan(s, asal, indent + 4)


def tanya_user(pertanyaan, jawaban_otomatis=None):
    fakta = []
    print("Jawab y/t.")
    for i, (teks, tanya) in enumerate(pertanyaan.items(), 1):
        while True:
            if jawaban_otomatis:
                j = jawaban_otomatis[i - 1].lower()
                print(f"{i}. {tanya} (y/t) > {j}")
            else:
                j = input(f"{i}. {tanya} (y/t) > ").strip().lower()
            if j in ("y", "t"):
                break
            print("   Ketik y atau t.")
        if j == "y":
            fakta.append(teks)
    return fakta


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kb", default="kb_lele.json")
    ap.add_argument("--jawab", help="string y/t, satu huruf per pertanyaan")
    args = ap.parse_args()

    kb = muat_kb(args.kb)
    n = len(kb["pertanyaan"])
    if args.jawab and len(args.jawab) != n:
        raise SystemExit(f"--jawab harus {n} huruf (y/t), dapat {len(args.jawab)}")

    print(kb["judul"])
    fakta_awal = tanya_user(kb["pertanyaan"], args.jawab)

    print("\nFakta awal:", ", ".join(fakta_awal) if fakta_awal else "(tidak ada)")
    print()
    memori, asal, siklus = forward_chaining(kb["aturan"], fakta_awal)
    for no, r in siklus:
        if r is None:
            print(f"Siklus {no}: tidak ada aturan baru, berhenti")
        else:
            print(f"Siklus {no}: {r['id']} -> {r['maka']}")

    akhir = kesimpulan_akhir(asal)
    print()
    if not akhir:
        print("Kesimpulan: tidak ada kesimpulan dari fakta yang diberikan")
    else:
        print("Kesimpulan:", "; ".join(akhir))
        print("Alasan:")
        for k in akhir:
            cetak_alasan(k, asal)
    print("\nCatatan:", kb["batas"])


if __name__ == "__main__":
    main()
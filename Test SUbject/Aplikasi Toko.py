print("=== Program Cek Harga ===")
produk = input ("Masukkan nama produk:")
harga = int(input("Masukkan harga produk:"))
jumlah = int(input("Masukkan Jumlah produk:" ))
stok = int(input("Masukkan stok produk:"))
if stok < 10:
    print("Peringatan: Stok hampir habis!, Segera lakukan restock")
elif stok > 100:
    print("peringatan: stok terlalu banyak!, segera lakukan promo")
total_biaya = harga * jumlah
persen_untung = float(input("Masukkan persen untung:"))
untung_per_produk = int((persen_untung / 100) * harga)
total_untung = untung_per_produk * jumlah
harga_jual_satuan = harga + untung_per_produk
total_harga_jual = total_biaya + total_untung
print(f"Total Biaya Modal: {total_biaya:,}".replace(",","."))
print(f"Untung per produk: {untung_per_produk:,}".replace(",","."))
print(f"Harga jual Per piece: {harga_jual_satuan:,}".replace(",","."))
if harga_jual_satuan < 5000:
    print("peringatan harga terlalu murah!, segra lakukan penyesuaian harga")
elif harga_jual_satuan > 10000:
    print("peringatan harga terlalu mahal!, segera lakukan penyesuaian harga")
print(f"Total Pendapatan: {total_harga_jual:,}".replace(",","."))
lagi = input("Apakah ingin menghitung lagi? (y/n): ")
lagi = "y"
while lagi == "y":
    produk = input ("Masukkan nama produk:")
    harga = int(input("Masukkan harga produk:"))
    jumlah = int(input("Masukkan Jumlah produk:" ))
    stok = int(input("Masukkan stok produk:"))
    if stok < 10:
        print("Peringatan: Stok hampir habis!, Segera lakukan restock")
    elif stok > 100:
        print("peringatan: stok terlalu banyak!, segera lakukan promo")
    total_biaya = harga * jumlah
    persen_untung = float(input("Masukkan persen untung:"))
    untung_per_produk = int((persen_untung / 100) * harga)
    total_untung = untung_per_produk * jumlah
    harga_jual_satuan = harga + untung_per_produk
    total_harga_jual = total_biaya + total_untung
    print(f"Total Biaya Modal: {total_biaya:,}".replace(",","."))
    print(f"Untung per produk: {untung_per_produk:,}".replace(",","."))
    print(f"Harga jual Per piece: {harga_jual_satuan:,}".replace(",","."))
    if harga_jual_satuan < 5000:
        print("peringatan harga terlalu murah!, segra lakukan penyesuaian harga")
    elif harga_jual_satuan > 10000:
        print("peringatan harga terlalu mahal!, segera lakukan penyesuaian harga")
    print(f"Total Pendapatan: {total_harga_jual:,}".replace(",","."))
    lagi = input("Apakah ingin menghitung lagi? (y/n): ")
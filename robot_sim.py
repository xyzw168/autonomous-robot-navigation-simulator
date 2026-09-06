# Autonomous Robot Navigation Simulator
arena = [
    ['.', '.', '.', '.', '.'],
    ['.', 'S', '.', '#', '.'],  
    ['.', '.', '.', '#', '.'],  
    ['.', '.', '.', '.', 'G'],
    ['.', '.', '.', '.', '.']
]

def print_arena(grid):
    """Fungsi untuk mencetak arena ke layar"""
    for row in grid:
        print(" ".join(row))
    print("-" * 15)

def cari_posisi_robot(grid):
    """Mencari koordinat (baris, kolom) si robot 'S'"""
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            if grid[r][c] == 'S':
                return (r, c)
    return None

def cek_sensor(grid, pos):
    """Fungsi sensor virtual untuk mendeteksi sekeliling robot"""
    r, c = pos
    atas = grid[r - 1][c] if r > 0 else "Batas"
    bawah = grid[r + 1][c] if r < len(grid) - 1 else "Batas"
    kiri = grid[r][c - 1] if c > 0 else "Batas"
    kanan = grid[r][c + 1] if c < len(grid[r]) - 1 else "Batas"
    return {"atas": atas, "bawah": bawah, "kiri": kiri, "kanan": kanan}

print("Kondisi Arena dengan Obstacle (#):")
print_arena(arena)

posisi_awal = cari_posisi_robot(arena)
print(f"Posisi robot (S) ada di: Baris {posisi_awal[0]}, Kolom {posisi_awal[1]}")

hasil_sensor = cek_sensor(arena, posisi_awal)

print("\n--- HASIL SENSOR ROBOT ---")
for arah, kondisi in hasil_sensor.items():
    status = "Ada Rintangan (#)" if kondisi == '#' else ("Batas Arena" if kondisi == "Batas" else "Aman (.)")
    print(f"Sensor arah {arah.upper()}: {status}")

print("\n--- KEPUTUSAN KONTROLER ROBOT ---")
if hasil_sensor["kanan"] == '.':
    print("Keputusan: Jalur kanan aman. Robot bergerak KE KANAN ➡️")
elif hasil_sensor["bawah"] == '.':
    print("Keputusan: Jalur kanan terhalang, jalur bawah aman. Robot bergerak KE BAWAH ⬇️")
else:
    print("Keputusan: Terhalang! Mencari arah alternatif 🔄")

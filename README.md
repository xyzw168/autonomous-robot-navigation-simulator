# Autonomous Robot Navigation Simulator

Proyek simulasi navigasi robot menggunakan Python pada arena grid 2D. Robot dapat membaca kondisi di sekitarnya menggunakan sensor virtual, mencari jalur menuju target menggunakan algoritma BFS dan A*, kemudian bergerak secara otomatis menuju target.

## Fitur

* Arena grid 2D dengan posisi awal, target, dan obstacle
* Sensor virtual untuk membaca kondisi di 4 arah
* Path planning menggunakan BFS
* Path planning menggunakan A*
* Heuristic Manhattan Distance
* Validasi gerakan robot
* Pergerakan robot secara otomatis
* Animasi pergerakan di terminal
* Perbandingan performa BFS dan A*

## Simbol pada Arena

* `S` = posisi awal
* `G` = target
* `#` = obstacle
* `.` = area yang bisa dilewati
* `·` = jejak pergerakan robot
* `*` = jalur hasil path planning

## Cara Kerja

1. Robot menentukan posisi awal `S` dan target `G`.
2. Sensor virtual membaca kondisi di sekitar robot.
3. Program mencari jalur dari `S` menuju `G` menggunakan BFS dan A*.
4. BFS mencari jalur terpendek tanpa heuristic.
5. A* menggunakan kombinasi jarak yang telah ditempuh dan heuristic Manhattan Distance untuk menentukan prioritas pencarian.
6. Jalur BFS digunakan sebagai acuan animasi pergerakan robot.
7. Setiap perpindahan robot divalidasi untuk memastikan gerakan tidak menabrak obstacle.
8. Program menampilkan perbandingan hasil BFS dan A*.

## BFS vs A*

BFS dan A* sama-sama dapat menemukan jalur terpendek pada arena dengan biaya perpindahan yang sama.

Perbedaan utamanya adalah cara menentukan posisi yang dieksplorasi:

* **BFS** mengeksplorasi berdasarkan jarak dari posisi awal.
* **A*** menggunakan `f(n) = g(n) + h(n)`.
* `g(n)` merupakan jarak yang telah ditempuh.
* `h(n)` merupakan perkiraan jarak menuju target menggunakan Manhattan Distance.

Pada contoh arena yang digunakan:

| Parameter    |        BFS |         A* |
| ------------ | ---------: | ---------: |
| Jalur        | 10 langkah | 10 langkah |
| Posisi dicek |         44 |         15 |
| Waktu proses | 0.000308 s | 0.000220 s |

Hasil tersebut menunjukkan bahwa kedua algoritma menemukan jalur dengan panjang yang sama, sementara A* mengeksplorasi lebih sedikit posisi pada arena pengujian.

## Hasil Simulasi

Berikut contoh hasil simulasi ketika robot berhasil mencapai target:

![Hasil Simulasi](screenshots/simulation.png)

## Tools

* Python 3
* BFS (*Breadth-First Search*)
* A* (*A-Star Search*)
* Manhattan Distance
* Virtual Sensor
* Path Planning
* `heapq`
* `collections.deque`

## Cara Menjalankan

Pastikan Python 3 sudah terinstal, kemudian jalankan:

```bash
python main.py
```

## Pengembangan Selanjutnya

* Menambahkan obstacle yang bergerak
* Membuat sensor dengan jangkauan yang lebih realistis
* Menambahkan visualisasi yang lebih interaktif
* Mengembangkan simulasi menuju sistem robot nyata
* Mengintegrasikan sensor dan kontroler dengan mikrokontroler

import os
import time
import heapq
from collections import deque

# arena
arena = [
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', 'S', '.', '#', '#', '.', '.', '.'],
    ['.', '.', '.', '#', '.', '.', '#', '.'],
    ['.', '#', '.', '#', '.', '#', '#', '.'],
    ['.', '#', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '#', '#', '.', '.', 'G'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
]

ROBOT = '🤖'
START = 'S'
GOAL = 'G'
OBSTACLE = '#'
EMPTY = '.'
PATH = '·'

ANIMATION_DELAY = 0.5


# tampilkan arena
def print_arena(grid, robot_pos=None, path=None, visited=None):
    os.system('cls' if os.name == 'nt' else 'clear')

    print("AUTONOMOUS ROBOT NAVIGATION SIMULATOR")

    path = path or set()
    visited = visited or set()

    for r in range(len(grid)):
        row = []

        for c in range(len(grid[r])):
            pos = (r, c)

            if pos == robot_pos:
                row.append(ROBOT)
            elif grid[r][c] == START:
                row.append(START)
            elif grid[r][c] == GOAL:
                row.append(GOAL)
            elif grid[r][c] == OBSTACLE:
                row.append(OBSTACLE)
            elif pos in visited:
                row.append(PATH)
            elif pos in path:
                row.append('*')
            else:
                row.append(EMPTY)

        print("   ".join(row))

    print("----------------------------------------")


# cari posisi S atau G
def cari_posisi(grid, simbol):
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            if grid[r][c] == simbol:
                return (r, c)

    return None


# sensor virtual
def baca_sensor(grid, pos):
    r, c = pos

    sensor = {
        "atas": None,
        "bawah": None,
        "kiri": None,
        "kanan": None
    }

    sensor["atas"] = grid[r - 1][c] if r > 0 else "Batas"
    sensor["bawah"] = grid[r + 1][c] if r < len(grid) - 1 else "Batas"
    sensor["kiri"] = grid[r][c - 1] if c > 0 else "Batas"
    sensor["kanan"] = grid[r][c + 1] if c < len(grid[r]) - 1 else "Batas"

    return sensor


# tampilkan sensor
def tampilkan_sensor(sensor):
    print("\n--- SENSOR ---")

    for arah, kondisi in sensor.items():
        if kondisi == EMPTY:
            status = "Aman"
        elif kondisi == OBSTACLE:
            status = "Obstacle"
        elif kondisi == GOAL:
            status = "Goal"
        elif kondisi == START:
            status = "Start"
        else:
            status = "Batas"

        print(f"{arah.capitalize():<6}: {status}")


# cari posisi yang bisa dilewati
def get_valid_neighbors(grid, pos):
    r, c = pos

    candidates = [
        (r - 1, c),
        (r + 1, c),
        (r, c - 1),
        (r, c + 1)
    ]

    neighbors = []

    for nr, nc in candidates:
        if 0 <= nr < len(grid) and 0 <= nc < len(grid[nr]):
            if grid[nr][nc] != OBSTACLE:
                neighbors.append((nr, nc))

    return neighbors


# BFS untuk mencari jalur terpendek
def bfs_shortest_path(grid, start, goal):
    queue = deque([start])
    visited = {start}
    parent = {start: None}

    explored = 0

    while queue:
        current = queue.popleft()
        explored += 1

        if current == goal:
            break

        for neighbor in get_valid_neighbors(grid, current):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)

    if goal not in parent:
        return None, explored

    path = []
    current = goal

    while current is not None:
        path.append(current)
        current = parent[current]

    path.reverse()

    return path, explored


# heuristic
def manhattan_distance(pos_a, pos_b):
    r1, c1 = pos_a
    r2, c2 = pos_b

    return abs(r1 - r2) + abs(c1 - c2)


# A* untuk mencari jalur terpendek 
def astar_shortest_path(grid, start, goal):
    open_set = [(manhattan_distance(start, goal), 0, start)]

    g_score = {start: 0}
    parent = {start: None}
    visited = set()

    explored = 0

    while open_set:
        _, current_g, current = heapq.heappop(open_set)

        if current in visited:
            continue

        visited.add(current)
        explored += 1

        if current == goal:
            break

        for neighbor in get_valid_neighbors(grid, current):
            tentative_g = current_g + 1

            if tentative_g < g_score.get(neighbor, float('inf')):
                g_score[neighbor] = tentative_g
                parent[neighbor] = current

                f_score = tentative_g + manhattan_distance(neighbor, goal)
                heapq.heappush(open_set, (f_score, tentative_g, neighbor))

    if goal not in parent:
        return None, explored

    path = []
    current = goal

    while current is not None:
        path.append(current)
        current = parent[current]

    path.reverse()

    return path, explored


# tentukan arah robot
def tentukan_arah(pos_lama, pos_baru):
    r1, c1 = pos_lama
    r2, c2 = pos_baru

    if r2 < r1:
        return "Atas ↑"
    elif r2 > r1:
        return "Bawah ↓"
    elif c2 < c1:
        return "Kiri ←"
    elif c2 > c1:
        return "Kanan →"

    return "Diam"


# cek apakah gerakan valid
def gerakan_valid(grid, pos_lama, pos_baru):
    r1, c1 = pos_lama
    r2, c2 = pos_baru

    if abs(r1 - r2) + abs(c1 - c2) != 1:
        return False

    if not (0 <= r2 < len(grid)):
        return False

    if not (0 <= c2 < len(grid[r2])):
        return False

    if grid[r2][c2] == OBSTACLE:
        return False

    return True


# jalankan satu algoritma dan kembalikan hasil terstruktur
def jalankan_algoritma(nama, fungsi, grid, start, goal):
    start_time = time.perf_counter()
    path, explored = fungsi(grid, start, goal)
    execution_time = time.perf_counter() - start_time

    return {
        "nama": nama,
        "path": path,
        "langkah": (len(path) - 1) if path else None,
        "explored": explored,
        "waktu": execution_time
    }


# perbandingan BFS vs A*
def tampilkan_perbandingan(hasil_list):
    print("\nPERBANDINGAN PATH PLANNING")

    for hasil in hasil_list:
        print(f"\n{hasil['nama']}")

        if hasil["path"] is None:
            print("Path           : Tidak ditemukan")
            continue

        print(f"Path           : {hasil['langkah']} langkah")
        print(f"Posisi dicek   : {hasil['explored']}")
        print(f"Waktu proses   : {hasil['waktu']:.6f} detik")


# hasil animasi robot
def tampilkan_hasil(start, goal, path, explored, execution_time, nama_algoritma):
    print("\nHASIL SIMULASI")
    print(f"Start          : {start}")
    print(f"Goal           : {goal}")
    print(f"Jumlah langkah : {len(path) - 1}")
    print(f"Posisi dicek   : {explored}")
    print(f"Waktu proses   : {execution_time:.6f} detik")
    print("Collision      : Tidak")
    print("Status         : Goal tercapai")
    print(f"Path Planning  : {nama_algoritma}")


# animasi robot berjalan mengikuti satu path
def animasikan_robot(grid, goal, path):
    planned_path = set(path)
    visited_positions = set()

    for i, current_position in enumerate(path):
        visited_positions.add(current_position)

        print_arena(
            grid,
            current_position,
            planned_path,
            visited_positions
        )

        if current_position == goal:
            print("\nGOAL TERCAPAI!")
            print(f"Robot sampai dalam {i} langkah.")
            break

        next_position = path[i + 1]

        if not gerakan_valid(
            grid,
            current_position,
            next_position
        ):
            print("\nGerakan tidak valid.")
            return False

        arah = tentukan_arah(
            current_position,
            next_position
        )

        print(f"\nLangkah {i + 1}: {arah}")

        time.sleep(ANIMATION_DELAY)

    return True


# jalankan simulasi
def jalankan_simulasi():
    start = cari_posisi(arena, START)
    goal = cari_posisi(arena, GOAL)

    if start is None or goal is None:
        print("Start atau Goal tidak ditemukan.")
        return

    print_arena(arena, start)

    print(f"\nStart : {start}")
    print(f"Goal  : {goal}")

    time.sleep(1)

    sensor = baca_sensor(arena, start)
    tampilkan_sensor(sensor)

    print("\nMencari jalur dengan BFS dan A*...")
    time.sleep(1)

    hasil_bfs = jalankan_algoritma("BFS", bfs_shortest_path, arena, start, goal)
    hasil_astar = jalankan_algoritma("A*", astar_shortest_path, arena, start, goal)

    if hasil_bfs["path"] is None:
        print("\nTidak ada jalur menuju Goal.")
        return

    print(f"\nJalur ditemukan: {hasil_bfs['langkah']} langkah")

    time.sleep(1)

    berhasil = animasikan_robot(arena, goal, hasil_bfs["path"])

    if not berhasil:
        return

    tampilkan_hasil(
        start,
        goal,
        hasil_bfs["path"],
        hasil_bfs["explored"],
        hasil_bfs["waktu"],
        "BFS"
    )

    tampilkan_perbandingan([hasil_bfs, hasil_astar])


# mulai program
if __name__ == "__main__":
    jalankan_simulasi()

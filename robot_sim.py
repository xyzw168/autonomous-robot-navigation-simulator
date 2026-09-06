import os
import time
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

    print("=== AUTONOMOUS ROBOT NAVIGATION SIMULATOR ===")

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
            elif pos in path:
                row.append('*')
            elif pos in visited:
                row.append(PATH)
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


# tampilkan hasil
def tampilkan_hasil(start, goal, path, explored, execution_time):
    print("\n=== HASIL SIMULASI ===")
    print(f"Start          : {start}")
    print(f"Goal           : {goal}")
    print(f"Jumlah langkah : {len(path) - 1}")
    print(f"Posisi dicek   : {explored}")
    print(f"Waktu proses   : {execution_time:.6f} detik")
    print("Collision      : Tidak")
    print("Status         : Goal tercapai")
    print("Path Planning  : BFS")


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

    print("\nMencari jalur...")
    time.sleep(1)

    start_time = time.perf_counter()

    path, explored = bfs_shortest_path(
        arena,
        start,
        goal
    )

    execution_time = time.perf_counter() - start_time

    if path is None:
        print("\nTidak ada jalur menuju Goal.")
        return

    print(f"\nJalur ditemukan: {len(path) - 1} langkah")

    planned_path = set(path)

    time.sleep(1)

    visited_positions = set()

    # robot bergerak mengikuti jalur
    for i, current_position in enumerate(path):
        visited_positions.add(current_position)

        print_arena(
            arena,
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
            arena,
            current_position,
            next_position
        ):
            print("\nGerakan tidak valid.")
            return

        arah = tentukan_arah(
            current_position,
            next_position
        )

        print(f"\nLangkah {i + 1}: {arah}")

        time.sleep(ANIMATION_DELAY)

    tampilkan_hasil(
        start,
        goal,
        path,
        explored,
        execution_time
    )


# mulai program
if __name__ == "__main__":
    jalankan_simulasi()

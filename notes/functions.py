''' custom function definition for (a^b)+1 '''
def raised_to_power_of_num_plus1(place_holder1=0, place_holder2=0):# "=0" is the default value if nothing entered
    combined_placeholder = place_holder1 ** place_holder2 #optional
    return combined_placeholder + 1 # "+1" could have also been in optional variable
print(raised_to_power_of_num_plus1(3, 2)) #(3^2)+1.....3 & 2 override 0 as default value

import random

# --- Ecosystem Parameters ---
GRID_SIZE = 20  # Size of the simulation grid (20x20)
INITIAL_PLANTS = 100
INITIAL_HERBIVORES = 20
INITIAL_CARNIVORES = 5

PLANT_REGROWTH_RATE = 0.1  # Percentage of empty cells that regrow plants each step
HERBIVORE_REPRODUCTION_RATE = 0.05
HERBIVORE_ENERGY_PER_PLANT = 5
HERBIVORE_MOVE_ENERGY_COST = 1
HERBIVORE_MAX_ENERGY = 50
HERBIVORE_INITIAL_ENERGY = 20

CARNIVORE_REPRODUCTION_RATE = 0.03
CARNIVORE_ENERGY_PER_HERBIVORE = 20
CARNIVORE_MOVE_ENERGY_COST = 2
CARNIVORE_MAX_ENERGY = 100
CARNIVORE_INITIAL_ENERGY = 50

SIMULATION_STEPS = 200

# --- Helper Functions ---
def get_random_empty_cell(grid, occupied_cells):
    """Finds a random empty cell on the grid."""
    while True:
        x, y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
        if (x, y) not in occupied_cells:
            return x, y
    return None # Should not happen if there are empty cells

class Plant:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = "plant"

    def __repr__(self):
        return "P"

class Herbivore:
    def __init__(self, x, y, energy):
        self.x = x
        self.y = y
        self.energy = energy
        self.type = "herbivore"

    def __repr__(self):
        return "H"

    def move(self, grid, occupied_cells):
        if self.energy <= HERBIVORE_MOVE_ENERGY_COST:
            return False # Not enough energy to move

        potential_moves = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = (self.x + dx) % GRID_SIZE, (self.y + dy) % GRID_SIZE
                if (nx, ny) not in occupied_cells or grid[nx][ny] is None or isinstance(grid[nx][ny], Plant):
                    potential_moves.append((nx, ny))

        if potential_moves:
            old_pos = (self.x, self.y)
            self.x, self.y = random.choice(potential_moves)
            self.energy -= HERBIVORE_MOVE_ENERGY_COST
            return old_pos, (self.x, self.y)
        return False

    def eat(self, plant):
        self.energy = min(self.energy + HERBIVORE_ENERGY_PER_PLANT, HERBIVORE_MAX_ENERGY)

    def reproduce(self):
        return random.random() < HERBIVORE_REPRODUCTION_RATE and self.energy > HERBIVORE_MAX_ENERGY * 0.6

class Carnivore:
    def __init__(self, x, y, energy):
        self.x = x
        self.y = y
        self.energy = energy
        self.type = "carnivore"

    def __repr__(self):
        return "C"

    def move(self, grid, occupied_cells):
        if self.energy <= CARNIVORE_MOVE_ENERGY_COST:
            return False

        potential_moves = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = (self.x + dx) % GRID_SIZE, (self.y + dy) % GRID_SIZE
                # Can move to empty or herbivore cell
                if (nx, ny) not in occupied_cells or grid[nx][ny] is None or isinstance(grid[nx][ny], Herbivore):
                    potential_moves.append((nx, ny))

        if potential_moves:
            old_pos = (self.x, self.y)
            self.x, self.y = random.choice(potential_moves)
            self.energy -= CARNIVORE_MOVE_ENERGY_COST
            return old_pos, (self.x, self.y)
        return False

    def eat(self, herbivore):
        self.energy = min(self.energy + CARNIVORE_ENERGY_PER_HERBIVORE, CARNIVORE_MAX_ENERGY)

    def reproduce(self):
        return random.random() < CARNIVORE_REPRODUCTION_RATE and self.energy > CARNIVORE_MAX_ENERGY * 0.6

# --- Simulation Setup ---
def initialize_ecosystem():
    """Initializes the grid and populates it with entities."""
    grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    plants = []
    herbivores = []
    carnivores = []
    occupied_cells = set()

    # Place plants
    for _ in range(INITIAL_PLANTS):
        if len(occupied_cells) >= GRID_SIZE * GRID_SIZE: break
        x, y = get_random_empty_cell(grid, occupied_cells)
        plant = Plant(x, y)
        grid[x][y] = plant
        plants.append(plant)
        occupied_cells.add((x,y))

    # Place herbivores
    for _ in range(INITIAL_HERBIVORES):
        if len(occupied_cells) >= GRID_SIZE * GRID_SIZE: break
        x, y = get_random_empty_cell(grid, occupied_cells)
        herbivore = Herbivore(x, y, HERBIVORE_INITIAL_ENERGY)
        grid[x][y] = herbivore
        herbivores.append(herbivore)
        occupied_cells.add((x,y))

    # Place carnivores
    for _ in range(INITIAL_CARNIVORES):
        if len(occupied_cells) >= GRID_SIZE * GRID_SIZE: break
        x, y = get_random_empty_cell(grid, occupied_cells)
        carnivore = Carnivore(x, y, CARNIVORE_INITIAL_ENERGY)
        grid[x][y] = carnivore
        carnivores.append(carnivore)
        occupied_cells.add((x,y))

    return grid, plants, herbivores, carnivores, occupied_cells

def display_grid(grid):
    """Prints the current state of the grid."""
    print("-" * (GRID_SIZE * 2 + 1))
    for row in grid:
        display_row = []
        for cell in row:
            if cell is None:
                display_row.append(" ")
            else:
                display_row.append(str(cell))
        print("|" + "|".join(display_row) + "|")
    print("-" * (GRID_SIZE * 2 + 1))

# --- Simulation Loop ---
def run_simulation():
    grid, plants, herbivores, carnivores, occupied_cells = initialize_ecosystem()

    print(f"Initial state: Plants: {len(plants)}, Herbivores: {len(herbivores)}, Carnivores: {len(carnivores)}")
    display_grid(grid)

    for step in range(SIMULATION_STEPS):
        # --- Herbivore Actions ---
        new_herbivores = []
        herbivores_to_remove = []
        for herbivore in list(herbivores): # Iterate over a copy for safe removal
            if herbivore.energy <= 0:
                herbivores_to_remove.append(herbivore)
                continue

            # Try to eat
            ate = False
            if isinstance(grid[herbivore.x][herbivore.y], Plant):
                plant_to_eat = grid[herbivore.x][herbivore.y]
                herbivore.eat(plant_to_eat)
                plants.remove(plant_to_eat)
                grid[herbivore.x][herbivore.y] = herbivore # Herbivore stays in the cell
                ate = True
            elif grid[herbivore.x][herbivore.y] is None: # If cell became empty (e.g. another herbivore ate)
                grid[herbivore.x][herbivore.y] = herbivore # Re-occupy

            # Try to move if didn't eat or to find food
            if not ate or random.random() < 0.5: # Move even if ate, with some probability
                moved = herbivore.move(grid, occupied_cells - {(herbivore.x, herbivore.y)}) # Temporarily allow moving from current spot
                if moved:
                    old_pos, new_pos = moved
                    if grid[old_pos[0]][old_pos[1]] == herbivore: # Ensure it's this herbivore moving
                         grid[old_pos[0]][old_pos[1]] = None
                         occupied_cells.discard(old_pos)
                    grid[new_pos[0]][new_pos[1]] = herbivore
                    occupied_cells.add(new_pos)

                    # Check if moved onto a plant
                    if isinstance(grid[new_pos[0]][new_pos[1]], Plant): # This logic is a bit tricky if plant is at new_pos
                        # This means the move function allowed moving onto a plant, let's correct grid setup
                        # The move function should ideally check grid[nx][ny] type
                        # For simplicity, let's assume herbivore eats if it lands on a plant
                        target_at_new_pos = None
                        for p in plants: # find the plant object at new_pos
                            if p.x == new_pos[0] and p.y == new_pos[1] and p != herbivore: # make sure it's not the herbivore itself
                                target_at_new_pos = p
                                break
                        if target_at_new_pos and isinstance(target_at_new_pos, Plant):
                            herbivore.eat(target_at_new_pos)
                            plants.remove(target_at_new_pos)
                            # Herbivore is already at new_pos

            herbivore.energy -= HERBIVORE_MOVE_ENERGY_COST # Base energy decay
            if herbivore.energy <= 0:
                herbivores_to_remove.append(herbivore)
                continue

            if herbivore.reproduce():
                if len(occupied_cells) < GRID_SIZE * GRID_SIZE:
                    try:
                        nx, ny = get_random_empty_cell(grid, occupied_cells)
                        new_h = Herbivore(nx, ny, HERBIVORE_INITIAL_ENERGY)
                        new_herbivores.append(new_h)
                        grid[nx][ny] = new_h
                        occupied_cells.add((nx,ny))
                        herbivore.energy -= HERBIVORE_MAX_ENERGY * 0.3 # Cost of reproduction
                    except TypeError: # No empty cells
                        pass


        for h_rem in set(herbivores_to_remove): # Use set to avoid issues if added multiple times
            if h_rem in herbivores:
                herbivores.remove(h_rem)
                if grid[h_rem.x][h_rem.y] == h_rem:
                    grid[h_rem.x][h_rem.y] = None
                    occupied_cells.discard((h_rem.x, h_rem.y))
        herbivores.extend(new_herbivores)


        # --- Carnivore Actions ---
        new_carnivores = []
        carnivores_to_remove = []
        for carnivore in list(carnivores):
            if carnivore.energy <= 0:
                carnivores_to_remove.append(carnivore)
                continue

            # Try to eat
            ate_herbivore = False
            # Check adjacent cells for herbivores
            potential_prey_pos = []
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0: continue
                    nx, ny = (carnivore.x + dx) % GRID_SIZE, (carnivore.y + dy) % GRID_SIZE
                    if isinstance(grid[nx][ny], Herbivore):
                        potential_prey_pos.append((nx,ny))

            if potential_prey_pos:
                prey_x, prey_y = random.choice(potential_prey_pos)
                prey_herbivore = grid[prey_x][prey_y]

                if prey_herbivore in herbivores: # Ensure prey is still valid
                    carnivore.eat(prey_herbivore)
                    herbivores.remove(prey_herbivore) # Herbivore is eaten
                    # Carnivore moves to prey's cell
                    if grid[carnivore.x][carnivore.y] == carnivore:
                        grid[carnivore.x][carnivore.y] = None
                        occupied_cells.discard((carnivore.x, carnivore.y))
                    carnivore.x, carnivore.y = prey_x, prey_y
                    grid[prey_x][prey_y] = carnivore
                    occupied_cells.add((prey_x, prey_y))
                    ate_herbivore = True

            # Try to move if didn't eat or to find food
            if not ate_herbivore or random.random() < 0.5:
                moved = carnivore.move(grid, occupied_cells - {(carnivore.x, carnivore.y)})
                if moved:
                    old_pos, new_pos = moved
                    if grid[old_pos[0]][old_pos[1]] == carnivore:
                        grid[old_pos[0]][old_pos[1]] = None
                        occupied_cells.discard(old_pos)
                    grid[new_pos[0]][new_pos[1]] = carnivore
                    occupied_cells.add(new_pos)

                    # If carnivore moved onto a herbivore (less likely with current move logic but good check)
                    target_at_new_pos = None
                    for h in herbivores:
                        if h.x == new_pos[0] and h.y == new_pos[1] and h != carnivore:
                            target_at_new_pos = h
                            break
                    if target_at_new_pos and isinstance(target_at_new_pos, Herbivore):
                        carnivore.eat(target_at_new_pos)
                        herbivores.remove(target_at_new_pos)
                        # Carnivore is already at new_pos

            carnivore.energy -= CARNIVORE_MOVE_ENERGY_COST # Base energy decay
            if carnivore.energy <= 0:
                carnivores_to_remove.append(carnivore)
                continue

            if carnivore.reproduce():
                if len(occupied_cells) < GRID_SIZE * GRID_SIZE:
                    try:
                        nx, ny = get_random_empty_cell(grid, occupied_cells)
                        new_c = Carnivore(nx, ny, CARNIVORE_INITIAL_ENERGY)
                        new_carnivores.append(new_c)
                        grid[nx][ny] = new_c
                        occupied_cells.add((nx,ny))
                        carnivore.energy -= CARNIVORE_MAX_ENERGY * 0.3
                    except TypeError: # No empty cells
                        pass

        for c_rem in set(carnivores_to_remove):
            if c_rem in carnivores:
                carnivores.remove(c_rem)
                if grid[c_rem.x][c_rem.y] == c_rem:
                    grid[c_rem.x][c_rem.y] = None
                    occupied_cells.discard((c_rem.x, c_rem.y))
        carnivores.extend(new_carnivores)


        # --- Plant Regrowth ---
        num_empty_cells = GRID_SIZE * GRID_SIZE - len(occupied_cells)
        num_new_plants = int(num_empty_cells * PLANT_REGROWTH_RATE)

        for _ in range(num_new_plants):
            if len(occupied_cells) >= GRID_SIZE * GRID_SIZE: break
            try:
                x, y = get_random_empty_cell(grid, occupied_cells)
                plant = Plant(x, y)
                grid[x][y] = plant
                plants.append(plant)
                occupied_cells.add((x,y))
            except TypeError: # No empty cells
                break


        # --- Update occupied_cells (important for consistency) ---
        occupied_cells.clear()
        for r_idx, row in enumerate(grid):
            for c_idx, cell_content in enumerate(row):
                if cell_content is not None:
                    occupied_cells.add((r_idx, c_idx))
                    # Ensure entity positions match grid positions
                    if hasattr(cell_content, 'x') and hasattr(cell_content, 'y'):
                        cell_content.x = r_idx
                        cell_content.y = c_idx


        # --- Output Statistics ---
        if (step + 1) % 10 == 0 or step == 0: # Display every 10 steps or the first step
            print(f"\n--- Step {step + 1} ---")
            print(f"Plants: {len(plants)}, Herbivores: {len(herbivores)}, Carnivores: {len(carnivores)}")
            # display_grid(grid) # Can be too verbose for many steps
            if not herbivores and not carnivores:
                print("Ecosystem collapsed: All animals died.")
                break
            if not plants and not herbivores:
                print("Ecosystem collapsed: No plants or herbivores remaining.")
                break
            if not plants and herbivores:
                print("Warning: No plants remaining, herbivores may starve soon.")


    print("\n--- Simulation Ended ---")
    print(f"Final state after {SIMULATION_STEPS} steps:")
    print(f"Plants: {len(plants)}, Herbivores: {len(herbivores)}, Carnivores: {len(carnivores)}")
    display_grid(grid)

if __name__ == "__main__":
    run_simulation()
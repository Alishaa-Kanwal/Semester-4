def Water_jug_Solver(jug1, jug2, goal):
    stack = [(0,0)]
    visited = set()
    route = []

    while stack:
        state = stack.pop()
        x,y = state
        
        if state in visited:
            continue

        visited.add(state)
        route.append(state)
        print(f"Steps: {len(route)} - Jugs: {state}")

        if x == goal or y == goal:
            print("Solution Found.")
            for step in route:
                print(step)
            return
        
        possible_steps = [
            (jug1,y),
            (x,jug2),
            (0,y),
            (x,0),
            (x-min(x,jug2 - y), y+min(x, jug2 - y)),
            (x+min(y,jug1 - x), y-min(y,jug1 - x))
        ]

        for move in possible_steps:
            if move not in visited:
                stack.append(move)

    print("No Solution Found!")

jug1= int(input("Enter jug 1 water:"))
jug2= int(input("Enter jug 2 water:"))
goal= int(input("Enter Target:"))

Water_jug_Solver(jug1, jug2, goal)
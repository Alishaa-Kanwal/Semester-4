def grid_dimen():

    while True:
        grid =  input("Enter grid ration like 4X4:").strip().lower()
        if 'x' not in grid:
            print("Invalid Input. Enter (Row(space)Column).")
            continue

        part = grid.split('x')
        if len(part)!= 2:
            print("Invalid Format. Please use 'rowXcol'. ")
            continue
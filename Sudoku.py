import pygame
from time import time

pygame.init()
pygame.display.set_caption("Test")
screen = pygame.display.set_mode((750, 700))
pygame.key.set_repeat(300, 1)

### Screen Setting

Bg_Color = (150, 150, 150)
Gray = (80, 80, 80)
Bright_Bg = (230, 230, 230)
Blue = (50, 50, 250)
Green = (50, 250, 50)

Line_1 = 50
Line_2 = 650
Black = (0, 0, 0)
Line_Width = 8
Lines = []

Space = (Line_2 - Line_1) // (9 + 1)
for x in range(Line_1, Line_2, Space):
    Lines.append(((x, Line_1), (x, Line_2 - Space)))

for y in range(Line_1, Line_2, Space):
    Lines.append(((Line_1, y), (Line_2 - Space, y)))

### Game Setting

# Board
Board = [[0 for x in range(9)] for y in range(9)]


# Text
def ShowText(text, pos, size, color=Black):
    screen.blit(pygame.font.SysFont('Comic Sans MS', size).render(text, True, color), pos)


number = 1
Number_x = Line_1
Number_y = Line_2 - Space // 2
Text_Size = 30
Set_Size = 15


### Mouse Detect
def Mouse_Detect():
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if mouse_x <= Line_1 or mouse_x >= Line_2 - Space \
            or mouse_y <= Line_1 or mouse_y >= Line_2 - Space:
        return False
    pos = [-1, -1]
    for x in range(Line_1, Line_2, Space):
        if mouse_x < x:
            break
        else:
            pos[0] += 1

    for y in range(Line_1, Line_2 - Space, Space):
        if mouse_y < y:
            break
        else:
            pos[1] += 1

    return pos


def Draw_Rec(pos, color, size=1):
    pygame.draw.rect(
        screen,
        color,
        (Line_1 + Space * pos[0],
         Line_1 + Space * pos[1],
         Space * size, Space * size)
    )


# Set
Sets = [[set(range(1, 10)) for x in range(9)] for y in range(9)]
new = set()


def isFinish():
    for L in Board:
        if not all(L):
            return False
    return True


def isLegal():
    # row
    Update1()
    for L in Board:
        count = [0] * 9
        for nbr in L:
            if nbr:
                count[nbr - 1] += 1
        for c in count:
            if c > 1:
                return False
    # column
    for x in range(9):
        count = [0] * 9
        for y in range(9):
            if Board[y][x]:
                count[Board[y][x] - 1] += 1
            for c in count:
                if c > 1:
                    return False
    # block
    for Y in range(3):
        for X in range(3):
            count = [0] * 9
            for y in range(3):
                for x in range(3):
                    if Board[Y * 3 + y][X * 3 + x]:
                        count[Board[Y * 3 + y][X * 3 + x] - 1] += 1
            for c in count:
                if c > 1:
                    return False

    # set
    for y in range(9):
        for x in range(9):
            if not Board[y][x] and not Sets[y][x]:
                return False
    return True


def Update1():
    global Board, Sets, new
    for y in range(9):
        for x in range(9):
            if Board[y][x]:  # not 0
                Sets[y][x].clear()
                continue
            Set = set(range(1, 10))

            # row
            Set -= set(Board[y])

            # column
            Set -= set(list(zip(*Board))[x])

            # Block
            X = x // 3
            Y = y // 3
            for i in range(3):
                for j in range(3):
                    Set.discard(Board[Y * 3 + i][X * 3 + j])
            if len(Set) == 1:
                Board[y][x] = Set.pop()
                new.add((x, y))
                return Update1()

            Sets[y][x] = Set.copy()


def Update2():
    global Board, Sets, new
    Update1()
    if not isLegal():
        return False
    # row (only 1)
    for y in range(9):
        count = [0] * 9
        for x in range(9):
            for e in Sets[y][x]:
                if e:
                    count[e - 1] += 1
        for i in range(9):
            if count[i] == 1:  # only 1
                # find
                for x in range(9):
                    if i + 1 in Sets[y][x]:
                        Board[y][x] = i + 1
                        new.add((x, y))
                        return Update2()
    # column (only 1)
    for x in range(9):
        count = [0] * 9
        for y in range(9):
            for e in Sets[y][x]:
                if e:
                    count[e - 1] += 1
        for i in range(9):
            if count[i] == 1:  # only 1
                # find
                for y in range(9):
                    if i + 1 in Sets[y][x]:
                        Board[y][x] = i + 1
                        new.add((x, y))
                        return Update2()

    # block (only 1)
    for Y in range(3):
        for X in range(3):
            count = [0] * 9
            for y in range(Y * 3, Y * 3 + 3):
                for x in range(X * 3, X * 3 + 3):
                    for e in Sets[y][x]:
                        if e:
                            count[e - 1] += 1
            for i in range(9):
                if count[i] == 1:  # only 1
                    # find
                    for y in range(Y * 3, Y * 3 + 3):
                        for x in range(X * 3, X * 3 + 3):
                            if i + 1 in Sets[y][x]:
                                Board[y][x] = i + 1
                                new.add((x, y))
                                return Update2()
    return isLegal()


def Update3():
    global Board, Sets, new
    if not Update2():
        return False
    # Find len(set) == 2
    for y in range(9):
        for x in range(9):
            if len(Sets[y][x]) == 2:
                # Back up
                Board_c = [L.copy() for L in Board]
                new_c = new.copy()

                choice0, choice1 = Sets[y][x]
                # Try 0
                Board[y][x] = choice0
                new.add((x, y))

                if not isLegal():  # is 1
                    # Back
                    Board = [L.copy() for L in Board_c]
                    new = new_c.copy()

                    # go 1
                    Board[y][x] = choice1
                    new.add((x, y))
                    return Update3()

                if isFinish():
                    return True

                # Stop (Try 1)
                # Back
                Board = [L.copy() for L in Board_c]
                new = new_c.copy()

                # try 1
                Board[y][x] = choice1
                new.add((x, y))
                Update2()
                if not isLegal():  # is 0
                    # Back
                    Board = [L.copy() for L in Board_c]
                    new = new_c.copy()

                    # go 0
                    Board[y][x] = choice0
                    new.add((x, y))
                    return Update3()

                if isFinish():
                    return True

                # both are uncertain
                # Back
                Board = [L.copy() for L in Board_c]
                new = new_c.copy()
    return isLegal()


def Brute_Force(depth):
    global Board, Sets, new
    Update1()
    for y in range(9):
        for x in range(9):
            for e in Sets[y][x].copy():
                # Back up
                Board_c = [L.copy() for L in Board]
                new_c = new.copy()

                if depth != 0:
                    # Try
                    Board[y][x] = e
                    new.add((x, y))

                    if Brute_Force(depth - 1):
                        return True
                    # Back
                    Board = [L.copy() for L in Board_c]
                    new = new_c.copy()

                else:
                    # Try
                    Board[y][x] = e
                    new.add((x, y))
                    if not Update3() or not isFinish():
                        # Back
                        Board = [L.copy() for L in Board_c]
                        new = new_c.copy()
                    else:
                        return True
    return isFinish()


while True:
    pygame.time.delay(50)

    select = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            select = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
            elif event.key == pygame.K_a:
                number -= 1
            elif event.key == pygame.K_d:
                number += 1

            elif event.key == pygame.K_r:
                for pos in new:
                    Board[pos[1]][pos[0]] = 0
                new.clear()

            elif event.key == pygame.K_u:
                for pos in new:
                    Board[pos[1]][pos[0]] = 0
                new.clear()
                Update1()

            elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                new.clear()
                Update3()
                if not isFinish():
                    Depth = 0
                    time1 = time()
                    print("Brute Force : 0")
                    while not Brute_Force(Depth):
                        Depth += 1
                        print("time :", time() - time1)
                        print("Brute Force :", Depth)
                        time1 = time()
                    print("time :", time() - time1)

    # -------------------------------------- Screen

    # Board
    screen.fill(Bg_Color)

    # gray rec
    Draw_Rec((3, 0), Gray, 3)
    Draw_Rec((0, 3), Gray, 3)
    Draw_Rec((3, 6), Gray, 3)
    Draw_Rec((6, 3), Gray, 3)

    # lines
    for tp in Lines:
        pygame.draw.line(screen, Black, tp[0], tp[1], Line_Width)

    # Number List
    if number == -1:
        number = 9
    elif number == 10:
        number = 0

    # mouse detect
    detect = Mouse_Detect()
    if detect:
        Draw_Rec(detect, Bright_Bg)
        if select:
            Board[detect[1]][detect[0]] = number

        # Show Set
        if not Board[detect[1]][detect[0]]:
            for e in Sets[detect[1]][detect[0]]:
                ShowText(str(e), (Line_2 + ((e - 1) % 3 - 1) * Space // 2, Line_2 + ((e - 1) // 3 - 5) * Space // 2),
                         Text_Size, Blue)

    # Show Text
    # Number List
    for i in range(10):
        if i == number:
            ShowText(str(i), (Number_x + Space * i, Number_y), Text_Size, Green)
        else:
            ShowText(str(i), (Number_x + Space * i, Number_y), Text_Size)

    # Board Number
    for y in range(9):
        for x in range(9):
            v = Board[y][x]
            if v:
                if (x, y) in new:
                    ShowText(str(v), ((x + 1.2) * Space, (y + 1) * Space), Text_Size, Green)
                else:
                    ShowText(str(v), ((x + 1.2) * Space, (y + 1) * Space), Text_Size)

    pygame.display.update()

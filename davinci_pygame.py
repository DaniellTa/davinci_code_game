import pygame_widgets
import pygame
from pygame_widgets.button import Button
from pygame_widgets.dropdown import Dropdown
import random
import collections

# Constants
TILE_SIZE = 100
SCREEN_WIDTH = TILE_SIZE * 10
SCREEN_HEIGHT = TILE_SIZE * 6
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (211, 211, 211)
LIGHT_GREY = (245, 245, 245)

# Initialize pygame
pygame.init()
BLINK_EVENT = pygame.USEREVENT + 0

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Da Vinci Code")

# Font setup
font = pygame.font.Font(None, 74)

# Game setup

# Define tiles
order_of_tiles = [[j, str(i), False] for i in range(12) for j in range(2)]
order_of_tiles.insert(random.randint(0, len(order_of_tiles)), [0, "-", False])
order_of_tiles.insert(random.randint(0, len(order_of_tiles)), [1, "-", False])
all_tiles = []
all_tiles.extend(order_of_tiles)



# Define helper functions
def create_tiles():
    temp_all_black_tiles = [i for i in all_tiles if i[0] == 0]
    black_tiles = random.sample(temp_all_black_tiles, 2)
    for i in black_tiles:
        all_tiles.remove(i)
    temp_all_white_tiles = [i for i in all_tiles if i[0] == 1]
    white_tiles = random.sample(temp_all_white_tiles, 2)
    for i in white_tiles:
        all_tiles.remove(i)

    # Combine the selected tiles
    selected_tiles = black_tiles + white_tiles

    # Sort the tiles based on order_of_tiles
    final = [i for i in order_of_tiles if i in selected_tiles]

    return final


def get_selected_box(mouse_pos):
    # # top tiles
    # for idx, [color, number, revealed] in enumerate(tiles1):
    #     top_tile = pygame.Rect(idx*TILE_SIZE, 0, TILE_SIZE, TILE_SIZE)
    #     if top_tile.collidepoint(mouse_pos):
    #         return [color, number, revealed]
    #
    # # bottom tiles and raised bottom tiles
    # for idx, [color, number, revealed] in enumerate(tiles2):
    #     if not revealed:
    #         bottom_tile = pygame.Rect(idx * TILE_SIZE, 390 + TILE_SIZE, TILE_SIZE, TILE_SIZE)
    #         if bottom_tile.collidepoint(mouse_pos):
    #             return [color, number, revealed]
    #     else:
    #         bottom_tile = pygame.Rect(idx * TILE_SIZE, 330 + TILE_SIZE, TILE_SIZE, TILE_SIZE)
    #         if bottom_tile.collidepoint(mouse_pos):
    #             return [color, number, revealed]

    # confirm button
    confirm_button = pygame.Rect(SCREEN_WIDTH - TILE_SIZE*2 - 20, 204, 100, 50)
    if confirm_button.collidepoint(mouse_pos):
        return "confirm clicked"

    black_tile_pickup = pygame.Rect(SCREEN_WIDTH - TILE_SIZE * 2 - 20, 300, TILE_SIZE, TILE_SIZE)
    if black_tile_pickup.collidepoint(mouse_pos):
        return "black tile picked"

    white_tile_pickup = pygame.Rect(SCREEN_WIDTH - TILE_SIZE - 10, 300, TILE_SIZE, TILE_SIZE)
    if white_tile_pickup.collidepoint(mouse_pos):
        return "white tile picked"


def create_dropdowns(tiles):
    global dict_dropdowns
    global dropdown_states
    dict_dropdowns = {}
    for idx, [color, number, revealed] in enumerate(tiles):
        dict_dropdowns[(color, number, revealed)] = Dropdown(
            screen, TILE_SIZE*idx, 80, TILE_SIZE, 20, name='guess',
            choices=[str(i) for i in range(12)] + ["-"],
            borderRadius=3, colour=pygame.Color(LIGHT_GREY), direction='down', textHAlign='centre')

    dropdown_states = {}
    for key, value in dict_dropdowns.items():
        dropdown_states[key] = None


def check_tile():
    if last_selected_dropdown is not None and last_selected_dropdown in dict_dropdowns.values():
        guess = last_selected_dropdown.getSelected() #e.g. "-"
        key = list(dict_dropdowns.keys())[list(dict_dropdowns.values()).index(last_selected_dropdown)] #[color, number, raised, revealed]
        if str(guess) == key[1]:
            return key
    return False


def tile_to_coordinates(key):
    return dict_tile_coords[key]

def pickup_tile(tiles: list, color_choice: int) -> None:
    tiles_of_color_choice = [i for i in all_tiles if i[0] == color_choice]
    tile_choice = tiles_of_color_choice.pop(random.randrange(len(tiles_of_color_choice)))
    all_tiles.remove(tile_choice)
    tiles.append(tile_choice)
    final = [i for i in order_of_tiles if i in tiles]
    #tiles = final
    for i in range(len(tiles)):
        tiles.pop()
    for i in final:
        tiles.append(i)
    tiles[tiles.index(tile_choice)][2] = True

def draw_black_and_white_tiles():
    pygame.draw.rect(screen, BLACK, (SCREEN_WIDTH - TILE_SIZE*2 - 20, 300, TILE_SIZE, TILE_SIZE), border_radius=10)
    pygame.draw.rect(screen, WHITE, (SCREEN_WIDTH - TILE_SIZE - 10, 300, TILE_SIZE, TILE_SIZE), border_radius=10)
    text = pygame.font.Font(None, 25).render("Pick a tile color first", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH - TILE_SIZE - TILE_SIZE-20, 270))


# Define dicts and variables
dict_dropdowns = {}
dict_tile_coords = {}
dropdown_states = {}
last_selected_dropdown = None

tiles1 = create_tiles()
# print(f"top tiles: {[i[1] for i in tiles1]}")
tiles2 = create_tiles()

#create_dropdowns(tiles1)

# for key, value in dict_dropdowns.items():
#     dropdown_states[key] = None

confirm_choice_button = Button(
    screen, SCREEN_WIDTH - TILE_SIZE*2 - 20, 204, 100, 50, text='Confirm Guess', fontSize=30,
    margin=20, inactiveColour=(152, 251, 152), pressedColour=pygame.Color("green"),
    radius=5, onClick=check_tile, font=pygame.font.SysFont('calibri', 10),
    textVAlign='bottom'
)








# --------------------------------------------------------------------------------------------- #
# Main game loop #

# initialize tile dictionaries and coordinates for top player
for idx, [color, number, revealed] in enumerate(tiles1):
    dict_tile_coords[(color, number, revealed)] = (idx*TILE_SIZE, 0, TILE_SIZE, TILE_SIZE)
    #print(color, number, revealed)


# initialize same for bottom player
for idx, [color, number, revealed] in enumerate(tiles2):
    if not revealed:
        dict_tile_coords[(color, number, revealed)] = (idx * TILE_SIZE, 390 + TILE_SIZE, TILE_SIZE, TILE_SIZE)
    else:
        dict_tile_coords[(color, number, revealed)] = (idx * TILE_SIZE, 330 + TILE_SIZE, TILE_SIZE, TILE_SIZE)


def main_menu(tiles1, tiles2):
    global dropdown_states, dict_dropdowns, dict_tile_coords, last_selected_dropdown
    running = True
    wrong_guess = False
    picked_up = False


    # change color of dropdown
    for idx, [color, number, revealed] in enumerate(tiles1):
        color_value = BLACK if color == 0 else WHITE
        dict_dropdowns[(color, number, revealed)] = Dropdown(
            screen, TILE_SIZE * idx, 80, TILE_SIZE, 20, name='',
            choices=[str(i) for i in range(12)] + ["-"],
            borderRadius=3, colour=color_value, direction='down', textHAlign='centre')

    while running:
        #screen.fill((173, 216, 230))
        screen.fill((144,213,255))
        selected = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if wrong_guess:
                        running = False
                        break
                elif event.key == pygame.K_ESCAPE:
                    running = False
                    break
            #detect mouse click
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                selected = get_selected_box(mouse_pos) # [color, number, revealed]

        # check winner
        count = len([i for i in tiles1 if i[2]])
        if count == len(tiles1):
            winner_text = pygame.font.Font(None, 60).render("WINNER WINNER CHICKEN DINNER", True, (70, 255, 200))
            screen.blit(winner_text, (15, (SCREEN_HEIGHT // 2) - 15))

        # make user pick up tile first
        if not picked_up:
            dict_dropdowns = {}
            dropdown_states = {}
            if selected == "black tile picked":
                picked_up = True
                pickup_tile(tiles2, 0)
                create_dropdowns(tiles1)
            elif selected == "white tile picked":
                picked_up = True
                pickup_tile(tiles2, 1)
                create_dropdowns(tiles1)


        #dropdown selection
        if picked_up:
            for key, none_bool in dropdown_states.items():
                try:
                    dropdown = dict_dropdowns[key]
                except KeyError:
                    breakpoint()
                current_selection = dropdown.getSelected()
                if current_selection is not None and current_selection is not none_bool:
                    last_selected_dropdown = dropdown
                    dropdown_states[key] = current_selection
                elif current_selection is None:
                    dropdown_states[key] = None

            # if guess is wrong
            if wrong_guess:
                text = pygame.font.Font(None, 45).render("Incorrect guess. Press space to end your turn.", True, (255, 0, 0))
                screen.blit(text, (10, (SCREEN_HEIGHT // 2) - 10))


        # Draw tiles for top player
        for idx, [color, number, revealed] in enumerate(tiles1):
            dict_tile_coords[(color, number, revealed)] = (idx*TILE_SIZE, 0, TILE_SIZE, TILE_SIZE)
            color_value = BLACK if color == 0 else WHITE
            pygame.draw.rect(screen, color_value, dict_tile_coords[(color, number, revealed)], border_radius=10)


            if selected == "confirm clicked" and check_tile() == (color, number, revealed) and picked_up:

                selected = None

                #reveal tile in tiles1
                tiles1[idx][2] = True

                # update dict_tile_coords
                buffer_dict = {}
                for key, value in dict_tile_coords.items():
                    if key == (color, number, revealed):
                        buffer_dict[(color, number, not revealed)] = value
                    else:
                        buffer_dict[key] = value
                del dict_tile_coords
                dict_tile_coords = buffer_dict

                # update dict_dropdown
                buffer_dict = {}
                for key, value in dict_dropdowns.items():
                    if key == (color, number, revealed):
                        buffer_dict[(color, number, not revealed)] = value
                    else:
                        buffer_dict[key] = value
                del dict_dropdowns
                dict_dropdowns = buffer_dict

                #update dropdown_states
                buffer_dict = {}
                for key, value in dropdown_states.items():
                    if key == (color, number, revealed):
                        buffer_dict[(color, number, not revealed)] = value
                    else:
                        buffer_dict[key] = value
                del dropdown_states
                dropdown_states = buffer_dict

                # change color of dropdown
                dict_dropdowns[(color, number, revealed)] = Dropdown(
                    screen, TILE_SIZE * idx, 80, TILE_SIZE, 20, name='',
                    choices=[str(i) for i in range(12)] + ["-"],
                    borderRadius=3, colour=color_value, direction='down', textHAlign='centre')

            elif selected == "confirm clicked" and not check_tile() and picked_up:
                wrong_guess = True
                selected = None

            if revealed:
                # reveal tile number
                text = font.render(number, True, WHITE if color == 0 else BLACK)
                screen.blit(text, (idx * TILE_SIZE + 30, 10))

                # change color of dropdown
                dict_dropdowns[(color, number, revealed)] = Dropdown(
                    screen, TILE_SIZE * idx, 80, TILE_SIZE, 20, name='',
                    choices=[str(i) for i in range(12)] + ["-"],
                    borderRadius=3, colour=color_value, direction='down', textHAlign='centre')

        draw_black_and_white_tiles()


        # Draw tiles for bottom player
        for idx, [color, number, revealed] in enumerate(tiles2):
            if not revealed:
                dict_tile_coords[(color, number, revealed)] = (idx * TILE_SIZE, 390 + TILE_SIZE, TILE_SIZE, TILE_SIZE)
                color_value = BLACK if color == 0 else WHITE
                pygame.draw.rect(screen, color_value, dict_tile_coords[(color, number, revealed)],
                                 border_radius=10)
                text = font.render(number, True, WHITE if color == 0 else BLACK)
                screen.blit(text, (idx * TILE_SIZE + 30, 400 + TILE_SIZE))
            else:
                dict_tile_coords[(color, number, revealed)] = (idx * TILE_SIZE, 330 + TILE_SIZE, TILE_SIZE, TILE_SIZE)
                color_value = BLACK if color == 0 else WHITE
                pygame.draw.rect(screen, color_value, dict_tile_coords[(color, number, revealed)],
                                 border_radius=10)
                text = font.render(number, True, WHITE if color == 0 else BLACK)
                screen.blit(text, (idx * TILE_SIZE + 30, 340 + TILE_SIZE))

        # removes tiles from coords dict after raising
        buffer_list = [key[:2] for key in dict_tile_coords.keys()]
        duplicate_keys = [item for item, count in collections.Counter(buffer_list).items() if count > 1]
        for i in duplicate_keys:
            try:
                dict_tile_coords.pop((i[0], i[1], False, False))
            except KeyError:
                pass


        pygame_widgets.update(pygame.event.get())
        pygame.display.update()

        # Update the display
        pygame.display.flip()

        # Delay to manage frame rate
        pygame.time.Clock().tick(30)

def switch_turns():
    running = True
    clock = pygame.time.Clock()

    # Timer variables for blinking
    blink_timer = 0
    show_text = True
    blink_interval = 500  # Blink interval in milliseconds

    while running:
        # Fill the screen with background color
        screen.fill((144,213,255))

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE:
                    running = False

        # Blink logic
        blink_timer += clock.get_time()
        if blink_timer >= blink_interval:
            show_text = not show_text
            blink_timer = 0

        # Display text if `show_text` is True
        if show_text:
            text = pygame.font.Font(None, 50).render("Press space to start your turn", True, BLACK)
            screen.blit(text, (255, (SCREEN_HEIGHT // 2) - 20))

        # Update the display
        pygame.display.flip()

        # Delay to manage frame rate
        clock.tick(60)

def start_menu():
    running = True
    clock = pygame.time.Clock()

    # Timer variables for blinking
    blink_timer = 0
    show_text = True
    blink_interval = 500  # Blink interval in milliseconds

    while running:
        # Fill the screen with background color
        screen.fill((144,213,255))

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                running = False

        # Blink logic
        blink_timer += clock.get_time()
        if blink_timer >= blink_interval:
            show_text = not show_text
            blink_timer = 0

        text = pygame.font.Font(pygame.font.match_font('SFNS Mono'), 80).render("The Da Vinci Code", True, BLACK)
        screen.blit(text, (80, (SCREEN_HEIGHT // 2) - 100))

        # Display text if `show_text` is True
        if show_text:
            text2 = pygame.font.Font(pygame.font.match_font('SFNS Mono'), 30).render("Press any key to start", True, BLACK)
            screen.blit(text2, (300, (SCREEN_HEIGHT // 2 + 20)))

        # Update the display
        pygame.display.flip()

        # Delay to manage frame rate
        clock.tick(60)

def winner_blink():
    running = True
    clock = pygame.time.Clock()

    # Timer variables for blinking
    blink_timer = 0
    show_text = True
    blink_interval = 500  # Blink interval in milliseconds

    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE:
                    running = False

        # Blink logic
        blink_timer += clock.get_time()
        if blink_timer >= blink_interval:
            show_text = not show_text
            blink_timer = 0

        # Display text if `show_text` is True
        if show_text:
            winner_text = pygame.font.Font(None, 80).render("YOU WIN", True, BLACK)
            screen.blit(winner_text, (200, (SCREEN_HEIGHT // 2) - 15))

        # Update the display
        pygame.display.flip()

        # Delay to manage frame rate
        clock.tick(60)

start_menu()
while True:
    main_menu(tiles1, tiles2)
    switch_turns()
    main_menu(tiles2, tiles1)
    switch_turns()

pygame.quit()
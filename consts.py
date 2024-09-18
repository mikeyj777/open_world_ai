class Consts:
    AGENT_CHANCE_OF_BEING_BAD = 0.2
    COORD_DISPLAY_ANCHOR_X = 10
    COORD_DISPLAY_ANCHOR_Y = 60
    AGENT_FIELD_CENTER = (0, 0, 0)  # Center of the circular field
    AGENT_FIELD_RADIUS = 50  # Radius of the circular field
    MIN_DISTANCE_BETWEEN_AGENTS_FOR_CONNECTION = 2  # Minimum distance between agents for connection
    MAX_AMOUNT_OF_ANY_RESOURCE = 15

    AGENT_COLORS = {
        "red": (255, 0, 0),
        "green": (0, 255, 0),
        "blue": (0, 0, 255),
        "yellow": (255, 255, 0),
        "cyan": (0, 255, 255),
        "magenta": (255, 0, 255),
        "white": (255, 255, 255),
    }

    AGENT_COLOR_DEAD_RGB = (255, 165, 0) # orange.  will flash before it dies.
import arcade
from menu import MenuView


def main():
    screen_width, screen_height = arcade.get_display_size()

    window = arcade.Window(screen_width, screen_height, "Chess")
    menu_view = MenuView("default", 1.0)
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    main()

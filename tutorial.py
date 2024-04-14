import arcade
import arcade.gui

SCREEN_WIDTH, SCREEN_HEIGHT = arcade.get_display_size()


class Page:
    def __init__(self, image):
        self.image = arcade.load_texture(image)

    def get_image(self):
        return arcade.gui.UISpriteWidget(sprite=arcade.Sprite(texture=self.image), width=SCREEN_WIDTH // 3,
                                         height=SCREEN_WIDTH // 3)


class SubMenu(arcade.gui.UIMouseFilterMixin, arcade.gui.UIAnchorLayout):
    """Acts like a fake view/window."""

    def __init__(self, title: str):
        super().__init__(size_hint=(1, 1))

        self.frame = None
        self.title_label = arcade.gui.UILabel(text=title, align="center", font_size=20, multiline=False,
                                              text_color=arcade.color.BLACK, width=700)

        # Adding some extra space around the title.
        self.title_label_space = arcade.gui.UISpace(height=10, width=700, color=arcade.color.BRUNSWICK_GREEN)
        self.button_space = arcade.gui.UISpace(height=40, width=510, color=arcade.color.WHITE)

        self.current_menu = 0  # Index of the current menu
        self.menus = []

        text = "The real danger is not that computers will begin to think like people, " \
               "but that people will begin " \
               "to think like computers. - Sydney Harris (Journalist)"

        Page_1 = Page("tutorial/1.png")
        Page_2 = Page("tutorial/2.png")
        Page_3 = Page("tutorial/3.png")
        Page_4 = Page("tutorial/4.png")
        Page_5 = Page("tutorial/5.png")
        Page_6 = Page("tutorial/6.png")

        self.menus.append(Page_1)
        self.menus.append(Page_2)
        self.menus.append(Page_3)
        self.menus.append(Page_4)
        self.menus.append(Page_5)
        self.menus.append(Page_6)

        self.grid = arcade.gui.UIGridLayout(column_count=9, row_count=1, horizontal_spacing=10, vertical_spacing=20)

        self.back_button = arcade.gui.UIFlatButton(text="X", width=30, height=30)

        # The type of event listener we used earlier for the button will not work here.
        self.back_button.on_click = self.on_click_back_button

        next_button = arcade.gui.UIFlatButton(text="Next", width=100, height=40)
        prev_button = arcade.gui.UIFlatButton(text="Prev", width=100, height=40)

        # Adding the buttons to the layout.
        self.grid.add(prev_button, col_num=0, row_num=0)
        self.grid.add(self.button_space, col_num=1, row_num=0)
        self.grid.add(next_button, col_num=8, row_num=0)

        self.create_page()

        @next_button.event("on_click")
        def on_click_switch_button(event):
            if self.current_menu < len(self.menus) - 1:
                self.current_menu = self.current_menu + 1
                self.create_page()

        @prev_button.event("on_click")
        def on_click_switch_button(event):
            if self.current_menu > 0:
                self.current_menu = self.current_menu - 1
                self.create_page()

    def create_page(self):
        self.frame = self.add(arcade.gui.UIAnchorLayout(width=800, height=600, size_hint=None))
        self.frame.with_padding(all=20)

        # Add a background to the window.
        # Nine patch smoothes the edges.
        self.frame.with_background(texture=arcade.load_texture(
            "assets/grey_panel.png"), start=(7, 7), end=(7, 7))

        widget_layout = arcade.gui.UIBoxLayout(align="center", space_between=10)
        widget_layout.add(self.title_label)
        widget_layout.add(self.title_label_space)
        widget_layout.add(self.menus[self.current_menu].get_image())

        self.frame.add(child=widget_layout, anchor_x="center", anchor_y="top")
        self.frame.add(child=self.grid, anchor_x="left", anchor_y="bottom", align_y=60, align_x=10)
        self.frame.add(child=self.back_button, anchor_x="right", anchor_y="top")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.current_menu = (self.current_menu - 1) % len(self.menus)
        elif key == arcade.key.RIGHT:
            self.current_menu = (self.current_menu + 1) % len(self.menus)
            # self.show_current_menu()

    def on_click_back_button(self, event):
        # Removes the widget from the manager.
        # After this the manager will respond to its events like it previously did.
        self.parent.remove(self)

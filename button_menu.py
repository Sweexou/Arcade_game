class Button:
    def __init__(self, image, pos, text_input, font, base_color, selected_color, hovering_color, grid_pos=None):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color = base_color
        self.selected_color = selected_color
        self.hovering_color = hovering_color
        self.text_input = text_input
        self.is_selected = False  # Track if the button is selected
        self.text = self.font.render(self.text_input, True, self.base_color)
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
        self.grid_pos = grid_pos  # New attribute to store grid position

    def update(self, screen):
        # Update text color based on selection state
        color = self.selected_color if self.is_selected else self.base_color
        self.text = self.font.render(self.text_input, True, color)
        screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        return self.rect.collidepoint(position)

    def select(self):
        self.is_selected = True

    def deselect(self):
        self.is_selected = False

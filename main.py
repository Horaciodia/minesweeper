import pygame, random, os, sys

pygame.init()

WIDTH, HEIGHT = 800, 500
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Minesweeper')

class Block:
    def __init__(self, is_mine, position, size, color):
        self.revealed = False
        self.is_mine = is_mine
        self.position = position
        self.size = size
        self.color = color
        self.rect = pygame.Rect(self.position[0], self.position[1], self.size, self.size)
        self.font = pygame.font.Font(None, 24)  
        self.marked = None

    def reveal(self):
        self.revealed = True

        if not self.is_mine:
            if (self.position[0] // 50 + self.position[1] // 50) % 2 == 0:
                self.color =  (173, 216, 230)
            else:
                self.color =  (144, 238, 144)
        else:
            self.color = (255, 0, 0)

    def draw(self, blocks):
        pygame.draw.rect(window, self.color, self.rect)
        if self.revealed:
            adjacent_mines = self.get_adjacent_mines(blocks)
            if len(adjacent_mines) > 0:
                text_surface = self.font.render(str(len(adjacent_mines)), True, (255, 0, 0))
                text_rect = text_surface.get_rect(center=self.rect.center)
                window.blit(text_surface, text_rect)

    def get_adjacent_mines(self, blocks):
        adjacent_mines = []
        for x in [-1, 0, 1]:
            for y in [-1, 0, 1]:
                if x == 0 and y == 0:
                    continue 
                neighbour_x = self.position[0] + x * self.size
                neighbour_y = self.position[1] + y * self.size
                for other_block in blocks:
                    if (other_block.position == (neighbour_x, neighbour_y)) and other_block.is_mine:
                        adjacent_mines.append(other_block)
        return adjacent_mines
    
    def get_adjacent_non_mines(self, blocks):
        non_mines_neighbours = []
        for x in [-1, 0, 1]:
            for y in [-1, 0, 1]:
                if x == 0 and y == 0:
                    continue
                neighbour_x = self.position[0] + x * self.size
                neighbour_y = self.position[1] + y * self.size
                for other_block in blocks:
                    if other_block.position == (neighbour_x, neighbour_y) and not other_block.is_mine:
                        non_mines_neighbours.append(other_block)

        return non_mines_neighbours

    def reveal_non_mines(self, blocks):
        queue = [self]
        visited = set()

        while queue:
            current = queue.pop(0)            
            visited.add(current)
            current.reveal()
            current.draw(blocks)

            adjacent_mines = current.get_adjacent_mines(blocks)

            for block in current.get_adjacent_non_mines(blocks):
                if block not in visited and block not in queue and not adjacent_mines:
                    queue.append(block)

    def flag(self):
        if not self.marked:
            self.marked = Flag((self.position[0] + 25, self.position[1] + 25), True)
        else:
            self.marked = None

class Flag:
    def __init__(self, position, center=False):
        current_dir = os.path.dirname(__file__)  
        image_path = os.path.join(current_dir, 'mark.png')
        self.flag_image = pygame.image.load(image_path)
        self.flag_rect = self.flag_image.get_rect()
        if center:
            self.flag_rect.center = position
        else:
            self.flag_rect.topleft = position
        self.flagged = False

    def draw(self):
        window.blit(self.flag_image, self.flag_rect)

    def flagging(self):
        self.flagged = not self.flagged

def main():
    blocks = []
    for x in range(0, 750, 50):
        for y in range(0, 500, 50):
            is_mine = False
            color = (255, 255, 153) if (x // 50 + y // 50) % 2 == 0 else (221, 160, 221)
            if random.uniform(0, 1) < 0.1:
                is_mine = True
            blocks.append(Block(is_mine, (x, y), 50, color))

    flag = Flag((760, 10))
    game_over = False
    font = pygame.font.Font(None, 54)
    all_non_mine_blocks = [block for block in blocks if not block.is_mine]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                pos = pygame.mouse.get_pos()
                for block in blocks:
                    if block.rect.collidepoint(pos) and not flag.flagged:
                        block.reveal()
                        if block.is_mine:
                            text_surface = font.render('Game over', True, (255, 255, 255))
                            text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                            game_over = True
                        else:                            
                            block.reveal_non_mines(blocks)     
                            non_mine_blocks = [block for block in blocks if not block.is_mine and block.revealed]
                            if non_mine_blocks == all_non_mine_blocks:
                                text_surface = font.render('You won!', True, (255, 255, 255))
                                text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                                game_over = True                       
                    elif block.rect.collidepoint(pos) and flag.flagged:
                        block.flag()

                    
                
                if flag.flag_rect.collidepoint(pos):
                    flag.flagging()

        if not game_over:
            for block in blocks:
                block.draw(blocks)
                if block.marked:
                    block.marked.draw()
            flag.draw()
        else:
            window.blit(text_surface, text_rect)    


        pygame.display.update()


main()
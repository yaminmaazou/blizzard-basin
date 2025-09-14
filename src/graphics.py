#type: ignore

from collections.abc import Iterable
from typing import Optional
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
import drawsvg as dsvg

from world import World
from state import State


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
PINK = (255, 0, 255)
GRAY = (100, 100, 100)


class Graphics():
    def __init__(self,
                world: World,
                player_x: Optional[int] = None,
                player_y: Optional[int] = None,
                ) -> None:
        pygame.init()
        MAX_SCREEN_WIDTH = pygame.display.Info().current_w
        MAX_SCREEN_HEIGHT = pygame.display.Info().current_h
        MAX_TILE_SIZE = 100
        MIN_TILE_SIZE = 10

        if MAX_SCREEN_WIDTH / world.width + 2 < MIN_TILE_SIZE:
            print("Error: World is too wide")
            quit()
        if MAX_SCREEN_HEIGHT / world.height + 2 < MIN_TILE_SIZE:
            print("Error: World is too tall")
            quit()

        self.world: World = world
        if player_x is not None and player_x < world.width and player_x >= 0:
            self.player_x = player_x + 1
        else:
            self.player_x = world.entry_x + 1
        if player_y is not None and player_y <= world.height and player_y >= -1:
            self.player_y = player_y + 1
        else:
            self.player_y = 0
        self.trajectory: list[tuple[int, int]] = [(self.player_x, self.player_y)]
        self.time: int = 0 # only used for manual mode

        self.grid_width: int = world.width + 2 # +2 for walls
        self.grid_height: int = world.height + 2
        self.tile_size: int = min(MAX_SCREEN_WIDTH // self.grid_width,
                                  MAX_SCREEN_HEIGHT // self.grid_height)
        if self.tile_size > MAX_TILE_SIZE:
            self.tile_size = MAX_TILE_SIZE
        
        self.margin: int = 5
        self.map_width: int = self.tile_size * self.grid_width
        self.map_height: int = self.tile_size * self.grid_height
        self.status_width: int = self.map_width
        self.status_height: int = 50
        self.screen_width: int = self.map_width + self.margin * 2
        self.screen_height: int = self.map_height + self.status_height + self.margin * 2

        self.map = pygame.Surface((self.map_width, self.map_height))
        self.status = pygame.Surface((self.status_width, self.status_height))
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Blizzard Basin")
        self.clock = pygame.time.Clock()

    def _draw_grid(self) -> None:
        for i in range(self.grid_width):
            pygame.draw.line(self.map, GRAY, (i * self.tile_size, 0),
                             (i * self.tile_size, self.screen_height))
        for i in range(self.grid_height):
            pygame.draw.line(self.map, GRAY, (0, i * self.tile_size),
                             (self.screen_width, i * self.tile_size))

    def _draw_walls(self) -> None:
        top_border = pygame.Rect(0, 0, self.grid_width * self.tile_size, self.tile_size)
        bottom_border = pygame.Rect(0,
                                    (self.grid_height - 1) * self.tile_size,
                                    self.grid_width * self.tile_size,
                                    self.tile_size)
        left_border = pygame.Rect(0, 0, self.tile_size, self.grid_height * self.tile_size)
        right_border = pygame.Rect((self.grid_width - 1) * self.tile_size,
                                    0,
                                    self.tile_size,
                                    self.grid_height * self.tile_size)

        pygame.draw.rect(self.map, BLACK, bottom_border)
        pygame.draw.rect(self.map, BLACK, left_border)
        pygame.draw.rect(self.map, BLACK, right_border)
        pygame.draw.rect(self.map, BLACK, top_border)
    
    def _draw_entry_exit(self) -> None:
        entry = pygame.Rect((self.world.entry_x + 1) * self.tile_size,
                            0,
                            self.tile_size,
                            self.tile_size)
        exit = pygame.Rect((self.world.exit_x + 1) * self.tile_size,
                            (self.grid_height - 1) * self.tile_size,
                            self.tile_size,
                            self.tile_size)
        pygame.draw.rect(self.map, GRAY, entry)
        pygame.draw.rect(self.map, GRAY, exit)
    
    def _draw_player(self) -> None:
        rect = pygame.Rect(self.player_x * self.tile_size,
                            self.player_y * self.tile_size,
                            self.tile_size,
                            self.tile_size)
        color = BLUE
        if self.world.is_dead(self.player_x - 1, self.player_y - 1):
            color = RED
        elif self.world.is_solved(self.player_x - 1, self.player_y - 1):
            color = GREEN
        pygame.draw.rect(self.map, color, rect)
    
    def _draw_blizzards(self) -> None:
        for i in range(self.world.height):
            for j in range(self.world.width):
                center_x = ((j + 1) * self.tile_size) + self.tile_size // 2
                center_y = ((i + 1) * self.tile_size) + self.tile_size // 2
                if self.world.map[i][j] & 1:
                    pygame.draw.line(self.map, BLACK,
                                        (center_x, center_y),
                                        (center_x - self.tile_size // 2, center_y))
                    pygame.draw.polygon(self.map, BLACK,
                                        [
                                        (center_x - self.tile_size // 3, center_y - self.tile_size // 4),
                                        (center_x - self.tile_size // 2, center_y),
                                        (center_x - self.tile_size // 3, center_y + self.tile_size // 4)],
                                        )
                if self.world.map[i][j] & 2:
                    pygame.draw.line(self.map, BLACK,
                                        (center_x, center_y),
                                        (center_x, center_y + self.tile_size // 2))
                    pygame.draw.polygon(self.map, BLACK,
                                        [
                                        (center_x - self.tile_size // 4, center_y + self.tile_size // 3),
                                        (center_x, center_y + self.tile_size // 2),
                                        (center_x + self.tile_size // 4, center_y + self.tile_size // 3)],
                                        )
                if self.world.map[i][j] & 4:
                    pygame.draw.line(self.map, BLACK,
                                        (center_x, center_y),
                                        (center_x + self.tile_size // 2, center_y))
                    pygame.draw.polygon(self.map, BLACK,
                                        [
                                        (center_x + self.tile_size // 3, center_y - self.tile_size // 4),
                                        (center_x + self.tile_size // 2, center_y),
                                        (center_x + self.tile_size // 3, center_y + self.tile_size // 4)],
                                        )
                if self.world.map[i][j] & 8:
                    pygame.draw.line(self.map, BLACK,
                                        (center_x, center_y),
                                        (center_x, center_y - self.tile_size // 2))
                    pygame.draw.polygon(self.map, BLACK,
                                        [
                                        (center_x - self.tile_size // 4, center_y - self.tile_size // 3),
                                        (center_x, center_y - self.tile_size // 2),
                                        (center_x + self.tile_size // 4, center_y - self.tile_size // 3)],
                                        )
    
    def _draw_trajectory(self) -> None:
        for i in range(len(self.trajectory) - 1):
            pygame.draw.line(self.map, PINK,
                            (self.trajectory[i][0] * self.tile_size + self.tile_size // 2,
                             self.trajectory[i][1] * self.tile_size + self.tile_size // 2),
                            (self.trajectory[i + 1][0] * self.tile_size + self.tile_size // 2,
                             self.trajectory[i + 1][1] * self.tile_size + self.tile_size // 2),
                            width=2)

    def _draw_status(self) -> None:
        self.status.fill(WHITE)
        font = pygame.font.SysFont("Arial", 40)
        text = font.render(f"Step: {self.time}", True, BLACK)
        self.status.blit(text, (0, 0))

        font = pygame.font.SysFont("Arial", 25)
        text = font.render("Spacebar: Step   Enter: Run/Pause   ESC: Quit", True, BLACK)
        self.status.blit(text, (180, 0))

    def _draw_all(self) -> None:
        self.map.fill(WHITE)
        self.screen.fill(WHITE)
        self._draw_walls()
        self._draw_entry_exit()
        self._draw_player()
        self._draw_blizzards()
        self._draw_grid()
        self._draw_trajectory()
        self._draw_status()
        self.screen.blit(self.map, (self.margin, self.margin))
        self.screen.blit(self.status, (self.margin, self.map_height + self.margin))
        pygame.display.flip()
    
    def draw_svg(self, filename: str) -> None:
        svg = dsvg.Drawing(self.map_width, self.map_height)
        svg.append(dsvg.Rectangle(0, 0, self.map_width, self.map_height, fill='white'))

        # Draw walls
        top_border = dsvg.Rectangle(0, 0, self.map_width, self.tile_size, fill='black')
        bottom_border = dsvg.Rectangle(0, (self.grid_height - 1) * self.tile_size,
                                       self.map_width, self.tile_size, fill='black')
        left_border = dsvg.Rectangle(0, 0, self.tile_size, self.map_height, fill='black')
        right_border = dsvg.Rectangle((self.grid_width - 1) * self.tile_size, 0,
                                       self.tile_size, self.map_height, fill='black')
        svg.append(top_border)
        svg.append(bottom_border)
        svg.append(left_border)
        svg.append(right_border)

        # Draw entry and exit
        entry = dsvg.Rectangle((self.world.entry_x + 1) * self.tile_size, 0,
                               self.tile_size, self.tile_size, fill="#A3A3A3")
        exit = dsvg.Rectangle((self.world.exit_x + 1) * self.tile_size,
                               (self.grid_height - 1) * self.tile_size,
                               self.tile_size, self.tile_size, fill='#A3A3A3')
        svg.append(entry)
        svg.append(exit)
        # Draw player
        player_rect = dsvg.Rectangle(self.player_x * self.tile_size,
                                     self.player_y * self.tile_size,
                                     self.tile_size, self.tile_size,
                                     fill='blue')
        svg.append(player_rect)

        # Draw blizzards
        for i in range(self.world.height):
            for j in range(self.world.width):
                center_x = ((j + 1) * self.tile_size) + self.tile_size // 2
                center_y = ((i + 1) * self.tile_size) + self.tile_size // 2
                if self.world.map[i][j] & 1:
                    svg.append(dsvg.Line(center_x + 1, center_y,
                                         center_x - self.tile_size // 2.2, center_y,
                                         stroke='black', stroke_width=2))
                    svg.append(dsvg.Lines(center_x - self.tile_size // 3, center_y - self.tile_size // 4,
                                         center_x - self.tile_size // 2 + 0.5, center_y,
                                        center_x - self.tile_size // 3, center_y + self.tile_size // 4,
                                        close=True,
                                            stroke='none',
                                             fill='black'))
                if self.world.map[i][j] & 2:
                    svg.append(dsvg.Line(center_x, center_y - 1,
                                         center_x, center_y + self.tile_size // 2.2,
                                         stroke='black', stroke_width=2))
                    svg.append(dsvg.Lines(center_x - self.tile_size // 4, center_y + self.tile_size // 3,
                                         center_x, center_y + self.tile_size // 2 - 0.5,
                                         center_x + self.tile_size // 4, center_y + self.tile_size // 3,
                                         close=True,
                                             stroke='none',
                                             fill='black'))
                if self.world.map[i][j] & 4:
                    svg.append(dsvg.Line(center_x + 1, center_y,
                                         center_x + self.tile_size // 2.2, center_y,
                                         stroke='black', stroke_width=2))
                    svg.append(dsvg.Lines(center_x + self.tile_size // 3, center_y - self.tile_size // 4,
                                         center_x + self.tile_size // 2 - 0.5, center_y,
                                         center_x + self.tile_size // 3, center_y + self.tile_size // 4,
                                         close=True,
                                             stroke='none',
                                             fill='black'))
                if self.world.map[i][j] & 8:
                    svg.append(dsvg.Line(center_x, center_y + 1,
                                         center_x, center_y - self.tile_size // 2.2,
                                         stroke='black', stroke_width=2))
                    svg.append(dsvg.Lines(center_x - self.tile_size // 4, center_y - self.tile_size // 3,
                                         center_x, center_y - self.tile_size // 2 + 0.5,
                                         center_x + self.tile_size // 4, center_y - self.tile_size // 3,
                                         close=True,
                                             stroke='none',
                                             fill='black'))
        
        # Draw grid
        for i in range(self.grid_width + 1):
            svg.append(dsvg.Line(i * self.tile_size, 0,
                                 i * self.tile_size, self.map_height,
                                 stroke='gray', stroke_width=1))
        for i in range(self.grid_height + 1):
            svg.append(dsvg.Line(0, i * self.tile_size,
                                 self.map_width, i * self.tile_size,
                                 stroke='gray', stroke_width=1))
        
        # Draw trajectory
        for i in range(len(self.trajectory) - 1):
            svg.append(dsvg.Line(self.trajectory[i][0] * self.tile_size + self.tile_size // 2,
                                 self.trajectory[i][1] * self.tile_size + self.tile_size // 2,
                                 self.trajectory[i + 1][0] * self.tile_size + self.tile_size // 2,
                                 self.trajectory[i + 1][1] * self.tile_size + self.tile_size // 2,
                                 stroke='#FF00FF', stroke_width=2))

        svg.save_svg(filename)

    # manual mode
    def _move_player(self, dx: int, dy: int) -> None:
        new_x = self.player_x + dx
        new_y = self.player_y + dy
        if new_x < 1 or new_x >= self.grid_width - 1:
            return
        if new_y < 0 or new_y >= self.grid_height:
            return
        if new_y == 0 and new_x != self.world.entry_x + 1:
            return
        if new_y == self.grid_height - 1 and new_x != self.world.exit_x + 1:
            return
        self.player_x = new_x
        self.player_y = new_y
        self.trajectory.append((self.player_x, self.player_y))
        self.world.step()
        self.time += 1
    
    def _step(self, step: State) -> None:
        self.player_x = step.player_x + 1
        self.player_y = step.player_y + 1
        self.trajectory.append((self.player_x, self.player_y))
        self.world.step()
        self.time += 1
    
    def run(self, steps: Iterable[State]) -> None:
        if not steps:
            print("No steps to run.")
            return
        iterator = iter(steps)
        step: State = next(iterator)
        self.player_x = step.player_x + 1
        self.player_y = step.player_y + 1
        self.trajectory.append((self.player_x, self.player_y))

        autorun = False
        finished = False
        running = True
        while running:
            self._draw_all()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        break
                    elif event.key == pygame.K_SPACE:
                        if not autorun and not finished:
                            try:
                                step = next(iterator)
                                self._step(step)
                            except StopIteration:
                                finished = True
                                break
                    elif event.key == pygame.K_RETURN:
                        if not finished:
                            autorun = not autorun
                    elif event.key == pygame.K_x:
                        print("Saving current frame to output.svg")
                        self.draw_svg("output.svg")

            if autorun and not finished:
                try:
                    step = next(iterator)
                    self._step(step)
                except StopIteration:
                    finished = True
            self.clock.tick(60)
        pygame.quit()

    def run_manual(self) -> None:
        running = True
        while running:
            self._draw_all()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self._move_player(-1, 0)
                    elif event.key == pygame.K_RIGHT:
                        self._move_player(1, 0)
                    elif event.key == pygame.K_UP:
                        self._move_player(0, -1)
                    elif event.key == pygame.K_DOWN:
                        self._move_player(0, 1)
                    elif event.key == pygame.K_SPACE:
                        self.world.step()
                        self.time += 1
                    elif event.key == pygame.K_x:
                        print("Saving current frame to output.svg")
                        self.draw_svg("output.svg")
                    elif event.key == pygame.K_ESCAPE:
                        running = False
                        break

            self.clock.tick(60)

        pygame.quit()
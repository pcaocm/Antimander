import sys, random
import pygame
from pygame import gfxdraw

from map import Map
from partition import Partition

from metrics import compactness_district_centers as cdc, efficiency_gap

m = Map.makeRandom(100, seed=0)
p = Partition.makeRandom(8, m, seed=None)

pygame.init()
screen = pygame.display.set_mode((600, 600))
screen.fill((255, 255, 255))
font = pygame.font.SysFont("comicsansms", 14)

def draw_map(map):
    for i, vertices in enumerate(map.tile_vertices):
        vertices = [ (x*600, y*600) for x,y in vertices ]

        if map.tile_boundaries[i]:
            gfxdraw.filled_polygon(screen, vertices, (200, 100, 100))
        else:
            gfxdraw.filled_polygon(screen, vertices, (100, 100, 100))
        gfxdraw.aapolygon(screen, vertices, (50, 50, 50))

    for i, vertices in enumerate(map.tile_vertices):
        x1, y1 = map.tile_centers[i]
        v1 = (int(x1*600), int(y1*600))
        for j in map.tile_neighbours[i]:
            x2, y2 = map.tile_centers[j]
            v2 = (int(x2*600), int(y2*600))
            pygame.draw.line(screen, (200, 0, 0), v1, v2, 1)
        # for edge in tile.edges:
        #     if edge.neighbour:
        #         if p.tile2district[tile] == p.tile2district[edge.neighbour]:
        #             x2, y2 = edge.neighbour.center
        #             v2 = (int(x2*600), int(y2*600))


def draw_partition(partition, colors):
    m = partition.map

    for i in range(m.n_tiles):
        vertices = [ (x*600, y*600) for x,y in m.tile_vertices[i] ]
        district = partition.tile_districts[i]


        gfxdraw.filled_polygon(screen, vertices, colors[district] )
        gfxdraw.aapolygon(screen, vertices, (50, 50, 50))

        x,y = m.tile_centers[i]
        v = (int(x*600), int(y*600))

        # if i in partition.district_frontiers[district]:
        #     pygame.draw.circle(screen, (0,0,200), v, 5)

        # if p.tileIsFrontier(i):
        #     pygame.draw.circle(screen, (200,0,0), v, 3)

        # text = font.render(f'{i}: {district}', True, (20, 20, 20))
        # screen.blit(text, (v[0]-20, v[1]))

colors = [ [ random.randint(0, 255) for _ in range(3) ]
           for _ in range(p.n_districts) ]

mutate = False
draw_partition(p, colors)
print(efficiency_gap(m, p))

while True:
    if mutate:
        p2 = p.copy()
        p2.mutate()
        if cdc(m, p2) < cdc(m, p):
            p = p2
            print('better')
            draw_partition(p, colors)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()
            elif event.key == pygame.K_LEFT:
                p.mutate()
                draw_partition(p, colors)
                # pass
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    pygame.display.update()
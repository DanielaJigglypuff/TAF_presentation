import math
import numpy as np
import pygame
from pygame.locals import *
import Spline as SP

class RacingLineGame:
    def __init__(self):
        # Initialize the RacingLineGame object
        self.path = SP.Spline()  # Spline object representing the path
        self.trackLeft = SP.Spline()  # Spline object representing the left track boundary
        self.trackRight = SP.Spline()  # Spline object representing the right track boundary
        self.racingLine = SP.Spline()  # Spline object representing the racing line
        self.nNodes = 20  # Number of nodes on the track
        self.fDisplacement = [0] * self.nNodes  # Displacement of each node on the racing line
        self.nIterations = 1  # Number of iterations for the racing line optimization
        self.fMarker = 1.0  # Marker for the position on the racing line
        self.nSelectedNode = -1  # Index of the selected node
        self.vecModelCar = [[2, 0], [0, -1], [0, 1]]  # Model for drawing the car
        self.font_width = 8  # Set the font width
        self.font_height = 8  # Set the font height
        self.screen = None  # Pygame screen object
        self.font = None  # Pygame font object
        self.clock = None  # Pygame clock object
        self.fElapsed = 0.0  # Elapsed time since the last frame

    def ConstructConsole(self, width, height, font_width, font_height):
        # Initialize the Pygame console window
        pygame.init()
        self.screen = pygame.display.set_mode((width * font_width, height * font_height))
        self.font = pygame.font.Font(None, font_height)
        self.clock = pygame.time.Clock()
        self.fElapsed = 0.0

    def Start(self):
        # Start the game loop
        bGameRunning = True
        while bGameRunning:
            for event in pygame.event.get():
                if event.type == QUIT:
                    bGameRunning = False

            self.fElapsed += self.clock.tick() / 1000.0
            if self.fElapsed > 0.0333:
                self.fElapsed -= 0.0333

                self.OnUserUpdate(self.fElapsed)
                pygame.display.set_caption(self.m_sAppName + " - FPS: " + str(int(self.clock.get_fps())))
                pygame.display.flip()

        pygame.quit()

    def Fill(self, x1, y1, x2, y2, color):
        # Fill a rectangle with the specified color on the screen
        pygame.draw.rect(self.screen, color, pygame.Rect(x1, y1, x2 - x1, y2 - y1))

    def Draw(self, x, y, c, col):
        # Draw a character with the specified color at the given position on the screen
        self.screen.blit(self.font.render(c, True, col), (x * self.font_width, y * self.font_height))

    def GetMouseX(self):
        # Get the x-coordinate of the mouse cursor
        return pygame.mouse.get_pos()[0] // self.font_width

    def GetMouseY(self):
        # Get the y-coordinate of the mouse cursor
        return pygame.mouse.get_pos()[1] // self.font_height

    def DrawWireFrameModel(self, model, x, y, angle, scale, color):
        # Draw a wireframe model at the given position with the specified angle, scale, and color
        for i in range(len(model)):
            x1 = model[i][0] * scale
            y1 = model[i][1] * scale
            x2 = model[(i + 1) % len(model)][0] * scale
            y2 = model[(i + 1) % len(model)][1] * scale

            x1r = math.cos(angle) * x1 - math.sin(angle) * y1
            y1r = math.sin(angle) * x1 + math.cos(angle) * y1
            x2r = math.cos(angle) * x2 - math.sin(angle) * y2
            y2r = math.sin(angle) * x2 + math.cos(angle) * y2

            x1r += x
            y1r += y
            x2r += x
            y2r += y

            pygame.draw.line(self.screen, color, (x1r, y1r), (x2r, y2r))

    def OnUserCreate(self):
        # Initialize the game state
        for i in range(self.nNodes):
            self.trackLeft.points.append([0.0, 0.0, 0.0])
            self.trackRight.points.append([0.0, 0.0, 0.0])
            self.racingLine.points.append([0.0, 0.0, 0.0])

        # A handcrafted track
        self.path.points = [
            [81.8, 195.0, 0.0], [108.0, 210.0, 0.0], [152.0, 216.0, 0.0],
            [182.0, 185.6, 0.0], [190.0, 159.0, 0.0], [198.0, 122.0, 0.0], [226.0, 93.0, 0.0],
            [224.0, 41.0, 0.0], [204.0, 15.0, 0.0], [158.0, 24.0, 0.0], [146.0, 52.0, 0.0],
            [157.0, 93.0, 0.0], [124.0, 129.0, 0.0], [83.0, 104.0, 0.0], [77.0, 62.0, 0.0],
            [40.0, 57.0, 0.0], [21.0, 83.0, 0.0], [33.0, 145.0, 0.0], [30.0, 198.0, 0.0],
            [48.0, 210.0, 0.0]
        ]

        self.vecModelCar = [[2, 0], [0, -1], [0, 1]]

        self.path.UpdateSplineProperties()

    def OnUserUpdate(self, fElapsedTime):
        # Clear the screen
        self.Fill(0, 0, self.screen.get_width(), self.screen.get_height(), (0, 55, 0))

        # Handle iteration count
        if pygame.key.get_pressed()[pygame.K_w]:
            self.nIterations += 1
        if pygame.key.get_pressed()[K_s]:
            self.nIterations -= 1
        if self.nIterations < 0:
            self.nIterations = 0

        # Check if node is selected with the mouse
        if pygame.mouse.get_pressed()[0]:
            for i in range(len(self.path.points)):
                d = math.sqrt(
                    (self.path.points[i][0] - self.GetMouseX()) ** 2 +
                    (self.path.points[i][1] - self.GetMouseY()) ** 2
                )
                if d < 5.0:
                    self.nSelectedNode = i
                    break

        if not pygame.mouse.get_pressed()[0]:
            self.nSelectedNode = -1

        # Move the selected node
        if pygame.mouse.get_pressed()[0] and self.nSelectedNode >= 0:
            self.path.points[self.nSelectedNode][0] = self.GetMouseX()
            self.path.points[self.nSelectedNode][1] = self.GetMouseY()
            self.path.UpdateSplineProperties()

        # Move the car around the racing line
        self.fMarker += 2.0 * fElapsedTime
        if self.fMarker >= self.racingLine.fTotalSplineLength:
            self.fMarker -= self.racingLine.fTotalSplineLength

        # Calculate track boundary points
        fTrackWidth = 10.0
        for i in range(len(self.path.points)):
            p1 = self.path.GetSplinePoint(i)
            g1 = self.path.GetSplineGradient(i)
            glen = math.sqrt(g1[0] * g1[0] + g1[1] * g1[1])

            self.trackLeft.points[i][0] = p1[0] + fTrackWidth * (-g1[1] / glen)
            self.trackLeft.points[i][1] = p1[1] + fTrackWidth * (g1[0] / glen)
            self.trackRight.points[i][0] = p1[0] - fTrackWidth * (-g1[1] / glen)
            self.trackRight.points[i][1] = p1[1] - fTrackWidth * (g1[0] / glen)

        # Draw Track
        fRes = 0.2
        for t in np.arange(0.0, len(self.path.points), fRes):
            pl1 = self.trackLeft.GetSplinePoint(t)
            pr1 = self.trackRight.GetSplinePoint(t)
            pl2 = self.trackLeft.GetSplinePoint(t + fRes)
            pr2 = self.trackRight.GetSplinePoint(t + fRes)

            pygame.draw.polygon(self.screen, (128, 128, 128), [(pl1[0], pl1[1]), (pr1[0], pr1[1]), (pr2[0], pr2[1])])
            pygame.draw.polygon(self.screen, (128, 128, 128), [(pl1[0], pl1[1]), (pl2[0], pl2[1]), (pr2[0], pr2[1])])

        # Reset the racing line
        for i in range(len(self.racingLine.points)):
            self.racingLine.points[i] = self.path.points[i][:]
            self.fDisplacement[i] = 0.0
        self.racingLine.UpdateSplineProperties()

        for n in range(self.nIterations):
            for i in range(len(self.racingLine.points)):
                # Get locations of neighbor nodes
                pointRight = self.racingLine.points[(i + 1) % len(self.racingLine.points)]
                pointLeft = self.racingLine.points[(i + len(self.racingLine.points) - 1) % len(self.racingLine.points)]
                pointMiddle = self.racingLine.points[i]

                # Create vectors to neighbors
                vectorLeft = [pointLeft[0] - pointMiddle[0], pointLeft[1] - pointMiddle[1]]
                vectorRight = [pointRight[0] - pointMiddle[0], pointRight[1] - pointMiddle[1]]

                # Normalize neighbors
                lengthLeft = math.sqrt(vectorLeft[0] * vectorLeft[0] + vectorLeft[1] * vectorLeft[1])
                leftn = [vectorLeft[0] / lengthLeft, vectorLeft[1] / lengthLeft]
                lengthRight = math.sqrt(vectorRight[0] * vectorRight[0] + vectorRight[1] * vectorRight[1])
                rightn = [vectorRight[0] / lengthRight, vectorRight[1] / lengthRight]

                # Add together to create bisector vector
                vectorSum = [rightn[0] + leftn[0], rightn[1] + leftn[1]]
                glen = math.sqrt(vectorSum[0] * vectorSum[0] + vectorSum[1] * vectorSum[1])
                vectorSum[0] /= glen
                vectorSum[1] /= glen

                # Get point gradient and normalize
                g = self.path.GetSplineGradient(i)
                glen = math.sqrt(g[0] * g[0] + g[1] * g[1])
                g[0] /= glen
                g[1] /= glen

                # Project required correction onto point tangent to give displacement
                dp = -g[1] * vectorSum[0] + g[0] * vectorSum[1]

                # Shortest path
                self.fDisplacement[i] += dp * 0.3

                # Curvature
                # self.fDisplacement[(i + 1) % len(self.racingLine.points)] += dp * -0.2
                # self.fDisplacement[(i - 1 + len(self.racingLine.points)) % len(self.racingLine.points)] += dp * -0.2

            # Clamp displaced points to track width
            for i in range(len(self.racingLine.points)):
                if self.fDisplacement[i] >= fTrackWidth:
                    self.fDisplacement[i] = fTrackWidth
                if self.fDisplacement[i] <= -fTrackWidth:
                    self.fDisplacement[i] = -fTrackWidth

                g = self.path.GetSplineGradient(i)
                glen = math.sqrt(g[0] * g[0] + g[1] * g[1])
                g[0] /= glen
                g[1] /= glen

                self.racingLine.points[i][0] = self.path.points[i][0] + -g[1] * self.fDisplacement[i]
                self.racingLine.points[i][1] = self.path.points[i][1] + g[0] * self.fDisplacement[i]


        self.path.DrawSelf(self, 0, 0)
        self.racingLine.UpdateSplineProperties()
        self.racingLine.DrawSelf(self, 0, 0)

        for i in self.path.points:
            self.Fill(i[0] - 1, i[1] - 1, i[0] + 2, i[1] + 2, (255, 0, 0))

        car_p = self.racingLine.GetSplinePoint(self.fMarker)
        car_g = self.racingLine.GetSplineGradient(self.fMarker)
        self.DrawWireFrameModel(self.vecModelCar, car_p[0], car_p[1], math.atan2(car_g[1], car_g[0]), 3.0, (0, 0, 0))

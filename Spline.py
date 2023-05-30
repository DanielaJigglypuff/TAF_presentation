import math
import numpy as np
import pygame
from pygame.locals import *

class Spline:
    def __init__(self):
        self.points = []
        # List to store the control points of the spline curve
        self.fTotalSplineLength = 0.0
        # Total length of the spline curve
        self.bIsLooped = True
        # Flag indicating whether the spline is looped (cyclic)

    def GetSplinePoint(self, t):
        p0, p1, p2, p3 = 0, 0, 0, 0
        # Variables to store the indices of control points

        if not self.bIsLooped:
            # If the spline is not looped
            p1 = int(t) + 1
            p2 = p1 + 1
            p3 = p2 + 1
            p0 = p1 - 1
            # Set the indices of control points based on the current value of 't'
        else:
            # If the spline is looped
            p1 = int(t) % len(self.points)
            p2 = (p1 + 1) % len(self.points)
            p3 = (p2 + 1) % len(self.points)
            p0 = p1 - 1 if p1 >= 1 else len(self.points) - 1
            # Set the indices of control points based on the current value of 't' and handle edge cases

        t = t - int(t)
        # Adjust 't' to be in the range [0, 1)

        tt = t * t
        ttt = tt * t
        # Calculate t^2 and t^3

        q1 = -ttt + 2.0 * tt - t
        q2 = 3.0 * ttt - 5.0 * tt + 2.0
        q3 = -3.0 * ttt + 4.0 * tt + t
        q4 = ttt - tt
        # Calculate interpolation factors for cubic Hermite spline interpolation

        tx = 0.5 * (self.points[p0][0] * q1 + self.points[p1][0] * q2 + self.points[p2][0] * q3 + self.points[p3][0] * q4)
        ty = 0.5 * (self.points[p0][1] * q1 + self.points[p1][1] * q2 + self.points[p2][1] * q3 + self.points[p3][1] * q4)
        # Calculate the interpolated x and y coordinates based on the control points and interpolation factors

        return [tx, ty]
        # Return the calculated spline point

    def GetSplineGradient(self, t):
        p0, p1, p2, p3 = 0, 0, 0, 0
        # Variables to store the indices of control points

        if not self.bIsLooped:
            # If the spline is not looped
            p1 = int(t) + 1
            p2 = p1 + 1
            p3 = p2 + 1
            p0 = p1 - 1
            # Set the indices of control points based on the current value of 't'
        else:
            # If the spline is looped
            p1 = int(t) % len(self.points)
            p2 = (p1 + 1) % len(self.points)
            p3 = (p2 + 1) % len(self.points)
            p0 = p1 - 1 if p1 >= 1 else len(self.points) - 1
            # Set the indices of control points based on the current value of 't' and handle edge cases

        t = t - int(t)
        # Adjust 't' to be in the range [0, 1)

        tt = t * t
        ttt = tt * t
        # Calculate t^2 and t^3

        q1 = -3.0 * tt + 4.0 * t - 1.0
        q2 = 9.0 * tt - 10.0 * t
        q3 = -9.0 * tt + 8.0 * t + 1.0
        q4 = 3.0 * tt - 2.0 * t
        # Calculate interpolation factors for the derivative of the cubic Hermite spline

        tx = 0.5 * (self.points[p0][0] * q1 + self.points[p1][0] * q2 + self.points[p2][0] * q3 + self.points[p3][0] * q4)
        ty = 0.5 * (self.points[p0][1] * q1 + self.points[p1][1] * q2 + self.points[p2][1] * q3 + self.points[p3][1] * q4)
        # Calculate the interpolated x and y components of the gradient vector

        return [tx, ty]
        # Return the calculated gradient vector

    def CalculateSegmentLength(self, node):
        fLength = 0.0
        fStepSize = 0.1
        # Initialize the length of the segment to 0 and set the step size for calculating the length

        old_point = self.GetSplinePoint(float(node))
        # Get the initial point on the spline corresponding to the given node parameter

        for t in np.arange(0.0, 1.0, fStepSize):
            # Iterate over a range of values from 0.0 to 1.0 with a step size of 'fStepSize'

            new_point = self.GetSplinePoint(float(node) + t)
            # Calculate a new point on the spline curve by adding the current value of 't' to the given node parameter
            # Call the 'GetSplinePoint' method to retrieve the new point

            fLength += math.sqrt((new_point[0] - old_point[0]) ** 2 + (new_point[1] - old_point[1]) ** 2)
            # Calculate the Euclidean distance between the 'new_point' and 'old_point' using the Pythagorean theorem
            # Add the distance to the 'fLength' variable
            # This step calculates the length of the current segment of the spline curve

            old_point = new_point
            # Update the value of 'old_point' with the value of 'new_point' for the next iteration of the loop

        return fLength
        # After iterating through all the sample points along the spline curve, return the calculated length of the segment

    def GetNormalisedOffset(self, p):
        i = 0
        # Initialize the index variable 'i' to 0

        while p > self.points[i][2]:
            p -= self.points[i][2]
            i += 1
            # Subtract the segment length of each control point from 'p' until 'p' becomes less than or equal to the segment length
            # Increment the index 'i' to move to the next control point

        return float(i) + (p / self.points[i][2])
        # Return the normalized offset value by adding the index 'i' and the ratio of 'p' to the segment length of the current control point

    def UpdateSplineProperties(self):
        self.fTotalSplineLength = 0.0
        # Initialize the total spline length to 0

        if self.bIsLooped:
            # If the spline is looped
            for i in range(len(self.points)):
                self.points[i][2] = self.CalculateSegmentLength(i)
                # Calculate the segment length of each control point and store it in the third element of the control point's sublist
                self.fTotalSplineLength += self.points[i][2]
                # Add the segment length to the total spline length
        else:
            # If the spline is not looped
            for i in range(1, len(self.points) - 2):
                self.points[i][2] = self.CalculateSegmentLength(i)
                # Calculate the segment length of each internal control point and store it in the third element of the control point's sublist
                self.fTotalSplineLength += self.points[i][2]
                # Add the segment length to the total spline length

    def DrawSelf(self, gfx, ox, oy, c=0x2588, col=0x000F):
        if self.bIsLooped:
            # If the spline is looped
            for t in np.arange(0.0, float(len(self.points)) - 0, 0.005):
                pos = self.GetSplinePoint(t)
                gfx.Draw(int(pos[0]), int(pos[1]), chr(c), col)
                # Iterate over the range of values from 0.0 to the length of the control point list
                # Calculate the corresponding spline point for each value of 't'
                # Convert the spline point coordinates to integers and draw the point on the graphics object 'gfx'
        else:
            # If the spline is not looped
            for t in np.arange(0.0, float(len(self.points)) - 3, 0.005):
                pos = self.GetSplinePoint(t)
                gfx.Draw(int(pos[0]), int(pos[1]), chr(c), col)
                # Iterate over the range of values from 0.0 to the length of the control point list minus 3
                # Calculate the corresponding spline point for each value of 't'
                # Convert the spline point coordinates to integers and draw the point on the graphics object 'gfx'

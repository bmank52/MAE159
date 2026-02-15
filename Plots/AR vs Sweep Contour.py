import matplotlib.pyplot as plt
import numpy as np

# Data from your image
ar = [8, 8, 8, 10, 10, 10, 12, 12, 12]
sweep = [30, 35, 40, 30, 35, 40, 30, 35, 40]
weight = [430000, 420000, 400000, 455000, 445000, 410000, 480000, 470000, 430000]

plt.figure(figsize=(8, 6))
# Create the filled contour
cp = plt.tricontourf(sweep, ar, weight, cmap='viridis')
plt.colorbar(cp, label='Weight (lbs)')

# Add the contour lines and labels
lines = plt.tricontour(sweep, ar, weight, colors='black')
plt.clabel(lines, inline=True, fontsize=10)

# MARK YOUR CHOSEN AIRCRAFT (AR=8, Sweep=40)
plt.plot(40, 8, 'ro', markersize=10, label='Chosen Aircraft')

plt.xlabel('Sweep (degrees)')
plt.ylabel('Aspect Ratio (AR)')
plt.title('Weight Contour vs AR and Sweep')
plt.legend()
plt.show()
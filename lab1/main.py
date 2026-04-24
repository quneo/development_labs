import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, MultipleLocator
import numpy as np
from math import pi


x1 = np.linspace(0, 2*pi, num=101)
y1 = np.sin(x1*x1 - 8*x1)+ 2 * np.cos(3*x1)

x2 = np.linspace(0, 2*pi, num=50)
y2 = np.sin(x2*x2)+ np.cos(x2*x2/4)

fig, ax = plt.subplots(figsize=(10, 5))
fig.patch.set_facecolor("khaki")
ax.set_facecolor("salmon")
#ax.step(x1, y1, linewidth=2, marker='o', label="sin(x^2 - 8x) + 2cos(3x)", markerfacecolor='tab:blue', markerfacecoloralt='lightsteelblue', markeredgecolor='brown')
#ax.step(x2, y2, linewidth=2, marker='p', label="sin(x^2)+cos(x^2/4)")

ax.plot(x1, y1, drawstyle="steps-pre", color="cyan", linestyle="-", linewidth=2.0, zorder=2)
ax.plot(x1, y1, drawstyle="steps-pre", color="red", linestyle="--", linewidth=2.0, zorder=3)
line1 = plt.Line2D(x1, y1, marker="o", markersize=8,
                       markerfacecolor="blue", markerfacecoloralt="magenta",
                       fillstyle="left", markeredgecolor="black", markeredgewidth=0.75,
                       linestyle="None", zorder=6)
line1.set_label("sin(x^2 - 8x) + cos(3x)")
ax.add_line(line1)


ax.plot(x2, y2, drawstyle="steps-post", color="cyan", linestyle="-", linewidth=2.0, zorder=2)
ax.plot(x2, y2, drawstyle="steps-post", color="blue", linestyle="--", linewidth=2.0, zorder=4)
line2 = plt.Line2D(x2, y2, marker="H", markersize=10,
                       markerfacecolor="orange", markeredgecolor="black", markeredgewidth=0.75,
                       linestyle="None", zorder=6)
line2.set_label("sin(x^2) + cos(x^2/4)")
ax.add_line(line2)

ax.set_xticks(np.arange(0, 2*np.pi+0.01, np.pi/4))

labels = ['$0$', r'$\pi/4$', r'$\pi/2$', r'$3\pi/4$', r'$\pi$',
          r'$5\pi/4$', r'$3\pi/2$', r'$7\pi/4$', r'$2\pi$']

ax.set_xticklabels(labels)


ax.set(xlim=(0, 2*pi), xlabel="x")
ax.set(ylim=(-3, 3), xlabel="y")
ax.legend(fontsize=7, loc='upper left')

# ax.grid(which='major', axis='both', linestyle='-', linewidth=1)
# ax.minorticks_on()
# ax.grid(which='minor', axis='both', linestyle=':', linewidth=0.5, color='gray')
#ax.grid(which='minor', axis='both', linestyle=':', linewidth=0.3, color='gray')

# grid_points = np.arange(0, 2*pi, step=pi/4)
# ax.xaxis.set_ticks(grid_points)
# ax.grid(which='major', axis='both', linestyle='-', linewidth=1)

# grid_points = np.arange(0, 2*pi, step=pi/8)
# ax.xaxis.set_ticks(grid_points)
# ax.grid(which='minor', axis='both', linestyle=':', linewidth=0.3, color='gray')


major_step = pi/4
ax.xaxis.set_major_locator(MultipleLocator(major_step))
ax.yaxis.set_major_locator(MultipleLocator(1.5)) 

ax.grid(which='major', linestyle='--', linewidth='1', color='black')

minor_step = major_step/2
ax.xaxis.set_minor_locator(MultipleLocator(minor_step))
ax.yaxis.set_minor_locator(MultipleLocator(0.75)) 


ax.grid(which='minor', linestyle=':', linewidth='0.75', color='black', alpha=0.7)
ax.minorticks_on()
ax.grid(True)

plt.title("Functions")
plt.tight_layout()
plt.savefig("output.png", dpi=400)
from matplotlib import pyplot as plt
import numpy as np

plt.xkcd()

fig = plt.figure()
ax = fig.add_axes((0.1, 0.2, 0.8, 0.7))
ax.spines['top'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.set_xlim([0, 10])
ax.set_ylim([0, 10])
ax.set_xticks([])
ax.set_yticks([])

ax.axhline(y=5, color="black", linestyle="-")
ax.axvline(x=5, color="black", linestyle="-")

ax.text(-0.5, 5,'Likes spicy food',horizontalalignment='center', verticalalignment='center', rotation=90)
ax.text(5, -0.5,'Unbothered', horizontalalignment='center', verticalalignment='center', rotation=0)

ax.text(10.5, 5,'Hates spicy food',horizontalalignment='center', verticalalignment='center', rotation=90)
ax.text(5, 10.5,'Mouth is on fire', horizontalalignment='center', verticalalignment='center', rotation=0)

# does not work
ax.annotate('', xy=(0, 5), xycoords='data', xytext=(0, 5), fontsize=16, \
            arrowprops={'arrowstyle': '-|>', 'lw': 4, 'color': 'black'}, va='center', color='black')

#plt.tight_layout()
plt.show()
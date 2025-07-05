import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import matplotlib.font_manager as fm


fig, ax = plt.subplots(figsize=(6, 2), dpi=100)
ax.axis('off')


font_properties = fm.FontProperties(weight='bold', size=13)


legend_elements = [
    mlines.Line2D([], [], color='blue', marker='o', linestyle='-', linewidth=2, markersize=8, label='iOS'),
    mlines.Line2D([], [], color='red', marker='^', linestyle='-', linewidth=2, markersize=8, label='Android'),
    mlines.Line2D([], [], color='blue', linestyle=':', linewidth=2, label='iOS Moving Average'),
    mpatches.Patch(color='blue', alpha=0.2, hatch='///', label='iOS Bollinger Bands'),
    mlines.Line2D([], [], color='red', linestyle='--', linewidth=2, label='Android Moving Average'),
    mpatches.Patch(color='red', alpha=0.2, hatch='O', label='Android Bollinger Bands'),
]


ax.legend(handles=legend_elements, loc='center', ncol=1, frameon=True, prop=font_properties)


plt.savefig("h.png", dpi=300, bbox_inches='tight')
plt.show()

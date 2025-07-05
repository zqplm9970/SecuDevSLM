import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np


file_path = './model_1.csv'
data = pd.read_csv(file_path, encoding='ISO-8859-1')


data.columns = [
    'Model', 'Some_Value_1', 'Some_Value_2', 'Some_Value_3', 'Some_Value_4',
    'IOS_Trigger', 'Android_Trigger', 'iOS', 'Android'
]


trigger_data = data[['Model', 'iOS', 'Android']]


trigger_data['iOS'] = trigger_data['iOS'].apply(lambda x: 1 if x == 'ÊÇ' else 0)
trigger_data['Android'] = trigger_data['Android'].apply(lambda x: 1 if x == 'ÊÇ' else 0)


trigger_data.set_index('Model', inplace=True)


fig, ax = plt.subplots(figsize=(15, 14))


for (i, j), val in np.ndenumerate(trigger_data.values):
    if val == 1:
        face_color = '#1f77b4'
    else:
        face_color = '#c6dbef'

    rect = plt.Rectangle([j, i], 1, 1, facecolor=face_color, edgecolor='black', linewidth=0.5)
    ax.add_patch(rect)


ax.set_xlim(0, trigger_data.shape[1])
ax.set_ylim(0, trigger_data.shape[0])

ax.set_xticks(np.arange(trigger_data.shape[1]) + 0.5)
ax.set_yticks(np.arange(trigger_data.shape[0]) + 0.5)

ax.set_xticklabels(trigger_data.columns, fontsize=20, fontweight='bold')
ax.set_yticklabels(trigger_data.index, fontsize=7, fontweight='bold')

ax.invert_yaxis()
ax.xaxis.tick_top()


ax.set_facecolor('white')


for spine in ax.spines.values():
    spine.set_visible(False)


ax.tick_params(length=0)


trigger_patch = mpatches.Patch(color='#1f77b4', label='Trigger')
no_trigger_patch = mpatches.Patch(color='#c6dbef', label='No Trigger')


box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

legend = ax.legend(handles=[trigger_patch, no_trigger_patch],
                   loc='center left',
                   bbox_to_anchor=(1, 0.5),
                   fontsize=18,
                   frameon=False)


for text in legend.get_texts():
    text.set_fontweight('bold')

plt.show()

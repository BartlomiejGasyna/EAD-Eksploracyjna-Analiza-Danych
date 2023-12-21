import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor
import numpy as np


def ex2():
    df_temp = pd.read_csv('city_temperature.csv', low_memory=False)
    df_temp = df_temp[df_temp['Year'] >= 1900]
    pivot = df_temp.pivot_table(columns='Region', index=['Year', 'Month'], aggfunc=['mean'], values='AvgTemperature')
    june        = pivot.loc[(slice(None), 6), :]
    december    = pivot.loc[(slice(None), 12), :]

    fig, axes = plt.subplots(1, 2, figsize=(16, 8))

    # June plot
    june.unstack().plot(ax=axes[0], legend=False)
    axes[0].set_title('Average Temperatures in June')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Average Temperature')
    axes[0].grid()

    # December plot
    december.unstack().plot(ax=axes[1], legend=False)
    axes[1].set_title('Average Temperatures in December')
    axes[1].set_xlabel('Year')
    axes[1].set_ylabel('Average Temperature')
    axes[1].grid()


    # Legend
    regions = pivot.columns.get_level_values(1).unique()

    handles, _ = axes[0].get_legend_handles_labels()

    common_legend = fig.legend(handles, regions, loc='lower center', ncol=len(regions))

    # Adjust the layout to make room for the common legend
    plt.subplots_adjust(bottom=0.15)  # Adjust the bottom margin to make room for the legend

    # Place the common legend underneath both subplots
    fig.subplots_adjust(bottom=0.15)
    plt.show()

def ex3():
    ecg = pd.read_csv('raw_ecg.csv', low_memory=False)
    beats = pd.read_csv('ecg_beats.csv', low_memory=False)

    beats = np.array(beats['BeatTimestamp'])
    ecg = np.array(ecg['LeadI'])


    freq = 500
    range_values = np.arange(-0.55 * freq, 0.4 * freq)

    ranges = (beats[:, np.newaxis] + range_values).astype(int)

    ranges = np.clip(ranges, 0, len(ecg)-1)

    segments = ecg[ranges]

    avg_signal = np.mean(segments, axis=0)
    timescale = (range_values) / freq

    fig, ax = plt.subplots()

    annotation_range = (-0.045, 0.35)
    annotation_text = "Q-T INTERVAL 400ms"

    # Highlight the specified range
    ax.axvspan(annotation_range[0], annotation_range[1], color='red', alpha=0.3, label='annotation_text')

    # Add the annotation text
    ax.annotate(annotation_text,
                xy=(np.mean(annotation_range), 0.5),
                xytext=(np.mean(annotation_range), 300),  # Position of the text
                fontsize=10,
                ha='center', va='center')
    
    # Add annotation to a single point
    P_amplitue_x = -0.442
    P_amplitue_y = 80
    plt.annotate(f'P: {P_amplitue_y:.2f}',
                xy=(P_amplitue_x, P_amplitue_y),
                xytext=(P_amplitue_x, P_amplitue_y + 40),  # Position of the text
                arrowprops=dict(facecolor='black', arrowstyle='->'),
                fontsize=10,
                ha='center', va='center')

    # Add annotation to a single point
    R_amplitue_x = 0.0
    R_amplitue_y = 480.9
    plt.annotate(f'R: {R_amplitue_y:.2f}',
                xy=(R_amplitue_x, R_amplitue_y),
                xytext=(R_amplitue_x, R_amplitue_y + 40),  # Position of the text
                arrowprops=dict(facecolor='black', arrowstyle='->'),
                fontsize=10,
                ha='center', va='center')

    # Add annotation to a single point
    T_amplitue_x = 0.26
    T_amplitue_y = 182
    plt.annotate(f'T: {T_amplitue_y:.2f}',
                xy=(T_amplitue_x, T_amplitue_y),
                xytext=(T_amplitue_x, T_amplitue_y + 40),  # Position of the text
                arrowprops=dict(facecolor='black', arrowstyle='->'),
                fontsize=10,
                ha='center', va='center')


    ax.plot(timescale, avg_signal)
    ax.grid()
    plt.show()

def ex4():
    titanic_df = pd.read_csv('titanic_train.csv', low_memory=False)
    titanic_df = titanic_df[['Survived', 'Pclass', 'Sex']]

    pivot = titanic_df.dropna().pivot_table(index=['Pclass', 'Sex'], values='Survived', aggfunc=['mean'])

    pivot = pivot.unstack()

    print(pivot)

    pivot.plot(kind='bar', stacked=False, title='Percentage Survival Based on Sex and Ticket Class', figsize=(11,10))

    plt.xlabel('Ticket class')
    plt.ylabel('Percentage survival')

    plt.legend(title='Sex', labels=['Female', 'Male'])
    plt.xticks(rotation=0)
    plt.show()


if __name__ == '__main__':
    ex2()
    ex3()
    ex4()
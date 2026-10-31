from pathlib import Path
from calendar import month_name, month_abbr

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()

# Parse dates and use them as the index.
df = pd.read_csv(Path(__file__).with_name('fcc-forum-pageviews.csv'),
                 parse_dates=['date'], index_col='date')

# Keep the central 95% of daily page-view counts.
lower, upper = df['value'].quantile([0.025, 0.975])
df = df.loc[df['value'].between(lower, upper)].copy()


def draw_line_plot():
    df_line = df.copy()
    fig, ax = plt.subplots(figsize=(15, 5))
    ax.plot(df_line.index, df_line['value'], color='firebrick', linewidth=1)
    ax.set(
        title='Daily freeCodeCamp Forum Page Views 5/2016-12/2019',
        xlabel='Date', ylabel='Page Views'
    )
    fig.tight_layout()

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig


def draw_bar_plot():
    df_bar = df.copy()
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month
    monthly_means = df_bar.groupby(['year', 'month'])['value'].mean().unstack('month')
    monthly_means = monthly_means.reindex(columns=range(1, 13))
    monthly_means.columns = list(month_name)[1:]

    fig, ax = plt.subplots(figsize=(12, 7))
    monthly_means.plot.bar(ax=ax, width=0.8)
    ax.set(xlabel='Years', ylabel='Average Page Views')
    ax.tick_params(axis='x', rotation=0)
    ax.legend(title='Months')
    fig.tight_layout()

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig


def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    sns.boxplot(data=df_box, x='year', y='value', hue='year',
                palette='Set2', legend=False, ax=axes[0])
    sns.boxplot(data=df_box, x='month', y='value', hue='month',
                order=list(month_abbr)[1:], hue_order=list(month_abbr)[1:],
                palette='Set3', legend=False, ax=axes[1])
    axes[0].set(title='Year-wise Box Plot (Trend)', xlabel='Year', ylabel='Page Views')
    axes[1].set(title='Month-wise Box Plot (Seasonality)', xlabel='Month', ylabel='Page Views')
    for ax in axes:
        ax.set_ylim(0, 200000)
        ax.set_yticks(range(0, 200001, 20000))
    fig.tight_layout()

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig

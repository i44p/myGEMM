import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from random import shuffle

import matplotlib.font_manager as fm

prop = fm.FontProperties(fname='JetBrainsMonoNL-Regular.ttf', size=10)
propb = fm.FontProperties(fname='proxima-nova_regular.ttf', size=16)

dim_white = '#f2f5f8'

markers = ['o', 'v', '^', '8', 's', 'P', '*', 'D']

colors = [
    '#1e22aa',
    '#cacbf5',
    '#ae2ade',
    '#1ab2fb',
    '#32e875',
    '#ffca2b',
    '#ff794c',
]
shuffle(colors)


def plot_matrices(frame, name='plot_matrices', backend='myGEMM.cl', WGS = 16, opts='-cl-std=CL1.2', log=True, opts_n=0):
    fig, ax = plt.subplots(layout='constrained', figsize=(5,5))
    ax.grid(linestyle = '--', linewidth = 0.5, which="both")
    ax.set_axisbelow(True)

    opts = frame['cl_compiler_options'].unique().tolist()[opts_n]
    frame = frame[frame['backend'] == backend]
    frame = frame[frame['cl_compiler_options'] == opts]

    ax.set_xlabel("Размер матрицы", fontproperties=prop)
    ax.set_ylabel("Затраченное время (с), медиана", fontproperties=prop)
    ax.set_title(f"{backend}, WGS={WGS}, {opts}", fontproperties=prop)
    if log:
        ax.set_yscale('log')

    unique_kernels = frame['selected_kernel'].unique().tolist()
    unique_sizes = frame['matrix_dimensions'].unique().tolist()

    fmt = [f'{marker}--' for marker in markers]

    x = sorted(unique_sizes)
    y = {}
    for kernel in unique_kernels:
        kernel_frame = frame[frame['selected_kernel'] == kernel]
        times = []
        for size in x:
            times.append(kernel_frame[kernel_frame['matrix_dimensions'] == size]['elapsed_s'].median())
        y[kernel] = times
    
    ax.set_xticks(x, x)
    for kernel in unique_kernels:
        ax.plot(x, y[kernel], fmt[kernel], label=f"Ядро {kernel}", markersize=8, color=colors[kernel-1])

    ax.legend(loc='upper left', ncols=3)

    fig.savefig(f"plot/{name}{'_log' if log else ''}.png", dpi=400)

plt.rcParams["figure.facecolor"] = "w"

def grouped_bar_kernels(frame, name='grouped_bar_kernels', backend='myGEMM.cl', WGS = 16, opts_n=0):
    fig, ax = plt.subplots(layout='constrained', figsize=(9,5))
    ax.grid(linestyle = '--', linewidth = 0.3, which="minor")
    ax.set_axisbelow(True)
    ax.set_facecolor(dim_white)
    ax.spines[['right', 'top', 'bottom', 'left']].set_visible(False)

    for label in ax.get_xticklabels():
        label.set_fontproperties(prop)
    for label in ax.get_yticklabels():
        label.set_fontproperties(prop)

    opts = frame['cl_compiler_options'].unique().tolist()[opts_n]

    frame = frame[frame['backend'] == backend]
    frame = frame[frame['cl_compiler_options'] == opts]
    frame = frame[frame['work_group_size'] == WGS]

    ax.set_xlabel("Размер матрицы", fontproperties=propb)
    ax.set_ylabel("Затраченное время (с), медиана", fontproperties=propb)
    ax.set_title(f"{'RTX 3090' if '3090' in name.lower() else 'IMG BXE-2-32'}, {backend}, WGS={WGS}, {opts}", fontproperties=propb)
    ax.set_yscale('log')
    ax.set_ylim(
        bottom=frame['elapsed_s'].min()*0.9,
        top=frame['elapsed_s'].max()*5
        )

    unique_kernels = frame['selected_kernel'].unique().tolist()
    unique_sizes = frame['matrix_dimensions'].unique().tolist()

    groups = sorted(unique_sizes)

    kernel_times = {}
    for kernel in unique_kernels:
        kernel_frame = frame[frame['selected_kernel'] == kernel]
        times = []
        stdevs = []
        for size in groups:
            d = kernel_frame[kernel_frame['matrix_dimensions'] == size]['elapsed_s']
            times.append(d.median().round(6))
            stdevs.append(d.std())
        kernel_times[kernel] = [times, stdevs]

    x = np.arange(len(groups))  # the label locations
    width = 0.12  # the width of the bars
    multiplier = -2

    for kernel, measurement in kernel_times.items():
        offset = width * multiplier
        times, stdevs = measurement
        rects = ax.bar(x + offset, times, width, label=f"Ядро {kernel}", yerr=stdevs, color=colors[kernel-1])
        ax.bar_label(rects, padding=6, rotation=90, fontproperties=prop)
        multiplier += 1

    ax.set_xticks(x + width, groups)
    ax.legend(loc='upper left', ncols=3, prop=prop)

    fig.savefig(f"plot/{name}.png", dpi=400)

def plot_comp(frame, name='', WGS = 16, opts_n=0, k=4):
    fig, ax = plt.subplots(layout='constrained', figsize=(6,5))
    ax.grid(linestyle = '--', linewidth = 0.3, which="minor")
    ax.set_axisbelow(True)
    ax.set_facecolor(dim_white)
    ax.spines[['right', 'top', 'bottom', 'left']].set_visible(False)

    for label in ax.get_xticklabels():
        label.set_fontproperties(prop)
    for label in ax.get_yticklabels():
        label.set_fontproperties(prop)

    opts = frame['cl_compiler_options'].unique().tolist()[opts_n]

    frame = frame[frame['cl_compiler_options'] == opts]
    frame = frame[frame['selected_kernel'] == k]
    frame = frame[frame['work_group_size'] == WGS]
    frame = frame[frame['src'] != 'None']

    ax.set_xlabel("Размер матрицы", fontproperties=propb)
    ax.set_ylabel("Затраченное время (с), медиана", fontproperties=propb)
    ax.set_title(f"Ядро {k}, {WGS=}, {opts}", fontproperties=propb)
    ax.set_yscale('log')
    ax.set_ylim(
        bottom=frame['elapsed_s'].min()*0.9,
        top=frame['elapsed_s'].max()*10
        )

    unique_kernels = frame['src'].unique().tolist()
    unique_sizes = frame['matrix_dimensions'].unique().tolist()

    groups = sorted(unique_sizes)

    kernel_times = {}
    for kernel in unique_kernels:
        kernel_frame = frame[frame['src'] == kernel]
        times = []
        stdevs = []
        for size in groups:
            d = kernel_frame[kernel_frame['matrix_dimensions'] == size]['elapsed_s']
            times.append(d.median())
            stdevs.append(d.std())
        kernel_times[kernel] = [times, stdevs]

    x = np.arange(len(groups))  # the label locations
    width = 0.19  # the width of the bars
    multiplier = -0.5

    for kernel, measurement in kernel_times.items():
        offset = width * multiplier
        times, stdevs = measurement
        rects = ax.bar(x + offset, times, width, label=f"{kernel}", yerr=stdevs, color=colors[unique_kernels.index(kernel)])
        ax.bar_label(rects, padding=6, rotation=90, fontproperties=prop)
        multiplier += 1

    ax.set_xticks(x + width, groups)
    ax.legend(loc='upper left', ncols=2, prop=prop)

    fig.savefig(f"plot/{name}.png", dpi=400)

def boxplot_kernels(frame, name='boxplot_kernels', backend='myGEMM.cl', WGS = 16, SIZE=2048, opts_n=0):
    fig, ax = plt.subplots(layout='constrained', figsize=(5,5))
    fig.set_facecolor(dim_white)
    ax.set_facecolor(dim_white)
    ax.grid(linestyle = '--', linewidth = 0.5, which="both")
    ax.set_axisbelow(True)
    
    opts = frame['cl_compiler_options'].unique().tolist()[opts_n]

    frame = frame[frame['cl_compiler_options'] == opts]
    frame = frame[frame['backend'] == backend]
    frame = frame[frame['matrix_dimensions'] == SIZE]

    ax.set_xlabel("Ядро", fontproperties=propb)
    ax.set_ylabel("Затраченное время (с)", fontproperties=propb)
    ax.set_title(f"{backend}, WGS={WGS}, SIZE={SIZE}, {opts}", fontproperties=propb)
    ax.set_yscale('log')
    ax.set_ylim(
        bottom=frame['elapsed_s'].min()*0.9,
        top=frame['elapsed_s'].max()*1.1
    )

    unique_kernels = frame['selected_kernel'].unique().tolist()

    times = []
    kernels = []

    for kernel in sorted(unique_kernels):
        kernels.append(kernel)
        times.append(frame[frame['selected_kernel'] == kernel]['elapsed_s'])

    #bplot = ax.boxplot(times, tick_labels=kernels, showfliers=False)
    parts = ax.violinplot(times, showmedians=True, widths=0.9)
    parts['cmedians'].set_colors(colors[2])

    # ax.legend()

    fig.savefig(f"plot/{name}.png", dpi=400)

def read_file(fn):
    data = pd.read_csv(fn)
    data.columns = "backend,selected_kernel,work_group_size,cl_compiler_options,matrix_dimensions,elapsed_s".split(',')

    for col in data.columns:
        if pd.api.types.is_string_dtype(data[col]):
            data[col] = data[col].str.strip()
    return data

data1 = read_file("data/img_data.csv")
data1 = data1[data1['backend'] != 'clBlas']

grouped_bar_kernels(data1)
# boxplot_kernels(data1)
# plot_matrices(data1, log=False)

data2 = read_file("data/cuda_data.csv")
data2 = data2[data2['backend'] != 'clBlas']

grouped_bar_kernels(data2, name="grouped_bar_kernels_3090")
grouped_bar_kernels(data2, name="grouped_bar_kernels_3090_cuda", backend='myGEMM.cu')

data1['src'] = 'IMG BXE-2-32'
data2['src'] = [
    '3090 OpenCL' if x == 'myGEMM.cl' else
    '3090 CUDA' if x == 'myGEMM.cu' else
    '3090 cuBLAS' if x == 'cuBLAS' else
    'None'
    for x in data2['backend']]

plot_comp(
    pd.concat([data1, data2], ignore_index=True),
    name='comp',
)

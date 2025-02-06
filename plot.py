import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


data = pd.read_csv("pwr_data.csv")
data.columns = "backend,selected_kernel,work_group_size,cl_compiler_options,matrix_dimensions,elapsed_s".split(',')

for col in data.columns:
    if pd.api.types.is_string_dtype(data[col]):
        data[col] = data[col].str.strip()


def plot_matrices(frame, backend='myGEMM.cl', WGS = 16, opts='-cl-std=CL1.2', log=True):
    fig, ax = plt.subplots(layout='constrained', figsize=(9,5))

    frame = frame[frame['backend'] == backend]
    frame = frame[frame['cl_compiler_options'] == opts]

    ax.set_xlabel("Matrix size")
    ax.set_ylabel("Time spent (s), median")
    ax.set_title(f"{backend}, WGS={WGS}, {opts}")
    if log:
        ax.set_yscale('log')

    unique_kernels = frame['selected_kernel'].unique().tolist()
    unique_sizes = frame['matrix_dimensions'].unique().tolist()

    fmt = [f'{marker}--' for marker in ['o', 'v', '^', '8', 's', 'P', '*', 'D']]

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
        ax.plot(x, y[kernel], fmt[kernel], label=f"kernel={kernel}", markersize=8)

    ax.legend(loc='upper left', ncols=3)

    fig.savefig(f"plot/plot_matrices{'_log' if log else ''}.png", dpi=300)


def grouped_bar_kernels(frame, backend='myGEMM.cl', WGS = 16, opts='-cl-std=CL1.2'):
    fig, ax = plt.subplots(layout='constrained', figsize=(13,5))

    frame = frame[frame['backend'] == backend]
    frame = frame[frame['cl_compiler_options'] == opts]

    ax.set_xlabel("Matrix size")
    ax.set_ylabel("Time spent (s), median")
    ax.set_title(f"{backend}, WGS={WGS}, {opts}")
    ax.set_yscale('log')
    ax.set_ylim(bottom=10e-3, top=10e+2)

    unique_kernels = frame['selected_kernel'].unique().tolist()
    unique_sizes = frame['matrix_dimensions'].unique().tolist()

    groups = sorted(unique_sizes)

    kernel_times = {}
    for kernel in unique_kernels:
        kernel_frame = frame[frame['selected_kernel'] == kernel]
        times = []
        for size in groups:
            times.append(kernel_frame[kernel_frame['matrix_dimensions'] == size]['elapsed_s'].median())
        kernel_times[kernel] = times

    x = np.arange(len(groups))  # the label locations
    width = 0.13  # the width of the bars
    multiplier = 0

    for kernel, measurement in kernel_times.items():
        offset = width * multiplier
        rects = ax.bar(x + offset, measurement, width, label=f"kernel={kernel}")
        ax.bar_label(rects, padding=3, rotation=90)
        multiplier += 1

    ax.set_xticks(x + width, groups)
    ax.legend(loc='upper left', ncols=3)

    fig.savefig("plot/grouped_bar_kernels.png", dpi=300)

def boxplot_kernels(frame, backend='myGEMM.cl', WGS = 16, SIZE=2048):
    fig, ax = plt.subplots(layout='constrained')

    ax.set_xlabel("kernel")
    ax.set_ylabel("Time spent (s)")
    ax.set_title(f"{backend}, WGS={WGS}, SIZE={SIZE}")

    frame = frame[frame['backend'] == backend]
    frame = frame[frame['matrix_dimensions'] == SIZE]

    unique_kernels = frame['selected_kernel'].unique().tolist()

    times = []
    kernels = []

    for kernel in sorted(unique_kernels):
        kernels.append(kernel)
        times.append(frame[frame['selected_kernel'] == kernel]['elapsed_s'])

    bplot = ax.boxplot(times, tick_labels=kernels, showfliers=False)

    # ax.legend()

    fig.savefig("plot/boxplot_kernels.png", dpi=400)

grouped_bar_kernels(data)
boxplot_kernels(data)
plot_matrices(data)
plot_matrices(data, log=False)
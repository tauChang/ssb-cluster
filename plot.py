import datetime
import matplotlib.pyplot as plt
import random 
import argparse

def plot_node(file_path, node, colors, start_time, end_time, min_data, max_data, ax):
    with open(file_path, 'r') as f:
        data = f.readlines()

    # Initialize dictionaries to store the data
    sent_data = {}
    received_data = {}

    # Parse the data
    for line in data:
        parts = line.split(' ')
        try: 
            time_str, src, dst, amount = parts[0], parts[1], parts[2], int(parts[3])
            time = datetime.datetime.strptime(time_str, '%H:%M:%S.%f')
        except:
            continue

        if src != node:
            continue

        # Convert the time string to a datetime object

        # Add the amount of data to the appropriate dictionary
        if src not in sent_data:
            sent_data[src] = {}
        if dst not in sent_data[src]:
            sent_data[src][dst] = []
        sent_data[src][dst].append((time, amount))

        if dst not in received_data:
            received_data[dst] = {}
        if src not in received_data[dst]:
            received_data[dst][src] = []
        received_data[dst][src].append((time, amount))


    # Plot the data
    for src in sent_data:
        for dst in sent_data[src]:
            times = [data[0] for data in sent_data[src][dst]]
            amounts = [data[1] for data in sent_data[src][dst]]
            
            ax.plot(times, amounts, label=dst, color=colors[dst])

    # Set the x-limits to be the start and end times of the shared time axis
    ax.set_xlim(start_time, end_time)

    ax.set_xlabel(node)
    # y range
    ax.set_ylim(min_data, max_data)

def find_axis_range(file_paths, nodes):
    start_time = datetime.datetime.max
    end_time = datetime.datetime.min
    max_data = 0
    for file_path in file_paths:
        with open(file_path, 'r') as f:
            data = f.readlines()
        for line in data:
            parts = line.split(' ')
            if len(parts[0]) == 0:
                continue
            time_str = parts[0]
            try:
                time = datetime.datetime.strptime(time_str, '%H:%M:%S.%f')
            except:
                continue
            if time < start_time:
                start_time = time
            if time > end_time:
                end_time = time
            max_data = max(max_data, int(parts[3]))
    return start_time, end_time, 0, max_data
    

def main():
    # take input from user to see what the file path is

    parser = argparse.ArgumentParser(description='Plot data transmission logs for multiple nodes.')
    parser.add_argument('-d', '--dir', type=str, help='Directory containing the log files', required=True)
    parser.add_argument('-o', '--output', type=str, help='Output file name')
    args = parser.parse_args()

    dir_path = args.dir
    output_path = args.output
    
    # Open the log file
    nodes = [f"node{i}" for i in range(0, 8)]
    # assign random color
    colors = {}
    for node in nodes:
        colors[node] = f"#{random.randint(0, 0xFFFFFF):06x}"

    start_time, end_time, min_data, max_data = find_axis_range([f"{dir_path}/log_{node}" for node in nodes], nodes)
    max_data += 1000

    fig, axs = plt.subplots(len(nodes), 1, sharex=True, sharey=False, figsize=(10, 8))

    # Plot each node's data with
    for i, node in enumerate(nodes):
        file_path = f"{dir_path}/log_{node}"
        plot_node(file_path, node, colors, start_time, end_time, min_data, max_data, axs[i])

    # add a legend with all nodes and their corresponding colors
    handles = [plt.Rectangle((0,0),1,1, color=colors[label]) for label in colors]
    # posi
    legend = plt.legend(handles, colors.keys(), loc='center', bbox_to_anchor=(0.8, -0.8), ncol=4, fancybox=True)
    legend.get_frame().set_alpha(0.5)    

    # adjust subplot spacing and save the final plot
    fig.subplots_adjust(hspace=0.5)
    plt.savefig(output_path)
    plt.close()

if __name__ == '__main__':
    main()
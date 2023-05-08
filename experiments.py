import time
import threading
import sys

def hop_expirement(users):
    def issueWantsBlob(node, blob_id, elapsed_time):
        start_time = time.time()
        users[node].wantsBlob(blob_id)
        end_time = time.time()
        elapsed_time[node].append(end_time - start_time)
    
    def issueHasBlob(node, blob_id, elapsed_time):
        start_time = time.time()
        # loop until node has blob
        sleep_interval = 0.1
        while not users[node].hasBlob(blob_id):
            time.sleep(sleep_interval)
            # sleep_interval = min(sleep_interval+1, 0.5)
        print(f"{node} has blob")
        end_time = time.time()
        elapsed_time[node].append(end_time - start_time)
    
    users["node-1"].follow(users["node-0"])
    users["node-2"].follow(users["node-0"])
    users["node-3"].follow(users["node-0"])
    users["node-4"].follow(users["node-0"])
    users["node-5"].follow(users["node-0"])

    elapsed_time = {}
    recipients = users.keys() - ["node-0"]
    for node in recipients:
        elapsed_time[node] = []

    for i in range(5):
        print("round: ", i)
        fname = f"file{i}"
        blob_id = users["node-0"].addBlob(fname, 1000000) # max 5 mb
        users["node-0"].pushBlob(blob_id)

        # issue wantsBlob for all nodes in parallel threads
        threads = []
        for node in recipients:
            # thread = threading.Thread(target=issueWantsBlob, args=(node, blob_ids, elapsed_time))
            thread = threading.Thread(target=issueWantsBlob, args=(node, blob_id, elapsed_time))
            threads.append(thread)

        for thread in threads:
            thread.start()
        
        for thread in threads:
            thread.join()
    
    # selected_index = []
    # # pick the 5 indices with smallest time for node-3
    # for i in range(5):
    #     min_time = sys.maxsize
    #     min_index = -1
    #     for index, t in enumerate(elapsed_time["node-1"]):
    #         if t < min_time and index not in selected_index:
    #             min_time = t
    #             min_index = index
    #     selected_index.append(min_index)
    
    # print(selected_index)
    
    for node in recipients:
        # elapsed_time[node] = [elapsed_time[node][i] for i in selected_index]
        print(f"Average time for {node} to receive blob: {sum(elapsed_time[node])/len(elapsed_time[node])}")

    for node in recipients:
        print(f"{node}: ", [round(x, 2) for x in elapsed_time[node]])

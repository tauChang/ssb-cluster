import time
import threading
import sys

def hop_expirement(users):
    def issueWantsBlob(node, blob_id, elapsed_time):
        start_time = time.time()
        users[node].wantsBlob(blob_id)
        end_time = time.time()
        elapsed_time[node].append(end_time - start_time)
    
    publisher = "node0"
    recipients = users.keys() - [publisher]

    for node in recipients:
        users[node].follow(users[publisher])

    elapsed_time = {}
    for node in recipients:
        elapsed_time[node] = []

    for i in range(1):
        print("round: ", i)
        fname = f"file{i}"
        blob_id = users[publisher].addBlob(fname, 1000000) # max 5 mb
        users[publisher].pushBlob(blob_id)

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
    
    for node in recipients:
        # elapsed_time[node] = [elapsed_time[node][i] for i in selected_index]
        print(f"Average time for {node} to receive blob: {sum(elapsed_time[node])/len(elapsed_time[node])}")

    for node in recipients:
        print(f"{node}: ", [round(x, 2) for x in elapsed_time[node]])

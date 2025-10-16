from collections import Counter
import heapq

def least_interval(tasks, n):
    """
    Returns the least interval required to finish all the tasks with a cooldown time of n units.
    
    :param tasks: List of characters representing tasks
    :param n: Integer, cooldown period between same tasks
    :return: Integer, minimum time required to complete all tasks
    """
    task_counts = Counter(tasks)
    max_heap = [-count for count in task_counts.values()]
    heapq.heapify(max_heap)
    
    time = 0
    while max_heap:
        i, temp = 0, []
        while i <= n:
            if max_heap:
                count = heapq.heappop(max_heap)
                if count < -1:
                    temp.append(count + 1)
            time += 1
            if not max_heap and not temp:
                break
            i += 1
        
        for item in temp:
            heapq.heappush(max_heap, item)
    
    return time
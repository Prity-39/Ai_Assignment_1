import osmnx as ox
import random
import networkx as nx
import heapq
import time
from tabulate import tabulate
import matplotlib.pyplot as plt



list1 = []
list2 = []
list3 = []
risk_values = []
risk_iterator = 0
node_pairs = []
risk_values = []

def hstd(node1, node2):
    global risk_iterator  
    hstd_value = ox.distance.euclidean_dist_vec(graph.nodes[node1]['y'], graph.nodes[node1]['x'],
                                                 graph.nodes[node2]['y'], graph.nodes[node2]['x'])
    


    try:
        # Get the index of node1 and node2 from the node_pairs list
        index = node_pairs.index((node1, node2))
        risk_value = risk_values[index]
    except ValueError:  # Handle the case when the index is not found
        risk_value = 100000
    # index = node_pairs.index((node1, node2))
    
    # Find the risk value corresponding to the index
    # risk_value = risk_values[index]

   
    
    #print(node1)
    #risk_value = random.uniform(0, 500)
    
    retValue = hstd_value + risk_value
    #print(retValue)
    # # Append the risk value to a file
    # with open("risk.txt", "a") as f:
    #     f.write(str(risk_value) + "\n")
    
    
    # risk_value = risk_values[risk_iterator]
    
    # # Increment the risk iterator and loop back to the beginning if necessary
    # risk_iterator = (risk_iterator + 1) % len(risk_values)
    return retValue

def dijkstra(graph, start_node):
    dist = {node: float('inf') for node in graph.nodes}
    dist[start_node] = 0
    predecessors = {}
    pq = [(0, start_node)]
    while pq:
        current_dist, current_node = heapq.heappop(pq)
        if current_dist > dist[current_node]:
            continue
        for neighbor, edge in graph[current_node].items():
            weight = edge.get('weight', 1)
            new_dist = dist[current_node] + weight
            if new_dist < dist[neighbor]:
                dist[neighbor] = new_dist
                predecessors[neighbor] = current_node
                heapq.heappush(pq, (new_dist, neighbor))
    return dist, predecessors

def evaluation_function(node, target_node, actual_cost, heuristic, weight):
    return actual_cost[node] + weight * heuristic(node, target_node)

def greedy_best_first_search(graph, start_node, target_node, heuristic):
    visited = set()
    pq = [(heuristic(start_node, target_node), start_node)]
    while pq:
        _, current_node = heapq.heappop(pq)
        list1.append(current_node)
        if current_node == target_node:
            return visited
        visited.add(current_node)
        for neighbor in graph[current_node]:
            if neighbor not in visited:
                heapq.heappush(pq, (heuristic(neighbor, target_node), neighbor))
                list1.append(neighbor)
    return visited

def a_star(graph, start_node, target_node, actual_cost, heuristic):
    visited = set()
    pq = [(evaluation_function(start_node, target_node, actual_cost, heuristic, 1), start_node)]
    while pq:
        _, current_node = heapq.heappop(pq)
        list2.append(current_node) 
        if current_node == target_node:
            return visited
        visited.add(current_node)
        for neighbor in graph[current_node]:
            if neighbor not in visited:
                heapq.heappush(pq, (evaluation_function(neighbor, target_node, actual_cost, heuristic, 1), neighbor))
    return visited

def weighted_a_star(graph, start_node, target_node, actual_cost, heuristic, weight):
    visited = set()
    pq = [(evaluation_function(start_node, target_node, actual_cost, heuristic, weight), start_node)]
    while pq:
        _, current_node = heapq.heappop(pq)
        list3.append(current_node) 
        if current_node == target_node:
            return visited
        visited.add(current_node)
        for neighbor in graph[current_node]:
            if neighbor not in visited:
                heapq.heappush(pq, (evaluation_function(neighbor, target_node, actual_cost, heuristic, weight), neighbor))
    return visited

city_name = "Lake Placid, New York"
graph = ox.graph_from_place(city_name, network_type='all')





# Open the file in read mode
#with open("risk.txt", "r") as f:
    # Iterate over each line in the file
    #for line in f:
        # Convert the line to a float and append it to the list
        #risk_values.append(float(line.strip()))

# Print the list of risk values


if graph is not None:
    nodes = graph.nodes
    edges = graph.edges
    all_nodes = list(graph.nodes)
    


    # with open("nodes.txt", "w") as f:
    #     # Iterate over the nodes and write their IDs to the file
    #     for node in nodes:
    #         f.write(str(node) + "\n")

    desired_edge_index = 0
    
    # Iterate over the edges and find the edge with the desired index
    # for u, v, data in edges(data=True):
    #     if u == desired_edge_index or v == desired_edge_index:
    #         print("Edge data:", data)
    #         break


    print(len(edges))
    # with open("u_values.txt", "w") as f:  
    #  for u, v, data in edges(data=True):
    #     risk_value = random.uniform(0, 500)
    #     f.write(f"{u} {v} {risk_value}\n")
    #    # print(f"Edge: {u} -> {v}, Nodes: {u}, {v}")
        
         
# Open the file in read mode
    with open("riskValues.txt", "r") as f:
        # Iterate over each line in the file
        for line in f:
            # Split the line into three values: node1, node2, and risk value
            node1, node2, risk = line.split()
            node_pairs.append((int(node1), int(node2)))
            # Convert the risk value to float and append it to the list
            risk_values.append(float(risk))

    # Print the list of risk values
#     print("Risk values length:", len(risk_values))
#     print(risk_values)
# # Print the length of the node pairs list
#     print("Node pairs length:", len(node_pairs))
#     //print(node_pairs)
            

    # start_node = 8922966682
    # target_node = 8922966471



    start_node = random.choice(all_nodes)
    target_node = random.choice(all_nodes)
    start_time = time.time()
    actual_cost, _ = dijkstra(graph, start_node)
    dijkstra_time = time.time() - start_time

    start_time = time.time()
    gbfs_visited = greedy_best_first_search(graph, start_node, target_node, hstd)
    gbfs_time = time.time() - start_time

    start_time = time.time()
    a_star_visited = a_star(graph, start_node, target_node, actual_cost, hstd)
    a_star_time = time.time() - start_time

    start_time = time.time()
    weight = 4
    weighted_a_star_visited = weighted_a_star(graph, start_node, target_node, actual_cost, hstd, weight)
    weighted_a_star_time = time.time() - start_time

    # print("Start Node:", start_node)
    # print("Target Node:", target_node)

    gbfs_time_ms = gbfs_time * 1000
    a_star_time_ms = a_star_time * 1000
    weighted_a_star_time_ms = weighted_a_star_time * 1000

    results = [
        ("Greedy Best First Search", len(gbfs_visited)*8, gbfs_time_ms, len(gbfs_visited)),
        ("A*", len(a_star_visited)*8, a_star_time_ms, len(a_star_visited)),
        ("Weighted A*", len(weighted_a_star_visited)*100, weighted_a_star_time_ms, len(weighted_a_star_visited))
    ]

    # print("Size of List 1:", len(list1))
    # print("Size of List 2:", len(list2))
    # print("Size of List 3:", len(list3))


    print(tabulate(results, headers=["Algorithm", "Memory (Bytes)", "Time (ms)", "Search Space"], tablefmt="grid"))






    ox.plot_graph(ox.project_graph(graph), bgcolor='white', node_size=5, node_color='black', edge_color='#B2BEB5')
    ox.plot_graph(graph.subgraph(list1), node_size=10, node_color='green', edge_linewidth=0.5, edge_color='green')
    ox.plot_graph(graph.subgraph(list2), node_size=10, node_color='blue', edge_linewidth=0.5, edge_color='blue')
    ox.plot_graph(graph.subgraph(list3), node_size=10, node_color='red', edge_linewidth=0.5, edge_color='red')





   
else:
    print("Error: Failed to retrieve the graph data.")




   

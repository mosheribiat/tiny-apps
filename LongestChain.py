# Given the input, return length of the longest chain where the last name in a tuple matches the first name.

from typing import Dict, List, Optional, Tuple
input = [("Bob","Ross"),("Ross","Alice"),("Alice","Mark"),("Mark","Jim"), ("Mark","Cathy"),("Cathy","Daisy")]

def longest_chain(input: List[Tuple]) -> int:
    graph: Dict[str, List[str]] = {}
    for frm, to in input:
        if frm not in graph:
            graph[frm] = []
        graph[frm].append(to)

    memo: Dict[str, int] = {}
    def dfs(node: str) -> int:
        if node in memo:
            return memo[node]
        max_length = 0
        for neighbor in graph.get(node, []):
            length = 1 + dfs(neighbor)
            max_length = max(max_length, length)
        memo[node] = max_length
        return max_length

    max_chain = 0
    for person in graph:
        max_chain = max(max_chain, dfs(person))

    return max_chain


print(longest_chain(input))  # Output: 6

from collections import defaultdict
gr = defaultdict(list)
def dfs(node: str):
    children = gr.get(node, [])
    max_dep = 0
    for child in children:
        max_dep = max(max_dep, dfs(child) + 1)
        
    return max_dep
    

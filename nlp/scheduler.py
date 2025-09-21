from collections import defaultdict
import pulp

def topo_sort(nodes):
    visited = {}
    order = []
    def dfs(nid):
        if nid in visited:
            if visited[nid]==1:
                raise Exception("Cycle detected")
            return
        visited[nid]=1
        for p in nodes[nid].get("prerequisites",[]):
            dfs(p)
        visited[nid]=2
        order.append(nid)
    for nid in nodes:
        if nid not in visited:
            dfs(nid)
    return order[::-1]

def greedy_pack(nodes, total_weeks=12, hours_per_week=8):
    weeks = [{"topics": [], "remaining": hours_per_week} for _ in range(total_weeks)]
    order = topo_sort(nodes)
    for nid in order:
        est = nodes[nid].get("est_hours", 1)
        placed = False
        for w in weeks:
            if w["remaining"] + 1e-9 >= est:
                w["topics"].append(nid)
                w["remaining"] -= est
                placed = True
                break
        if not placed:
            weeks[-1]["topics"].append(nid)
            weeks[-1]["remaining"] -= est
    return weeks

def ilp_schedule(nodes, total_weeks=12, hours_per_week=8):
    topic_ids = list(nodes.keys())
    weeks = list(range(1, total_weeks+1))
    prob = pulp.LpProblem("schedule", pulp.LpMinimize)
    x = pulp.LpVariable.dicts("x", (topic_ids, weeks), lowBound=0, upBound=1, cat="Binary")
    for t in topic_ids:
        prob += pulp.lpSum([x[t][w] for w in weeks]) == 1
    for w in weeks:
        prob += pulp.lpSum([nodes[t].get("est_hours",1) * x[t][w] for t in topic_ids]) <= hours_per_week
    for t in topic_ids:
        for p in nodes[t].get("prerequisites",[]):
            for w in weeks:
                prob += pulp.lpSum([x[p][i] for i in weeks if i <= w]) >= x[t][w]
    avg_load = sum(nodes[t].get("est_hours",1) for t in topic_ids) / total_weeks
    slacks = pulp.LpVariable.dicts("slack", weeks, lowBound=0)
    for w in weeks:
        prob += pulp.lpSum([nodes[t].get("est_hours",1) * x[t][w] for t in topic_ids]) - avg_load <= slacks[w]
        prob += avg_load - pulp.lpSum([nodes[t].get("est_hours",1) * x[t][w] for t in topic_ids]) <= slacks[w]
    prob += pulp.lpSum([slacks[w] for w in weeks])
    prob.solve(pulp.PULP_CBC_CMD(msg=False))
    schedule = {w: [] for w in weeks}
    for t in topic_ids:
        for w in weeks:
            if pulp.value(x[t][w]) > 0.5:
                schedule[w].append(t)
    return schedule

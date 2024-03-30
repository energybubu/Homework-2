import copy
liquidity = {
    ("tokenA", "tokenB"): (17, 10),
    ("tokenA", "tokenC"): (11, 7),
    ("tokenA", "tokenD"): (15, 9),
    ("tokenA", "tokenE"): (21, 5),
    ("tokenB", "tokenC"): (36, 4),
    ("tokenB", "tokenD"): (13, 6),
    ("tokenB", "tokenE"): (25, 3),
    ("tokenC", "tokenD"): (30, 12),
    ("tokenC", "tokenE"): (10, 8),
    ("tokenD", "tokenE"): (60, 25),
}
def get_amount_out(amount_in, reserve_in, reserve_out):
    amount_in_with_fee = amount_in * 997
    numerator = amount_in_with_fee * reserve_out
    denominator = reserve_in * 1000 + amount_in_with_fee
    amount_out = numerator / denominator
    return amount_out
def get_dst_token_amnt(src_token, dst_token, amnt_of_src_token):
    sorted_pair = sorted([src_token, dst_token])
    pair = liquidity[tuple(sorted_pair)]
    if src_token < dst_token:
        src_reserved = pair[0]
        dst_reserved = pair[1]
    else:
        src_reserved = pair[1]
        dst_reserved = pair[0]
    out = get_amount_out(amnt_of_src_token, src_reserved, dst_reserved)

    return out

def dfs(initial_token, initial_amnt, options, explored, path_so_far, target_amnt):
    if initial_amnt == 0:
        return 0
    if initial_token == 'tokenB' and initial_amnt >= target_amnt:
        return path_so_far, initial_amnt
    for token in options:
        if token in explored or token == initial_token:
            continue
        received = get_dst_token_amnt(initial_token, token, initial_amnt)
        next_options = [x for x in options if x!=token]
        next_explored = explored.copy()
        next_explored.append(token)
        ret = dfs(token, received, next_options, next_explored, path_so_far+'->'+token, target_amnt)
        if ret!=0:
            return ret
    return 0

def get_final_amnt(path, initial_amnt):
    path = path.split()
    for i in range(len(path)):
        if i == len(path)-1:
            break
        before = copy.copy(initial_amnt)
        initial_amnt = get_dst_token_amnt(path[i], path[i+1], initial_amnt)
        print(f'{before:.4f}', path[i], ' -> ', f'{initial_amnt:.4f}', path[i+1])
    return initial_amnt

def arbitrage(target_amnt):
    options = ['tokenA', 'tokenB', 'tokenC', 'tokenD', 'tokenE']
    ret = dfs('tokenB', 5, options, [], 'tokenB', target_amnt)
    print(f"path: {ret[0]}, tokenB balance={ret[1]}.")
    return ret
get_final_amnt('tokenB tokenA tokenD tokenC tokenB', 5)
    
# arbitrage(20)
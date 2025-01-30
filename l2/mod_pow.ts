function mod_pow(b: bigint, e: bigint, m: bigint): bigint {
    if (m == 1n) {
        return 0n;
    }
    var result: bigint = 1n;
    var base: bigint = mod(b, m);
    for (let exp: bigint = e; exp > 0n; exp = exp / 2n) {
        var bit = mod(exp, 2n) 
        if (bit == 1n) {
            result = result * base
            result = mod(result, m);
        }
        base = base * base
        base = mod(base, m);
    }
    return result;
}

function mod(n: bigint, m: bigint): bigint {
  return n - n / m * m;
}

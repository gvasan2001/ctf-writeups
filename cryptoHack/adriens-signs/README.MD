# CryptoHack: Adrien's Signs (Legendre Symbol Attack)

**Writeup by Gokulavasan**

## Challenge

Adrien has found a way to encrypt his messages using symbols and minus signs. The task is to recover the flag from the given ciphertext.

## Given Code

```python
from random import randint

a = 288260533169915
p = 1007621497415251

FLAG = b'crypto{????????????????????}'


def encrypt_flag(flag):
    ciphertext = []
    plaintext = ''.join([bin(i)[2:].zfill(8) for i in flag])
    for b in plaintext:
        e = randint(1, p)
        n = pow(a, e, p)
        if b == '1':
            ciphertext.append(n)
        else:
            n = -n % p
            ciphertext.append(n)
    return ciphertext


print(encrypt_flag(FLAG))
```

## Background

**QR** means **Quadratic Residue**. A number `x` is a QR modulo `p` if it is a perfect square modulo `p`, that is, there is some `y` such that `y^2 ≡ x (mod p)`. If no such `y` exists, `x` is a **non-residue** (non-QR).

Useful rules:

- QR × QR = QR
- QR × non-QR = non-QR

## Analysis

1. The script converts the flag into a binary string, 8 bits per character.
2. For each bit, it picks a random exponent `e` and computes `n = a^e mod p`.
3. Here `p` is prime and `a` is a quadratic residue. A power of a QR is always a QR, so `n` is **always a QR**, no matter which `e` is chosen. The random number does not hide anything.
4. If the bit is `1`, the script outputs `n`, which is a QR.
5. If the bit is `0`, the script outputs `-n mod p`. This is `(-1) × n`.
6. Here `p ≡ 3 (mod 4)`, so `-1` is a **non-QR**. Therefore `(-1) × n` is (non-QR × QR) = **non-QR**.

So every ciphertext value leaks its bit:

| Bit | Ciphertext | Type |
|-----|-----------|------|
| 1 | `n` | QR |
| 0 | `-n mod p` | non-QR |

> Note: if `p ≡ 1 (mod 4)`, then `-1` would be a QR and this attack would not work.

## Attack

The Legendre symbol (Euler's criterion) tells us whether a number is a QR:

```
c^((p-1)/2) mod p = 1       if c is a QR
c^((p-1)/2) mod p = p - 1   if c is a non-QR  (p - 1 is -1 mod p)
```

Steps:

1. Loop over every ciphertext value `c`.
2. Compute `pow(c, (p-1)//2, p)`.
3. If the result is `1`, the bit is `1`. Otherwise the bit is `0`.
4. Join all bits into one binary string.
5. Convert the binary string to bytes to get the flag.

## Solve Script

See [`solve.py`](solve.py).

Flag: `crypto{...}`

## Lesson

The Legendre symbol can be computed by anyone when the modulus is a prime, and it needs no discrete log. Hiding a bit as "QR or non-QR" modulo a prime is therefore not secure. Real schemes like Goldwasser-Micali use a composite modulus `n = p·q` with a secret factorization, so only the key owner can tell QR from non-QR.

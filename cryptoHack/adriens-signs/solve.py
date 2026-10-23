ciphertext = [...]  # paste the ciphertext from the challenge here
p = 1007621497415251

binary_str = ""
for c in ciphertext:
    if pow(c, (p - 1) // 2, p) == 1:
        binary_str += "1"
    else:
        binary_str += "0"

flag = int(binary_str, 2).to_bytes((len(binary_str) + 7) // 8, "big").decode("utf-8")
print(flag)

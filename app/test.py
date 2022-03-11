#%%

a = {
    'a': 1,
    'b': 2,
    'c': 3
}

b = {
    'c': 6
}

for key, value in a.items():
    if key in b:
        a[key] = b[key]

print(a)


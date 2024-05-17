import hashlib

hasher = hashlib.sha3_256()

input_data = bytes("hello world", 'utf-8')
hasher.update(input_data)
result = hasher.hexdigest()
print("Hashed output:", result)

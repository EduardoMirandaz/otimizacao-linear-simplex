s = input().split()
while s: print(s.pop(),end=''); print(' ' if len(s) > 0 else '', end='')
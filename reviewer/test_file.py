import os

password = "admin123"  # hardcoded secret - should get flagged

def divide(a, b):
    return a / b  # no zero-check - should get flagged

def loop_test(n):
    for i in range(n+1):  # off-by-one - might get flagged
        print(i)
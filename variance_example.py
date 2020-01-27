import statistics


L1 = [1,0,5,4,0]
L2 = [0,0,0,0,2]
L3 = [4,4,4,4,4]

# Prints variance of the sample set

# Function will automatically calculate
# it's mean and set it as xbar
print("List L1 is ", L1)
print("Variance of L1 is ", statistics.variance(L1))
print("List L2 is ", L2)
print("Variance of L2 is ", statistics.variance(L2))
print("List L3 is ", L3)
print("Variance of L3 is ", statistics.variance(L3))

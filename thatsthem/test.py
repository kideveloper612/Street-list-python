print("# Create new threads")
for i in range(500):
    print("thread{} = myThread({})".format(i+1, i+1, i, i))
print("# Start new Threads")
for i in range(500):
    print("thread{}.start()".format(i+1))

print("# Add threads to thread list")
for i in range(500):
    print("threads.append(thread{})".format(i+1))


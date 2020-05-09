print("# Create new threads")
for i in range(5000):
    print("thread{} = myThread({}, thread_number_list[{}])".format(i+1, i+1, i))
print("# Start new Threads")
for i in range(5000):
    print("thread{}.start()".format(i+1))

print("# Add threads to thread list")
for i in range(5000):
    print("threads.append(thread{})".format(i+1))


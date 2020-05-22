print("# Create new threads")
for i in range(252):
    print("thread{} = myThread({}, thread_number_list[{}], proxy_list[{}])".format(i+1, i+1, i, i))
print("# Start new Threads")
for i in range(252):
    print("thread{}.start()".format(i+1))

print("# Add threads to thread list")
for i in range(252):
    print("threads.append(thread{})".format(i+1))


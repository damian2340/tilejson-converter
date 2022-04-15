# random data
import sys, random, time

inputValues = [int(i) for i in sys.argv[1:]]

for i in range(inputValues[0], inputValues[1]):
    time.sleep(random.random() * 2)  # wait 0 to 5 seconds
    value = (random.random() * 20) # 0 to 20
    print(value, flush=True, end='')
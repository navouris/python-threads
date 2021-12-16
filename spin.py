import time
delay = 0.1
while True:
    for s in ["|", "/", "—", "\\", "|", "/", "—", "\\"]:
        print(s, end="\r"); time.sleep(delay)

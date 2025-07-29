import threading, time
from veritas import veritas
from veritas.datastructs import ThreadSafeDict

shared = ThreadSafeDict()
shared.set("status", "🔵 INIT")
shared.set("index", 0)
status_values = ["🟢 READY", "🟡 WORKING", "🔴 ERROR", "🟣 PAUSED"]

@veritas
def write(shared=shared):
    idx = shared.get("index", 0)
    status = status_values[idx % len(status_values)]
    shared.set("status", status)
    shared.set("index", idx + 1)
    print(f"[Writer] status → {status}")

@veritas
def read(shared=shared, name="?"):
    print(f"[{name}] sees → {shared.get('status')}")

# Spawn threads
def writer_loop():
    while True:
        write()
        time.sleep(2)

def reader_loop(name):
    while True:
        read(name=name)
        time.sleep(2)

# Go
if __name__ == "__main__":
    threading.Thread(target=writer_loop).start()
    threading.Thread(target=reader_loop, args=("Reader-1",)).start()
    threading.Thread(target=reader_loop, args=("Reader-2",)).start()

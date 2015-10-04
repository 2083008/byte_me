import threading
import filtercontroller as fc

def update():
    threading.Timer(60.0, update).start()
    fc.update_all_relevancies()

update()

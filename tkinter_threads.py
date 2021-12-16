import tkinter as tk
import threading
import time
import random

delay = 0.1

class Worker():
    def __init__(self, root, txt, x, y, **kw):
        self.root = root
        self.top = tk.Toplevel(root)
        self.top.geometry(f"300x300+{x}+{y}")
        self.l = tk.Label(self.top, text = txt, **kw)
        self.l.pack(fill='both', expand=1, padx=5, pady=5)
        self.sp = tk.Label(self.top, text = 'speed: ', font = ('Consolas', 30))
        self.sp.pack(fill= 'x', expand=1, padx=5, pady=5)
    def stop(self):
        self.alive = False
    def run(self):
        t = threading.Thread(target = self.working)
        t.deamon = True
        t.start()
    def working(self):
        self.alive = True
        delay = random.random()/10
        self.sp.config(text = f"speed: {1/delay:.1f}")
        while True:
            if not self.alive or not tk.Toplevel.winfo_exists(self.top): break
            # for s in ["|", "/", "—", "\\", "|", "/", "—", "\\"]:
            for s in ["◜ ", " ◝", " ◞", "◟ " ]:
                if tk.Toplevel.winfo_exists(self.top): #  μόνο αν το παράθυρο υπάρχει ακόμη, 
                    self.l.config(text=s)
                    time.sleep(delay)

class Main():
    def __init__(self, root):
        self.workers = []
        self.root = root
        self.font = ('Consolas', 200)
        self.fontButton = ('Consolas', 50)
        b = tk.Button(self.root, font=self.fontButton, text='run', command = self.run)
        b.pack(fill='both', expand=1, padx=5, pady=5)
        s = tk.Button(self.root, font=self.fontButton, text='stop', command = self.stop)
        s.pack(fill='both', expand=1, padx=5, pady=5)        
        for _ in range(3):
            self.workers.append(Worker(root, txt="◯", \
                x=200 + _*300, y= 100, bg='lightgreen', font=self.font))
        self.threads = []
    def run(self):
        for w in self.workers: 
            if tk.Toplevel.winfo_exists(w.top): w.run()
    def stop(self):
        for w in self.workers: 
            w.stop()
root = tk.Tk()
m = Main(root)
root.mainloop()

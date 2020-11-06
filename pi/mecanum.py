from gpiozero import Motor

class MnCart():
    def __init__(self, fl, fr, rl, rr):
        self._fl = Motor(*fl)
        self._fr = Motor(*fr)
        self._rl = Motor(*rl)
        self._rr = Motor(*rr)
        self._all = [[self._fl, self._fr], [self._rl, self._rr]]
    def forward(self):
        for r in self._all:
            for m in r:
                m.forward()
    def backward(self):
        for r in self._all:
            for m in r:
                m.backward()
    def rightslide(self):
        self._fl.forward()
        self._fr.backward()
        self._rr.forward()
        self._rl.backward()
    def leftslide(self):
        self._fl.backward()
        self._fr.forward()
        self._rl.forward()
        self._rr.backward()
    def forwardleft(self):
        self._fr.forward()
        self._rl.forward()
    
    def forwardright(self):
        self._fl.forward()
        self._rr.forward()
    
    def backleft(self):
        self._fl.backward()
        self._rr.backward()
    def backright(self):
        self._fr.backward()
        self._rl.backward()
    def turn_cw(self):
        self._fl.forward()
        self._fr.backward()
        self._rl.forward()
        self._rr.backward()
    def turn_ccw(self):
        self._fr.forward()
        self._fl.backward()
        self._rr.forward()
        self._rl.backward()
    def stop(self):
        for r in self._all:
            for m in r:
                m.stop()

if __name__ == '__main__':
    mc = MnCart((24, 25), (23, 22), (10, 9), (7, 8))
    
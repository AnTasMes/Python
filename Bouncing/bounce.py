import math
import matplotlib.pyplot as plt


h0 = 7000
v0 = 0
v = 0
dt = 0.1
h = h0
g = 10
hmax = h0
hnew = 50
hstop = 0.01
t = 0
t_last = -math.sqrt(2*h/g)
vmax = math.sqrt(2 * hmax * g)
print(t)
vt = v0 + g*t
freefall = True
tau = 0.1
rho = 0.75

H = []
T = []

while(hmax > hstop):
    if(freefall):
        hnew = h + v*dt - 0.5*g*dt*dt
        if(hnew < 0):
            t = t_last + 2*math.sqrt(2*hmax/g)
            freefall = False
            t_last = t + tau
            h = 0
        else:
            t = t + dt
            v = v - g*dt
            h = hnew
    else:
        t = t + tau
        vmax = vmax * rho
        v = vmax
        freefall = True
        h = 0
    hmax = 0.5*vmax*vmax/g
    H.append(h)
    T.append(t)

print("stopped bouncing at t=%.3f\n" % (t))

plt.figure()
plt.plot(T, H)
plt.xlabel('time')
plt.ylabel('height')
plt.title('bouncing ball')
plt.show()

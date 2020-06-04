
from simple_hydrodinamic_model.lib import load_file, calc_wind, coriolis_parameter, predict_step
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
plt.rcParams['animation.convert_path'] = r'C:\Program Files\ImageMagick-7.0.10-Q16\magick.exe'
dn = 100000
l = coriolis_parameter()
X, Y, F = load_file(r'GEO.dat', dn, dn)
ug, vg = calc_wind(F)
steps = 3000
dt = 300
F_arr = np.zeros(shape=(steps, 40, 40), dtype=np.float64)
ug_arr = np.zeros(shape=(steps, 40, 40), dtype=np.float64)
vg_arr = np.zeros(shape=(steps, 40, 40), dtype=np.float64)

print((np.max(F)-np.min(F)))

F_arr[0] = F
vg_arr[0] = vg
ug_arr[0] = ug

for i in range(1, steps):
    Fp,ug,vg = predict_step(F_arr[i-1], ug_arr[i-1], vg_arr[i-1], 5)
    F_arr[i] = Fp
    vg_arr[i] = vg
    ug_arr[i] = ug
levels = []
min = np.min(F[:][:])-500
for i in range(30):
    dn = (np.max(F[:][:]) - np.min(F[:][:]))/20
    min += dn
    levels.append(min)

#Вывод результатов ветер
fig, ax = plt.subplots(figsize=(8, 8))
islolines = ax.contour(X, Y, F, levels=levels, colors='black')  # Рисуем изолинии
gradient = ax.contourf(X, Y, F, levels=levels)  # Заливаем градиентом
# bar = fig.colorbar(gradient)  # Выставляем градиентную шкалу
# wind = ax.quiver(X, Y, ug, vg, scale = 10)  # Наносим векторы ветр
ax.set_title('Поле геострофического ветра на уровне 500 гПа')
ax.set_aspect('equal')
# plt.show()
# plt.close()


def animate(i):
    global X,Y,ax
    # global wind
    global islolines, gradient
    Fp = F_arr[i]
    ugp,vgp = ug_arr[i], vg_arr[i]
    # wind.set_UVC(ugp, vgp)  # Наносим векторы ветр
    [i.remove() for i in islolines.collections]
    [i.remove() for i in gradient.collections]
    islolines = ax.contour(X, Y, Fp, levels=levels, colors='black')  # Рисуем изолинии
    gradient = ax.contourf(X, Y, Fp, levels=levels)  # Заливаем градиентом
    # wind.remove()
    # wind = ax.quiver(X, Y, ugp, vgp, scale=1, scale_units = 'inches')

anim = FuncAnimation(fig, animate, frames= steps, interval=1, blit=False)
anim.save('shallow_water.gif', writer='imagemagick')
plt.show()
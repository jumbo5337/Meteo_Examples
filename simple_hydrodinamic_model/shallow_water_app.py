
from simple_hydrodinamic_model.lib import load_file, calc_wind, coriolis_parameter, predict_step
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
# plt.rcParams['animation.convert_path'] = r'C:\Program Files\ImageMagick-7.0.10-Q16\magick.exe'
dn = 100000
l = coriolis_parameter()
X, Y, F = load_file(r'GEO.dat', dn)
ug, vg = calc_wind(F, dn)
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
    Fp,ug,vg = predict_step(F_arr[i-1], ug_arr[i-1], vg_arr[i-1], 5, dn)
    F_arr[i] = Fp
    vg_arr[i] = vg
    ug_arr[i] = ug

print(ug_arr[-1])
print("=========")
print(vg_arr[-1])


levels = np.mgrid[50000:60000:20j]

#Вывод результатов ветер
fig, ax = plt.subplots(figsize=(8, 8))
isolines = ax.contour(X, Y, F, levels=levels, colors='black')  # Рисуем изолинии
labels = ax.clabel(isolines,levels)
gradient = ax.contourf(X, Y, F, levels=levels)  # Заливаем градиентом
bar = fig.colorbar(gradient)  # Выставляем градиентную шкалу
# wind = ax.quiver(X, Y, ug, vg, scale = 10)  # Наносим векторы ветр
ax.set_title('Поле геострофического ветра на уровне 500 гПа')
ax.set_aspect('equal')
# plt.show()
# plt.close()


def animate(i):
    global X,Y,ax
    global wind
    global isolines, gradient, labels
    Fp = F_arr[i]
    # ugp,vgp = ug_arr[i], vg_arr[i]
    # wind.set_UVC(ugp, vgp)  # Наносим векторы ветр
    [i.remove() for i in isolines.collections]
    [i.remove() for i in gradient.collections]
    isolines = ax.contour(X, Y, Fp, levels=levels, colors='black')  # Рисуем изолинии
    gradient = ax.contourf(X, Y, Fp, levels=levels)  # Заливаем гради
    for i in labels: i.remove()
    ticks = {}
    for i in levels :
        ticks[i] = str(int(i/100))
    labels = ax.clabel(isolines, levels, fmt= ticks, fontsize=8, inline=True)
    # wind.remove()
    # wind = ax.quiver(X, Y, ugp, vgp, scale=1, scale_units = 'inches')

anim = FuncAnimation(fig, animate, frames= steps, interval=1, blit=False)
plt.show()
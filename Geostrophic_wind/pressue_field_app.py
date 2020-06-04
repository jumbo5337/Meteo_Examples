import numpy as np
import matplotlib.pyplot as plt
from numpy import sin
from mpl_toolkits.axes_grid1 import make_axes_locatable

# Константы
dn = 100000  # Шаг сетки, М
fi = np.radians(60)  # Кассчёт на широте 60 градусов
w = 7.29e-5  # Угловая скорость вращения земли
l = 2 * w * sin(fi)  # Параметр Кариолиса
# Подготовка данных
F = np.loadtxt("GEO.dat", delimiter=' ')  # Загружаем данные по геопотенциалу
X = [i * dn for i in range(len(F[0]))]  # Задаем массивы для координат
Y = [i * dn for i in range(len(F))]
# Рассчётная часть
dy, dx = np.gradient(F, dn)  # Считаем градиенты геопотенциала по Oy и Ox
ug = -dy * l  # Рассчитываем компоненты геострофического ветра
vg = dx * l
# Расчёт дивиргенции и завихрённости
udy, udx = np.gradient(ug, dn)
vdy, vdx = np.gradient(vg, dn)
rotor = vdx - udy
div = udx + udy
# Вывод результатов ветер
fig, ax = plt.subplots(figsize=(8, 8))
islolines = ax.contour(X, Y, F, levels=20, colors='black')  # Рисуем изолинии
gradient = ax.contourf(X, Y, F, levels=20)  # Заливаем градиентом
fig.colorbar(gradient)  # Выставляем градиентную шкалу
ax.quiver(X, Y, ug, vg)  # Наносим векторы ветра
ax.set_aspect('equal')  # Выставляем соотношение сторон
ax.set_title('Поле геострофического ветра на уровне 500 гПа')
plt.show()
plt.close()
# Вывод результатов  ротор
fig, ax = plt.subplots(ncols=2,figsize=(8, 8))
islolines = ax[0].contour(X, Y, F, levels=20, colors='black')  # Рисуем изолинии
gradient = ax[0].contourf(X, Y, rotor, levels=20, cmap = 'jet')  # Заливаем градиентом
divider = make_axes_locatable(ax[0])
cax = divider.append_axes("right", size="5%", pad=0.1)
fig.colorbar(gradient, ax=ax[0], cax = cax)  # Выставляем градиентную шкалу
ax[0].quiver(X, Y, ug, vg)  # Наносим векторы ветра
ax[0].set_aspect('equal')  # Выставляем соотношение сторон
ax[0].set_title('Завихренность геострофического ветра \n на уровне 500 гПа')
ax[0].set_yticks([])
ax[0].set_xticks([])
islolines = ax[1].contour(X, Y, F, levels=20, colors='black')  # Рисуем изолинии
gradient = ax[1].contourf(X, Y, div, levels=20, cmap = 'jet')  # Заливаем градиентом
divider = make_axes_locatable(ax[1])
cax = divider.append_axes("right", size="5%", pad=0.1)
fig.colorbar(gradient,ax=ax[1], cax=cax)  # Выставляем градиентную шкалу
ax[1].quiver(X, Y, ug, vg)  # Наносим векторы ветра
ax[1].set_aspect('equal')  # Выставляем соотношение сторон
ax[1].set_title('Дивиргенция геострофического ветра \n на уровне 500 гПа')
ax[1].set_yticks([])
ax[1].set_xticks([])
plt.show()
plt.close()

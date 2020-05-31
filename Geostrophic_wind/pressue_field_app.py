import numpy as np
import matplotlib.pyplot as plt
from numpy import sin
import matplotlib.colors as mcol

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
fig, ax = plt.subplots(figsize=(8, 8))
islolines = ax.contour(X, Y, F, levels=20, colors='black')  # Рисуем изолинии
gradient = ax.contourf(X, Y, rotor, levels=20, cmap = 'jet')  # Заливаем градиентом
fig.colorbar(gradient)  # Выставляем градиентную шкалу
ax.quiver(X, Y, ug, vg)  # Наносим векторы ветра
ax.set_aspect('equal')  # Выставляем соотношение сторон
ax.set_title('Завихренность геострофического ветра на уровне 500 гПа')
plt.show()
plt.close()
# Вывод результатов дивиргенция
fig, ax = plt.subplots(figsize=(8, 8))
islolines = ax.contour(X, Y, F, levels=20, colors='black')  # Рисуем изолинии
gradient = ax.contourf(X, Y, div, levels=20)  # Заливаем градиентом
fig.colorbar(gradient)  # Выставляем градиентную шкалу
ax.quiver(X, Y, ug, vg)  # Наносим векторы ветра
ax.set_aspect('equal')  # Выставляем соотношение сторон
ax.set_title('Дивиргенция геострофического ветра на уровне 500 гПа')
plt.show()
plt.close()

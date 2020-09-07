import numpy as np
from numpy import sin, gradient



def coriolis_parameter (fi = 60):
    fi = np.radians(fi)  # Кассчёт на широте 60 градусов
    w = 7.29e-5  # Угловая скорость вращения земли
    return 2 * w * sin(fi)

def load_file(filename, dn):
    F = np.loadtxt(filename, delimiter=' ')  # Загружаем данные по геопотенциалу
    X = [i * dn for i in range(len(F[0]))]  # Задаем массивы для координат
    Y = [i * dn for i in range(len(F))]
    return X,Y,F

def calc_wind(F, dn):
    l = coriolis_parameter()
    dy, dx = gradient(F, dn)  # Считаем градиенты геопотенциала по Oy и Ox
    ug = -dy * l  # Рассчитываем компоненты геострофического ветра
    vg = dx * l
    return ug,vg

def predict_step(F,ug,vg, dt, dn):
    l = coriolis_parameter()
    Fdy,Fdx = gradient(F, dn)
    ugDy, ugDx = gradient(ug, dn)
    vgDy, vgDx = gradient(vg, dn)
    ugP = ug - dt*(ug*ugDx + vg*ugDy) -dt*Fdx +dt* l*vg
    vgP = vg - dt*(ug*vgDx + vg*vgDy) -dt*Fdy -dt*l*ug
    FuDx = gradient(F*ug, dn)[1]
    FvDy = gradient(F*vg, dn)[0]
    Fp = F - dt*(FuDx + FvDy)
    return Fp, ugP, vgP
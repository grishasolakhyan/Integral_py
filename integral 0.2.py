import numpy as np;
import matplotlib.pyplot as plt
import math

n=20;
oX1=0;
oX2=10;

def func (fun_st, x):
    fun=eval(fun_st)
    return fun
def rectangle(oX1, oX2, n):
    h=(oX2-oX1)/n
    sum=0
    btx=oX1+h/2
    while (btx<oX2):
        sum+=func(fun_st, btx)
        btx+=h
    return sum*h
def trapezium(oX1, oX2, n):
    h=(oX2-oX1)/n
    btx=oX1+h
    sum=(func(fun_st, oX1)+func(fun_st, oX2))/2
    for i in range (1, n):
        sum+=func(fun_st, btx)
        btx+=h
    return sum*h
def Simpson(oX1, oX2, n):
    btx=oX1
    h=(oX2-oX1)/n
    sum=func(fun_st, oX1)+func(fun_st, oX2)
    sum1=0
    sum2=0
    for i in range (1, n, 2):
        sum1+=func(fun_st, btx+i*h)
    for i in range (2, n, 2):
        sum2+=func(fun_st, btx+i*h)
    sum=(h/3)*(sum+4*sum1+2*sum2)
    return sum





fun_st = input('Введите уравнение функции f(x) = ')

print ("Левая граница = ", oX1, sep='')
print ("Правая граница = ", oX2, sep='')
print ("Число разбиений = ", n, sep='')

print ("\nМЕТОД ПРЯМОУГОЛЬНИКОВ")
print ("I = ", round(rectangle(oX1, oX2, n), 6))
print ("\nМЕТОД ТРАПЕЦИЙ")
print ("I = ", round(trapezium(oX1, oX2, n), 6))
print ("\nМЕТОД СИМПСОНА")
print ("I = ", round(Simpson(oX1, oX2, n), 6))




fig = plt.figure()
fig.patch.set_facecolor('#4a5b67')
fig.patch.set_alpha(1)

ax = fig.add_subplot(111)
ax.patch.set_alpha(0.0)

t=np.arange(oX1, oX2, 0.1)
y=func(fun_st, t)
plt.plot(t, y, color='#ffa1c0')
plt.fill_between(t, y, np.zeros_like(y), color='#bd305b')
plt.show()
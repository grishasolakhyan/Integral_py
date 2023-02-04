import numpy as np;
import matplotlib.pyplot as plt
import math

n=20;
oX1=-1;
oX2=1;
x=1;

def func (x):
    return 2*x*x+x+5

def rectangle(oX1, oX2, n):
    h=(oX2-oX1)/n
    sum=0
    btx=oX1+h/2
    while (btx<oX2):
        sum+=func(btx)
        btx+=h
    return sum*h

def trapezium(oX1, oX2, n):
    h=(oX2-oX1)/n
    btx=oX1+h
    sum=(func(oX1)+func(oX2))/2
    for i in range (1, n):
        sum+=func(btx)
        btx+=h
    return sum*h

def Simpson(oX1, oX2, n):
    btx=oX1
    h=(oX2-oX1)/n
    sum=func(oX1)+func(oX2)
    sum1=0
    sum2=0
    for i in range (1, n, 2):
        sum1+=func(btx+i*h)
    for i in range (2, n, 2):
        sum2+=func(btx+i*h)
    sum=(h/3)*(sum+4*sum1+2*sum2)
    return sum

print ("Левая граница = ", oX1, sep='')
print ("Правая граница = ", oX2, sep='')
print ("Число разбиений = ", n, sep='')
print ("\nМЕТОД ПРЯМОУГОЛЬНИКОВ")
print ("I = ", rectangle(oX1, oX2, n))
print ("\nМЕТОД ТРАПЕЦИЙ")
print ("I = ", trapezium(oX1, oX2, n))
print ("\nМЕТОД СИМПСОНА")
print ("I = ", Simpson(oX1, oX2, n))

t=np.arange(oX1, oX2, 0.1)
y=func(t)
plt.plot(t, y)
plt.show()
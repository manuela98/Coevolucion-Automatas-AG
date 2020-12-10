import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.image as mgimg
import numpy as np
from scipy import ndimage
import streamlit as st
import time
import pandas as pd


st.markdown("<h1 style='text-align: center; color: black;'>Robots Conserjes</h1>", unsafe_allow_html=True)

# better matrix
robby_matrix = np.loadtxt('better_robby_matrix.txt', dtype=int)
ones = np.where(robby_matrix==1)
twos =  np.where(robby_matrix==2)




fig, ax = plt.subplots( figsize=(5,5))
plt.axis([0, 1000, 0, 1000])
major_ticks = np.arange(0, 1001, 100)
ax.set_xticks(major_ticks)
ax.set_yticks(major_ticks)

plt.setp(ax.get_xticklabels(), visible=False)
plt.setp(ax.get_yticklabels(), visible=False)
ax.tick_params(axis='both', which='both', length=0)
ax.set_aspect('equal', adjustable='box')
ax.grid()
plt.gca().invert_yaxis()


# Put cans one

can = 'soda_40.png'
img_can = mgimg.imread(can)
rotated_img = ndimage.rotate(img_can, 180)
for i in range(len(ones[1])):
    #izquierda, derecha, abajo, arriba
    canobj = ax.imshow(rotated_img,extent=[ones[1][i]*100+50-img_can.shape[1]/2, ones[1][i]*100+50+img_can.shape[1]/2, ones[0][i]*100+50-img_can.shape[0]/2, ones[0][i]*100+50+img_can.shape[0]/2], zorder=1)
#print(img_can.shape[1],img_can.shape[0])

# Put cans one
can = 'soda_2_40.png'
img_can = mgimg.imread(can)
rotated_img = ndimage.rotate(img_can, 180)
for i in range(len(twos[1])):
    #izquierda, derecha, abajo, arriba
    canobj = ax.imshow(rotated_img,extent=[twos[1][i]*100+50-img_can.shape[1]/2, twos[1][i]*100+50+img_can.shape[1]/2, twos[0][i]*100+50-img_can.shape[0]/2, twos[0][i]*100+50+img_can.shape[0]/2], zorder=1)
#print(img_can.shape[1],img_can.shape[0])


f = open('better_robby.txt', 'r')
lines = f.read().splitlines()
last_line = lines[-1]
f.close()
list_str = last_line.split(',')
path_roby = [int(i) for i in list_str]



fname='robot_75.png'
img = mgimg.imread(fname)
rotated_robby = ndimage.rotate(img, 180)
imobj = ax.imshow(rotated_robby,extent=[800+12.5, 800+img.shape[1]+12.5, 125, 200], zorder=0)
fname='robot_2_75.png'
img = mgimg.imread(fname)
rotated_robby = ndimage.rotate(img, 180)
imobj = ax.imshow(rotated_robby,extent=[100+12.5, 100+img.shape[1]+12.5, 525, 600], zorder=0)
the_plot = st.pyplot(plt)




def mov_este(imobj):
    data = imobj.get_extent()
    imobj.set_extent([data[0]+20, data[1]+20, data[2] ,data[3]])
    return imobj

def mov_oeste(imobj):
    data = imobj.get_extent()
    imobj.set_extent([data[0]-20, data[1]-20, data[2] ,data[3]])
    return imobj

def mov_sur(imobj):
    data = imobj.get_extent()
    imobj.set_extent([data[0], data[1], data[2]+20 ,data[3]+20])
    return imobj


def mov_norte(imobj):
    data = imobj.get_extent()
    imobj.set_extent([data[0], data[1], data[2]-20 ,data[3]-20])
    return imobj

def random(imobj):
    actions = [
        mov_este,
        mov_oeste,
        mov_sur,
        mov_norte
    ]
    name_actions = ['random-este','random-oeste','random-norte','random-sur'] # para imprimir los nombres
    name_action = np.random.choice(name_actions) # escoje la accion en los nombres
    index_action = name_actions.index(name_action) # busca el indice de la accion en los nombres
    action = actions[index_action] # busca la accion en las acciones segun el indice
    action
    return action,name_action


def quieto(imobj):
    print('quieto')
    return imobj

def recoger(imobj):
    print('recoge')
    return imobj

def memoria_random():
    global imobj
    global contador
    global direccion_random
    global nombre_accion
    if contador==0:
        action, nombre_accion = random(imobj)
        imobj = action(imobj)
        contador = contador +1
        direccion_random = action
        print(nombre_accion,contador)
    elif contador >0 and contador<=3:
        direccion_random(imobj)
        contador = contador +1
        print(nombre_accion,contador)
    else:
        # contador==4:
        direccion_random(imobj)
        contador = 0
        print(nombre_accion,contador)

long_list = []
for i in path_roby:
    long_list +=[i]*5


contador = 0
direccion_random = None
nombre_accion = None
x = [imobj.get_extent()[0]]
y = [imobj.get_extent()[3]]
vertical = 0
horizonral = 0
'''def animate(i):
    global long_list
    global imobj
    global contador
    global direccion_random
    global nombre_accion
    global x,y
    global vertical,horizonral
    if long_list[i]==0:
        print('Norte')
        vertical = 1
        imobj = mov_norte(imobj)
    if long_list[i]==1:
        print('Este')
        horizonral = 1
        imobj = mov_este(imobj)
    if long_list[i]==2:
        print('Oeste')
        hortizontal = -1
        imobj = mov_oeste(imobj)
    if long_list[i]==3:
        print('Sur')
        imobj = mov_sur(imobj)
        vertical = -1
    if long_list[i]==4:
        print('Entro')
        memoria_random()
    if long_list[i]==5:
        imobj = quieto(imobj)
    if long_list[i]==6:
        imobj = recoger(imobj)
    coordenada_final =  imobj.get_extent()
    y+= [coordenada_final[3]]
    x+= [coordenada_final[0]]
    ax.plot(x,y)
    vertical = 0
    horizonral = 0
    the_plot.pyplot(plt)
    #return imobj,
#anim = animation.FuncAnimation(fig, animate, frames=len(long_list),  interval=10, repeat=False)
#ax.set_aspect('equal')
#plt.show()'''


#time.sleep(15)
#print(long_list)
'''for i in range(len(long_list)):
    animate(i)
    time.sleep(0.2)'''
# Traductor
st.markdown("<h3 style='text-align: center; color: black;'>Estrategia Robot A</h3>", unsafe_allow_html=True)
dict = {0:'North',
        1:'East',
        2: 'West',
        3: 'South',
        4: 'Random',
        5: 'Stay put',
        6: 'Pick up'}

North = ['Wall']
South = ['Empty']
East = ['Empty']
West = ['Wall']
Current_Site = ['Empty']
Action = [dict[path_roby[0]]]

dict_action = {0: [-1,0],
            1: [0,1],
            2: [0,-1],
            3: [1,0],
            4: [0,0], # Saber cual fue el movimiento random
            5: [0,0],
            6: [0,0]}

def found(posicion):
    global robby_matrix
    if ((posicion >=0 ).sum() == posicion.size).astype(np.int)==0:
        return 'Wall'
    else:
        try:
            elemento = robby_matrix[posicion[0],posicion[1]]
            if elemento == 0:
                return 'Empty'
            elif elemento ==1:
                return 'Can'
        except:
            return 'Wall'

posicion  = [np.array([0,0])]
for i in range(len(path_roby)-1):
    posicion += [posicion[-1] + np.array(dict_action[path_roby[i]])] # Se hace el movimiento en direccion de la accion
    posicion_actual = posicion[-1]
    posicion_norte = posicion[-1] + np.array(dict_action[0])
    posicion_sur = posicion[-1] + np.array(dict_action[3])
    posicion_este = posicion[-1] + np.array(dict_action[1])
    posicion_oeste = posicion[-1] + np.array(dict_action[2])

    North += [found(posicion_norte)]
    South += [found(posicion_sur)]
    East += [found(posicion_este)]
    West += [found(posicion_oeste)]
    Current_Site += [found(posicion_actual)]
    Action+= [dict[path_roby[i+1]]]






data = {'North':North,
        'South': South,
        'East': East,
        'West': West,
        'Current Site': Current_Site,
        'Action': Action}
frame = pd.DataFrame(data,columns = ['North','South','East','West','Current Site','Action'])
st.dataframe(frame)

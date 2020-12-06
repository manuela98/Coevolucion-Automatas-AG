# Coevolución de autómatas simulados con algoritmos genéticos  
Esta herramienta simula dos autómatas con algoritmos genéticos, estos coevolucionan en un mismo ambiente, una cuadrícula bidimensional rodeada de cuatro paredes con características especificas, los robots deben tomar decisiones de colaboración o competencia mientras cumplen su tarea de conserjes (deben recoger latas vacias de soda) . El objetivo del paquete, es, mediante el diseño de experimentos, generar y estudiar las estrategias de coevolución y recolección eficientes.   
# Descripción del problema  
Dos robots conserjes, robotA y robotB, tienen como objetivo limpiar un ambiente, recogiendo latas vacías de soda,  en este caso una cuadrícula nxn, las latasA y latasB están distribuidas con probabilidades pA y pB respectivamente. Cada gen, representa un acción: 0 = Mover al norte,  1 = Mover al este, 2 = Mover al sur, 3 = Mover al oeste, 4 = Permanecer quieto, 5 = Movimiento aleatorio, 6 = Recoger lata. Cada individuo de la población es una cadena de 1024 número entre 0 y 6, 1024 debido a que cada robot puede ver el contenido de 5 sitios (norte, sur , este, oeste, actual)  y tiene 4 posibles situaciones en las celdas (vacía, pared, lataA, lata B), esto es 1024 posibles situaciones: 4x4x4x4x4 = 1024 (no se descartan las situaciones imposibles).
# Dependencias 
Python 3 en adelante  
yaml  
tqdm   
# Configuración  
La configuración de las variables se realiza en el archivo ´config.yaml´, se pueden podificar los valores de la cuadrícula, de evolución, de simulación y de coevolución, además de un adn útil para la comparación del rendimiento en cada experimento.
# Uso
1. Clonar el repositorio ```git clone https://github.com/manuela98/Coevolucion-Automatas-AG.git```  
2. Configurar y ejecutar en el símbolo del sistema o terminal ```python main.py```  
El uso de otras características se explican en el cuadernillo de jupyter.

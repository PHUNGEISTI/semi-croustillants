import tensorflow as tf
from keras.datasets import mnist


#On commence par ouvrir une session interactive

tf.InteractiveSession

#Tenseurs et matrices particuliers. Exemples

A = tf.ones([2,2,3])
B = tf.zeros([3,4])
Id = tf.eye(4)
d = tf.constant([1.,5.,4.,0.])
D = tf.diag(d)


#matrices et leur produit

A = tf.constant([1., 2., 3., 3.,4.,5.])
A = tf.reshape(A,(3,2))

B = tf.constant([[5.,1.],[0.,2.]])

C=tf.matmul(A, B)

#Et ensuite 

C.eval


#Création d'une image binaire, une image niveau de gris et une image en couleur

imb = tf.random_uniform((28,28), minval=0, maxval=2, dtype=tf.int32)
img = tf.random_uniform((28,28), minval=0, maxval=256, dtype=tf.int32)
imc = tf.random_uniform((28,28,3), minval=0, maxval=256, dtype=tf.int32)

taille1 = 100
taille2 = 15
w1 = tf.Variable(tf.zeros([taille1, taille2]))
w2 = tf.Variable(tf.random_normal((taille1, taille2), mean=0, stddev=1))

#Ensuite nous avons besoin d'une session pour évaluer ces tableaux et d'abord initialiser les variables

init_op = tf.global_variables_initializer()
sess = tf.Session()

sess.run(init_op)

sess.run(w1)

#Et pour modifier les valeurs de w1 on peut par exemple procéder comme suit :

sess.run(tf.assign(w1,tf.random_uniform((taille1, taille2), minval=1, maxval=20)))

#Fonction permettant de calculer la sortie d'un réseau simple (1 seule couche cachée) dont les paramètres sont intialisés
#aléatoirement

def init_simple_neural_network(data):
    hidden_layer = {'weights':tf.Variable(tf.random_normal([784, n_nodes_h])),'biases':tf.Variable(tf.random_normal([n_nodes_h]))}
    output_layer = {'weights':tf.Variable(tf.random_normal([n_nodes_h, n_classes])),'biases':tf.Variable(tf.random_normal([n_classes]))}
    l = tf.add(tf.matmul(data,hidden_layer['weights']), hidden_layer['biases'])
    output = tf.matmul(l,output_layer['weights']) + output_layer['biases']
    return output


#Récupération et étude des données

(x_train, y_train), (x_test, y_test) = mnist.load_data()

#Quel est le type et la taille de chacun des résultats ?
#appliquez min et max
#type des données

#Type des résultats : appliquez type(). On trouve numpy.ndarray

#En utilisant l'aide de numpy.array

x_train.dtype
x_train.shape
x_train.max()
x_train.min()

#On vérie ce faisant que les x_ sont des matrices 28*28 d'entiers compris entre 0 et 255 (niveaux de gris)
#On vérie ce faisant que les y_ sont des d'entiers compris entre 0 et 9 (des chiffres)
#On vérifie aussi que x_train et y_train contiennet 60000 éléments 
#              et que x_test et y_test contiennet 10000 éléments
			  
#Tranformations des images en un seule matrice de réels compris entre 0 et 1. L'objecif est de préparer le
#travail de notre réseau de neurones qui manipule des données réelles comprises entre 0 et 1

x_train = x_train.reshape(60000, 784)
x_test = x_test.reshape(10000, 784)
x_train = x_train.astype('float32')
x_test = x_test.astype('float32')
x_train /= 255
x_test /= 255

#Visulation de quelques images

import matplotlib as mpl
import matplotlib.pyplot as plt

A=x_train[0,:].reshape([28,28])
plt.figure()
plt.imshow(A, cmap='gray')
plt.grid(True)
plt.show()

#On peut aussi représenter plusieurs images avec le code suivant :

plt.figure(figsize=(5, 5), dpi=150)
for i in range(100):
  plt.subplot(10,20,i+1)
  plt.imshow(x_train[i,:].reshape([28,28]), cmap='gray')
  plt.axis('off')
plt.show()

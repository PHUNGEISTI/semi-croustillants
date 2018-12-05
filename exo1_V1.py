# Création d'un RNN à une seule couche cachée/Sortie binaire
from keras.models import Sequential
from keras.layers import Dense
import numpy
# Fixer la valeur du seed pour la reproducibilité des résultats
numpy.random.seed(7)
# Lecture du fichier de données
dataset = numpy.loadtxt("pima-indians-diabetes.csv", delimiter=",")
# Séparer chaque ligne du fichier en un input et un output
X = dataset[:,0:8]
Y = dataset[:,8]
# Création du modèle. Pour chaque niveau on précise
# le nombre de neurones et la fonction d'activation
model = Sequential()
model.add(Dense(12, input_dim=8, activation='relu'))
model.add(Dense(8, activation='relu'))
model.add(Dense(1, activation='sigmoid'))
#Affichage d'un récapitulatif du modèle
model.summary()
model.get_config()
# Compiler le modèle. Fonction d'erreur entropie, adam (descente du gradient), 
# sortie binanire ==> choix de la précision comme critère d'évaluation 
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
# Apprentissage
model.fit(X, Y, epochs=150, batch_size=10)
# Evaluation du modèle
scores = model.evaluate(X, Y)
print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))

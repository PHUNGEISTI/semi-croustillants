import numpy as np
import os

###################################################
image_size = 28
pixel_depth = 255.0

def maybe_pickle(folder, min_num_images_per_class):
  data_folders = os.listdir(folder)
  dataset_names = []
  for folder in data_folders:
    set_filename = folder + '.pickle'
    print(set_filename)
    dataset_names.append(set_filename)
    print('Pickling %s.' % set_filename)
    dataset = load_letter(folder, min_num_images_per_class)
    try:
      with open(set_filename, 'wb') as f:
        pickle.dump(dataset, f, pickle.HIGHEST_PROTOCOL)
    except Exception as e:
      print('Unable to save data to', set_filename, ':', e)
  return dataset_names


def load_letter(folder, min_num_images):
  image_files = os.listdir(folder)
  dataset = np.ndarray(shape=(len(image_files), image_size, image_size),dtype=np.float32)
  image_index = 0
  print(folder)
  for image in os.listdir(folder):
    image_file = os.path.join(os.sep,folder, image)
    print(image_file)
  
  
#Programme principal

repTrain = os.path.join(os.sep, 'h:\\', 'dl', 'train')
repTest = os.path.join(os.sep, 'h:\\', 'dl', 'test')
#print(repTrain)
#data_folders = [d for d in os.listdir(repTrain)]
#print("Nombre de sous-rép = ",len(data_folders))
#print(data_folders)


maybe_pickle(repTrain, 1800)



# -*- coding: utf-8 -*-
"""
Entrenamiento Red neuronal con Tensorflow

"""

import os
import numpy as np
import tensorflow as tf
assert tf.__version__.startswith('2')

from tflite_model_maker import model_spec
from tflite_model_maker import image_classifier
from tflite_model_maker.config import ExportFormat
from tflite_model_maker.config import QuantizationConfig
from tflite_model_maker.image_classifier import DataLoader

import matplotlib.pyplot as plt


# Cargar imágenes de entrenamiento
folder = 'C:/Users/Alejandro Garcia/Desktop/PROYECTO PDI/DATA'
folder2 = 'C:/Users/Alejandro Garcia/Desktop/PROYECTO PDI/MODELO/'
data = DataLoader.from_folder("C:/Users/Alejandro Garcia/Downloads/nuevodataset")
train_data, test_data = data.split(0.9)

# Personalziar modelo de tensorflow.
model = image_classifier.create(train_data)

# Evaluar el modelo.
loss, accuracy = model.evaluate(test_data)

# Exportar el modelo de tensorflow lite y el archivo de etiquetas
model.export(export_dir=folder2)
model.export(export_dir=folder2, export_format = ExportFormat.LABEL)

#model.evaluate_tflite('model.tflite', test_data)



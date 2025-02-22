# -*- coding: utf-8 -*-
"""model (4).ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1AI3kADEy1FcA0KcgwYOoYRRqZw2FXkRj
"""

from tensorflow import keras
import tensorflow as tf
from keras.layers import Conv2D,Flatten,Dense,MaxPooling2D,Dropout

from keras.preprocessing.image import ImageDataGenerator
datagen=ImageDataGenerator()

import os
import cv2

from google.colab import drive
drive.mount('/content/drive')

!unzip '/content/drive/MyDrive/dataset.zip' -d './content'

"""## **unifeing ginger images**"""

# source_folder = "/content/content/dataset"
# destination_folder = "/content/resized_data"



# # List all files in the source folder
# files = os.listdir(destination_folder)


# print(len(files))

# # Loop through each file
# for file_name in files:
#     # Check if the file is an image (you can adjust the condition as needed)
#     if file_name.endswith(".jpg") or file_name.endswith(".png"):
#         # Read the image
#         image = cv2.imread(os.path.join(source_folder, file_name))

#         # Write the image to the destination folder
#         cv2.imwrite(os.path.join(destination_folder, file_name), image)

# totaldata = datagen.flow_from_directory('/content/drive/MyDrive/final_year_research_paper/resized_data',class_mode='categorical',batch_size=32)



source_folder = '/content/drive/MyDrive/final_year_research_paper/data'
destination_folder = '/content/drive/MyDrive/final_year_research_paper/resized_data'

# Ensure the destination folder exists
if not os.path.exists(destination_folder):
    os.makedirs(destination_folder)

"""## **resizing**"""

for class_folder in os.listdir(source_folder):
    class_path = os.path.join(source_folder, class_folder)

    # Ensure it's a directory
    if os.path.isdir(class_path):
        # Loop through each file in the class folder
        for file_name in os.listdir(class_path):
            # Read the image
            image = cv2.imread(os.path.join(class_path, file_name))

            # Resize the image to 256x256
            resized_image = cv2.resize(image, (256, 256))

            # Save the resized image to the destination folder
            destination_class_folder = os.path.join(destination_folder, class_folder)
            if not os.path.exists(destination_class_folder):
                os.makedirs(destination_class_folder)
            cv2.imwrite(os.path.join(destination_class_folder, file_name), resized_image)

print("Images resized and saved successfully!")

"""## **splitting**"""

import os
import shutil
from sklearn.model_selection import train_test_split
import random
random.seed(42)

source_folder = '/content/content/dataset'

# Destination folders for train, test, and validation sets
train_folder = '/content/content/train_resized_data'
test_folder = '/content/content/test_resized_data'
val_folder = '/content/content/validation_resized_data'

for folder in [train_folder, test_folder, val_folder]:
    if not os.path.exists(folder):
      os.makedirs(folder)

classes = os.listdir(source_folder)
for class_name in classes:
    class_path = os.path.join(source_folder, class_name)
    images = os.listdir(class_path)
    random.shuffle(images)
    train_images, test_val_images = train_test_split(images, test_size=0.3, random_state=42)
    test_images, val_images = train_test_split(test_val_images, test_size=0.5, random_state=42)
    for image in train_images:
        src_path = os.path.join(class_path, image)
        dest_path = os.path.join(train_folder, class_name, image)
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        shutil.copy(src_path, dest_path)

    for image in test_images:
        src_path = os.path.join(class_path, image)
        dest_path = os.path.join(test_folder, class_name, image)
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        shutil.copy(src_path, dest_path)

    for image in val_images:
        src_path = os.path.join(class_path, image)
        dest_path = os.path.join(val_folder, class_name, image)
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        shutil.copy(src_path, dest_path)

print("Images split into train, test, and validation sets successfully!")

"""## **model**"""

from keras.preprocessing.image import ImageDataGenerator
datagen=ImageDataGenerator(rescale=1./255)

train = datagen.flow_from_directory('/content/content/train_resized_data',class_mode='categorical',batch_size=32,target_size=(256,256))
test = datagen.flow_from_directory('/content/content/test_resized_data',class_mode='categorical',batch_size=32,target_size=(256,256))
valid = datagen.flow_from_directory('/content/content/validation_resized_data',class_mode='categorical',batch_size=32,target_size=(256,256))

x_train,xt=train.next()
print('Batch shape=',x_train.shape,'min=',x_train.min(),'max=',x_train.max())

class_names = ['Cherry_Powdery_mildew',
 'Cherry_healthy',
 'Grape_Black_rot',
 'Grape_Esca_(Black_Measles)',
 'Grape_Leaf_blight_(Isariopsis_Leaf_Spot)',
 'Grape_healthy',
 'Pepper,_bell___Bacterial_spot',
 'Pepper,_bell___healthy',
 'Strawberry_Leaf_scorch',
 'Strawberry_healthy',
 'Tomato_Bacterial_spot',
 'Tomato_Early_blight',
 'Tomato_Late_blight',
 'Tomato_Leaf_Mold',
 'Tomato_Septoria_leaf_spot',
 'Tomato_Spider_mites',
 'Tomato_Target_Spot',
 'Tomato_Yellow_Leaf_Curl_Virus',
 'Tomato_healthy']

from keras.optimizers import Adam

learning_rate = 0.0000001  # Adjust this value as needed

# Create Adam optimizer with custom learning rate
optimizer = Adam(learning_rate=learning_rate)

from keras.applications import ResNet50
model = tf.keras.models.Sequential([
    ResNet50(input_shape=(256, 256, 3), include_top=False),
])
# model.add(Conv2D(128, (3,3), activation='relu'))
# model.add(MaxPooling2D(2,2))
# # model.add(Conv2D(128, (1,1), activation='relu'))
# # model.add(MaxPooling2D(2,2))
model.add(Flatten())
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(7, activation='softmax'))
model.compile(loss='categorical_crossentropy',optimizer=optimizer,metrics=['accuracy'])


model.summary()

# model=keras.models.Sequential([
#     #1
#     keras.layers.Conv2D(filters=90,kernel_size=(5,5),strides=(2,2),activation='relu',input_shape=(256,256,3)),
#     keras.layers.BatchNormalization(),
#     keras.layers.MaxPool2D(pool_size=(2,2)),
#     #2
#     keras.layers.Conv2D(filters=256,kernel_size=(3,3),strides=(1,1),activation='relu',padding='same'),
#     keras.layers.BatchNormalization(),
#     keras.layers.MaxPool2D(pool_size=(3,3)),
#     #3
#     keras.layers.Conv2D(filters=256,kernel_size=(3,3),strides=(1,1),activation='relu',padding='same'),
#     keras.layers.BatchNormalization(),
#     #4
#     keras.layers.Conv2D(filters=256, kernel_size=(1,1), strides=(1,1), activation='relu', padding="same"),
#     keras.layers.BatchNormalization(),
#     #5
#     keras.layers.Conv2D(filters=256, kernel_size=(1,1), strides=(1,1), activation='relu', padding="same"),
#     keras.layers.BatchNormalization(),
#     keras.layers.MaxPool2D(pool_size=(2,2)),

#     keras.layers.Flatten(),
#     #6
#     keras.layers.Dense(512,activation='relu'),
#     keras.layers.Dropout(0.5),
#     #7
#     keras.layers.Dense(512,activation='relu'),
#     keras.layers.Dropout(0.5),
#     #8
#     keras.layers.Dense(7,activation='softmax')

# ])
# model.compile(loss='categorical_crossentropy',optimizer=optimizer,metrics=['accuracy'])
# model.summary()

# from keras.callbacks import ModelCheckpoint

# # Define the path to save the checkpoints
# checkpoint_path = "/content/drive/MyDrive/final_year_research_paper/model_checkpoint.h5"

# checkpoint_callback = ModelCheckpoint(filepath=checkpoint_path,
#                                       save_weights_only=False,  # Set to True if you only want to save the weights
#                                       save_best_only=False,  # Set to True if you only want to save the best model
#                                       verbose=1)

# model.load_weights('/content/drive/MyDrive/final_year_research_paper/model_checkpoint.h5')

history=model.fit(train,epochs=10,validation_data=valid)#,callbacks=[checkpoint_callback])
# history=model.fit(train,epochs=10,validation_data=valid)

# model.evaluate(test)

# model.save('/content/drive/MyDrive/final_year_research_paper/model.h5')

# import numpy as np
# from keras.preprocessing import image

# # Load the image
# img_path = '/content/drive/MyDrive/final_year_research_paper/test_resized_data/ginger/IMG_20231204_135256_112.jpg'  # Replace 'path_to_your_image.jpg' with the path to your image
# img = image.load_img(img_path, target_size=(256, 256))  # Load the image and resize it to match the input shape (256x256)

# img_array = image.img_to_array(img)
# img_array = np.expand_dims(img_array, axis=0)

# img_array = img_array / 255.0
# predictions = model.predict(img_array)

# predicted_class_index = np.argmax(predictions)
# print(class_names[predicted_class_index])

# import matplotlib.pyplot as plt

# # Get training and validation loss from the history object
# train_loss = history.history['loss']
# val_loss = history.history['val_loss']

# # Plot model loss vs. epoch
# epochs = range(1, len(train_loss) + 1)
# plt.plot(epochs, train_loss, 'b', label='Training loss')
# plt.plot(epochs, val_loss, 'orange', label='Validation loss')
# plt.title('Training and validation loss')
# plt.xlabel('Epochs')
# plt.ylabel('Loss')
# plt.legend()
# plt.savefig('/content/drive/MyDrive/final_year_research_paper/loss_plot.png')
# plt.show()



from keras import backend as K

def precision(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + K.epsilon())
    return precision

def recall(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    recall = true_positives / (possible_positives + K.epsilon())
    return recall

def f1_score(y_true, y_pred):
    precision_val = precision(y_true, y_pred)
    recall_val = recall(y_true, y_pred)
    return 2 * ((precision_val * recall_val) / (precision_val + recall_val + K.epsilon()))

predictions = model.predict(test)
y_pred = np.argmax(predictions, axis=1)
y_true = test.classes

print(precision(y_true,y_pred))
print(recall(y_true,y_pred))
print(f1_score(y_true,y_pred))

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, classification_report
from keras.preprocessing.image import ImageDataGenerator
import keras



# Make predictions
predictions = model.predict(test)
y_pred = np.argmax(predictions, axis=1)
y_true = test.classes

# Generate confusion matrix
conf_matrix = confusion_matrix(y_true, y_pred)

# Plot confusion matrix
plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', xticklabels=class_names, yticklabels=class_names)
plt.xlabel('Predicted labels')
plt.ylabel('True labels')
plt.title('Confusion Matrix')
plt.show()

# Generate classification report
cls_report = classification_report(y_true, y_pred, target_names=class_names)
print("Classification Report:\n", cls_report)


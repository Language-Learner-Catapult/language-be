# Beat tracking example
import librosa
import numpy as np

import base64
import io
import os
import soundfile as sf

# from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import LabelEncoder
# from keras.models import Sequential
# from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, LeakyReLU
# from keras.optimizers import RMSprop
# import matplotlib.pyplot as plt


# le = LabelEncoder()
# base64_audio_string = ""
# with open("./util/encoded-20240330185923.txt", "r") as file:
#     base64_audio_string = file.read()
# audio_bytes = base64.b64decode(base64_audio_string)
def decibelAnalysis(audio: io.BytesIO):
    # filename = librosa.example('nutcracker')
    # print(filename)
    y, sr = sf.read(audio, sr=None)
    D = librosa.stft(y)
    D_db = librosa.amplitude_to_db(D, top_db=None, ref=np.min)
    print(np.nanmean(D_db), np.nanmax(D_db))
    return (np.nanmean(D_db), np.nanmax(D_db))


# decibelAnalysis(io.BytesIO(audio_bytes))

# def getDecibelFreq(file):
#     y, sr = librosa.load(file, sr=None)
#     D = librosa.stft(y)
#     D_db = librosa.amplitude_to_db(D, top_db=None, ref = np.min)
#     return D_db
# def pad_2d_array(arr, target_length):
#     """Pad a 2D array with zeros to the desired length."""
#     padding = target_length - arr.shape[1]
#     if padding > 0:
#         return np.pad(arr, ((0, 0), (0, padding)))
#     else:
#         return arr
# def sentimentAnalysis(files):
#     emotion_key = {
#     "01": "neutral",
#     "02": "calm",
#     "03": "happy",
#     "04": "sad",
#     "05": "angry",
#     "06": "fearful",
#     "07": "disgust",
#     "08": "surprised"
#     }
#     print(files)
#     totalData = []
#     for fileName in os.listdir(files):

#         fileName = os.path.join(files, fileName)
#         if not fileName.endswith(".wav"):
#             continue
#         totalData.append([fileName, getDecibelFreq(fileName),{"sentiment": "-"}])
#     for item in totalData:
#         emotion_code = item[0].split('-')[2]
#         sentiment_label = emotion_key.get(emotion_code)
#         if sentiment_label:
#             item[2]['sentiment'] = sentiment_label
#     # shuffle data
#     np.random.shuffle(totalData)
#     x = []
#     y = []
#     for item in totalData:
#         x.append(item[1])
#         y.append(item[2]['sentiment'])
#     max_length = max(item.shape[1] for item in x)
#     data_padded = [pad_2d_array(item, max_length) for item in x]
#     x = np.array(data_padded)
#     y = np.array(y)
#     return (x,y)

# def trainModel(x, y):
#     x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

#     print("Training set size:", len(x_train))
#     print("Test set size:", len(x_test))


#     # Define the model architecture
#     model = Sequential()
#     model.add(Conv2D(32, (3, 3), input_shape=(x_train.shape[1], x_train.shape[2], 1)))
#     model.add(LeakyReLU())
#     model.add(MaxPooling2D((2, 2)))
#     model.add(Dropout(0.25))  # Dropout added here
#     model.add(Conv2D(64, (3, 3)))
#     model.add(LeakyReLU())
#     model.add(MaxPooling2D((2, 2)))
#     model.add(Flatten())
#     model.add(Dense(64))
#     model.add(LeakyReLU())
#     model.add(Dropout(0.25))  # And here
#     model.add(Dense(len(np.unique(y_train)), activation='softmax'))# Number of classes is the number of unique sentiments

#     # Compile the model
#     model.compile(optimizer=RMSprop(learning_rate=0.001), loss='sparse_categorical_crossentropy', metrics=['accuracy'])
#     y_train = le.fit_transform(y_train)
#     print(y_train)
#     y_test = le.transform(y_test)
#     # Train the model
#     model.fit(x_train[..., np.newaxis], y_train, epochs=10, batch_size=40, validation_data=(x_test[..., np.newaxis], y_test))
#     # Evaluate the model on the test set
#     test_loss, test_acc = model.evaluate(x_test[..., np.newaxis], y_test, verbose=2)
#     print('\nTest accuracy:', test_acc)
#     print('\nTest Loss:', test_loss)


#     # Use the model to make predictions
#     predictions = model.predict(x_test[..., np.newaxis])

#     # Convert the predictions from probabilities to class labels
#     predicted_labels = np.argmax(predictions, axis=1)

#     # Now predicted_labels contains the predicted class labels for the test set
#     print("Predicted labels:", predicted_labels)

# print("hey")

# x, y = sentimentAnalysis("data/temp_dataset/")
# print("done")

# trainModel(x,y)

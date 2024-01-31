import numpy as np
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.optimizers import Adam
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Flatten, Dense, Dropout
from tensorflow.keras.applications import VGG19
import json

def create_model(input_shape, num_classes, optimizer='adam', fine_tune=0):    
    conv_base = VGG19(include_top=False,
                     weights='imagenet', 
                     input_shape=input_shape)
    
    if fine_tune > 0:
        for layer in conv_base.layers[:-fine_tune]:
            layer.trainable = False
    else:
        for layer in conv_base.layers:
            layer.trainable = False

    top_model = conv_base.output
    top_model = Flatten(name="flatten")(top_model)
    top_model = Dense(4096, activation='relu')(top_model)
    top_model = Dense(1072, activation='relu')(top_model)
    top_model = Dropout(0.5)(top_model)
    output_layer = Dense(num_classes, activation='softmax')(top_model)
    
    model = Model(inputs=conv_base.input, outputs=output_layer)

    model.compile(optimizer=optimizer, 
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])
    
    return model

def getPrediction(filename):
    num_classes = 18
    input_shape = (70, 70, 3)
    optim = Adam(learning_rate=0.0001)
    
    model = create_model(input_shape, num_classes, optim, fine_tune=12)
    
    # Load the weights into the model
    model.load_weights("../VGG19/Dropout 0.5/tl_model_v18.weights.best.hdf5")
    
    image = load_img('./static/uploads/'+filename, target_size=(70, 70))
    image = img_to_array(image)
    image /= 255.0
    image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
    # image = preprocess_input(image)
    
    # Use the model directly for prediction (without assigning it to loaded_model)
    yhat = model.predict(image)
    
    # json_yhat = json.dumps({'yhat': (yhat*100).tolist()})
    
    # Use the class labels directly
    class_labels = ["ba", "ca", "da", "ga", "ha", "ja", "ka", "la", "ma", "na", "nga", "nya", "pa", "ra", "sa", "ta", "wa", "ya"]
    label_index = np.argmax(yhat)
    label = (class_labels[label_index])
    confidence = yhat[0][label_index] * 100

    print(yhat)
    print('%s (%.2f%%)' % (label, confidence))
    
    return label, confidence
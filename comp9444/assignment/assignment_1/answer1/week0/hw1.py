import tensorflow as tf
import matplotlib.pyplot as plt

from tensorflow import keras

def create_network(train_img, train_labels):
    model = keras.Sequential([
        keras.layers.Flatten(input_shape = (28,28)),
        keras.layers.Dense(128, activation=tf.nn.relu),
        keras.layers.Dense(10, activation=tf.nn.softmax)
    ])
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    model.fit(train_img, train_labels, epochs=5)
    return model


def test_network(model, test_img, test_labels):
    test_loss, test_acc = model.evaluate(test_img, test_labels)
    return test_acc

def main():
    fasion_minist = keras.datasets.fashion_mnist
    (train_img, train_labels), (test_img, test_labels) = fasion_minist.load_data()
    class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat', 'Sandal', 'Shirt', 'Sneaker', 
                    'Bag', 'Ankle boot']
    #print(train_img.shape)
    train_img = train_img/255.0
    test_img = test_img/255.0
    
    '''
    plt.figure(figsize=(10,10))
    for i in range(25):
        plt.subplot(5,5,i+1)
        plt.xticks([])
        plt.yticks([])
        plt.grid(False)
        plt.imshow(train_img[i])
        plt.xlabel(class_names[train_labels[i]])
    plt.show()
    '''
    model = create_network(train_img, train_labels)
    acc = test_network(model, test_img, test_labels)
    print("Accuracy on test set is: " + str(acc))

    

if __name__ == "__main__":
    main()

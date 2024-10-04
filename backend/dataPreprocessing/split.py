from sklearn.model_selection import train_test_split
import pandas as pd
import tensorflow as tf


def create_data_generator(dataframe, batch_size, augment=False, shuffle=True, target_size=(244, 244)):
    dataframe['label'] = dataframe['label'].astype(str)
    if augment:
        datagen = tf.keras.preprocessing.image.ImageDataGenerator(
            rescale=1. / 255,
            rotation_range=20,
            width_shift_range=0.2,
            height_shift_range=0.2,
            shear_range=0.2,
            zoom_range=0.2,
            horizontal_flip=True,
            fill_mode='nearest'
        )
    else:
        datagen = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1. / 255)

    generator = datagen.flow_from_dataframe(
        dataframe=dataframe,
        x_col='image_path',
        y_col='label',
        target_size=target_size,
        batch_size=batch_size,
        class_mode='binary',
        shuffle=shuffle
    )
    return generator


def split_data(labels_file_path):

    df = pd.read_csv(labels_file_path)

    train_df, val_df = train_test_split(df, test_size=0.25, random_state=42)

    train_df.to_csv('train_labels.csv', index=False)
    val_df.to_csv('val_labels.csv', index=False)


def main():
    split_data(labels_file_path='labels.csv')


if __name__ == '__main__':
    main()

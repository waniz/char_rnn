import numpy as np
import random
import sys
from keras.models import model_from_json, Sequential

# global params
MAXLEN = 16
STEP = 1
BATCH_SIZE = 1000
CHARS = 35


def sample(a, temperature=1.0):
    a = np.log(a) / temperature
    a = np.exp(a) / np.sum(np.exp(a))
    if sum(a) > 1.0:
        a *= 1 - (sum(a) - 1)
        if sum(a) > 1.0:
            a *= 0.99999
    return np.argmax(np.random.multinomial(1, a, 1))


def get_sample(model, temperatures):  # [0.2, 0.5, 1.0]
    for T in temperatures:
        print("------------Temperature", T)
        generated = ''
        sentence = 'примерный сэмпл выглядит '
        generated += sentence
        print("Generating with seed: " + sentence)
        print('')

        for i in range(400):
            char_to_int = dict((c, i) for i, c in enumerate(CHARS))
            int_to_char = dict((c, i) for i, c in enumerate(CHARS))

            seed = np.zeros((BATCH_SIZE, MAXLEN, len(CHARS)))
            for t, char in enumerate(sentence):
                seed[0, t, char_to_int[char]] = 1

            predictions = model.predict(seed, batch_size=BATCH_SIZE, verbose=2)[0]
            next_index = sample(predictions, T)
            next_char = int_to_char[next_index]

            sys.stdout.write(next_char)
            sys.stdout.flush()

            generated += next_char
            sentence = sentence[1:] + next_char
        print()


json_file = open('models/current_model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
trained_model = model_from_json(loaded_model_json)
trained_model.load_weights('models/weights_ep_3_loss_1.254_val_loss_1.267.h5')
trained_model.compile(loss='categorical_crossentropy', optimizer='rmsprop')





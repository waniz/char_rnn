import numpy as np
import random
import re
import sys
from keras.models import model_from_json


def sample(a, temperature=1.0):
    if temperature == 0:
        temperature = 1.0
    a = np.log(a) / temperature
    a = np.exp(a) / np.sum(np.exp(a))
    if sum(a) > 1.0:
        a *= 1 - (sum(a) - 1)
        if sum(a) > 1.0:
            a *= 0.9999
    return np.argmax(np.random.multinomial(1, a, 1))


def get_sample_chehov(model, temperatures):  # [0.2, 0.5, 1.0]
    # global params
    MAXLEN = 30
    STEP = 1
    BATCH_SIZE = 128

    raw_text = open('data/chehov.txt', encoding="utf-8").read()
    raw_text = raw_text.lower()
    raw_text_ru = re.sub("[^а-я, .\n]", "", raw_text)
    chars = sorted(list(set(raw_text_ru)))

    example_text = 'белая плотная шапка пены, большое облако, зависшее над полем созревшей пшеницы, ' \
                   'один только вид такой красоты заставляет сердце биться чаще, прогоняя из головы дурные мысли. ' \
                   'но только попробовав на вкус, почувствовав, как льется свежесть спелой пшеницы сквозь казавшиеся ' \
                   'такими плотными облака пены, можно ощутить всю полноту вкуса, почувствовать спрятавшиеся среди ' \
                   'колосьев яблоки, уловить невесть откуда взявшийся оттенок сладкой выпечки, а в конце ' \
                   'горечь, легкая и даже приятная. ' \
                   'плотный как туман ранним осенним утром, подсвеченный встающим ' \
                   'солнцем и такой же освежающий, как тот туман, напиток, похожий своим видом на осень, на вкус ' \
                   'больше походит на лето — пшеничный, со спелыми яблоками и горчинкой, легкой, едва уловимой. ' \
                   'описать этот вкус коротко так же тяжело, как описать воздух ранним весенним утром, однако стоит ' \
                   'сделать один глоток, как перед глазами встает поле, бескрайнее и золотое, полное созревших ' \
                   'колосьев пшеницы, за которым начинается яблоневый сад, окружающий усадьбу. и все они: и пшеница, ' \
                   'и яблоки, и легкий аромат выпечки к чаю из дома в саду переплетаются, ненавязчиво, где-то далеко,' \
                   ' но след оставляют четкий и явственный.' \
                   'ни горечи, ни тяжести, ни намека на тот обычный напиток в этом вкусе не найти. ' \
                   'с первого глотка — только легкость и свежесть антоновки сделаешь глоток, и пиво расцветает, ' \
                   'словно хочет улететь на воздух. а потом, чуть запоздав, подходят и пшеничные ноты, ' \
                   'которые звучат где-то далеко, как соловей в чаще за горячим полем.' \
                   'вкус раскинулся шатром сочной золотой пшеницы и чем-то еще еле уловимым, небольшим, таинственным, ' \
                   'что может показаться пряным ароматом бутонов гвоздики или утренней выпечкой.' \
                   'плотное и мягкое тело напитка словно в беспамятстве расплескалось на дне бокала, ' \
                   'в попытках скрыться от жаркой сладости солода — так усталые путники пытаются укрыться ' \
                   'от полуденного зноя в жидкой тени. для разнообразия мелькнет в напитке игривая прохлада ' \
                   'ягод или василька, вырастет на мгновение смолистая хвоя или раскинется яблоня. а потом ' \
                   'опять польется знойная степная горечь, сначала резковатая, но с каждым глотком более мягкая, ' \
                   'ленивая, уходящая куда-то за горизонт в длительное послевкусие.' \
                   'пиво пахнет молодой травкой, ягодами, цветущим садом и чем-то этаким особенным, веселым, весенним.' \
                   ' вкус продолжает аромат, будто взял горсть красных и черных ягодок, растянулся под выбеленной ' \
                   'вишней, да съел неторопливо, запив прохладной водой.' \
                   'бывает такая горечь, которая даже не горечь, а сплошной надрыв, оголенный нерв. ' \
                   'а бывает напротив, крепкое, чрезвычайно даже наполненное, но так по-особенному приготовленное, ' \
                   'что оно не только не зажимает тебя в тиски, но даже в некотором роде освобождает тебя. ' \
                   'есть в нем и горечь, и сладость, и травяная терпкость, и домашнее, деревянное тепло шоколада' \
                   ' и перца, и что-то еще; темное, как будто глядящее из самой глубины солодовой души'

    example_text = re.sub("[^а-я, .\n]", "", example_text)

    start_index = random.randint(0, len(example_text) - MAXLEN - 1)
    for T in temperatures:
        print("Che----------Temperature", T)
        generated = ''
        sentence = example_text[start_index:start_index + MAXLEN]
        generated += sentence
        print("Generating with seed: " + sentence)
        print('')

        for i in range(300):
            char_to_int = dict((c, i) for i, c in enumerate(chars))
            int_to_char = dict((i, c) for i, c in enumerate(chars))

            seed = np.zeros((BATCH_SIZE, MAXLEN, len(chars)))
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


def get_sample_do(model, temperatures):  # [0.2, 0.5, 1.0]
    # global params
    MAXLEN = 40
    STEP = 1
    BATCH_SIZE = 128

    raw_text = open('data/dost_best.txt', encoding="utf-8").read()
    raw_text = raw_text.lower()
    raw_text_ru = re.sub("[^а-я, .]", "", raw_text)
    chars = sorted(list(set(raw_text_ru)))

    example_text = 'белая плотная шапка пены, большое облако, зависшее над полем созревшей пшеницы, ' \
                   'один только вид такой красоты заставляет сердце биться чаще, прогоняя из головы дурные мысли. ' \
                   'но только попробовав на вкус, почувствовав, как льется свежесть спелой пшеницы сквозь казавшиеся ' \
                   'такими плотными облака пены, можно ощутить всю полноту вкуса, почувствовать спрятавшиеся среди ' \
                   'колосьев яблоки, уловить невесть откуда взявшийся оттенок сладкой выпечки, а в конце ' \
                   'горечь, легкая и даже приятная. ' \
                   'плотный как туман ранним осенним утром, подсвеченный встающим ' \
                   'солнцем и такой же освежающий, как тот туман, напиток, похожий своим видом на осень, на вкус ' \
                   'больше походит на лето — пшеничный, со спелыми яблоками и горчинкой, легкой, едва уловимой. ' \
                   'описать этот вкус коротко так же тяжело, как описать воздух ранним весенним утром, однако стоит ' \
                   'сделать один глоток, как перед глазами встает поле, бескрайнее и золотое, полное созревших ' \
                   'колосьев пшеницы, за которым начинается яблоневый сад, окружающий усадьбу. и все они: и пшеница, ' \
                   'и яблоки, и легкий аромат выпечки к чаю из дома в саду переплетаются, ненавязчиво, где-то далеко,' \
                   ' но след оставляют четкий и явственный.' \
                   'ни горечи, ни тяжести, ни намека на тот обычный напиток в этом вкусе не найти. ' \
                   'с первого глотка — только легкость и свежесть антоновки сделаешь глоток, и пиво расцветает, ' \
                   'словно хочет улететь на воздух. а потом, чуть запоздав, подходят и пшеничные ноты, ' \
                   'которые звучат где-то далеко, как соловей в чаще за горячим полем.' \
                   'вкус раскинулся шатром сочной золотой пшеницы и чем-то еще еле уловимым, небольшим, таинственным, ' \
                   'что может показаться пряным ароматом бутонов гвоздики или утренней выпечкой.' \
                   'плотное и мягкое тело напитка словно в беспамятстве расплескалось на дне бокала, ' \
                   'в попытках скрыться от жаркой сладости солода — так усталые путники пытаются укрыться ' \
                   'от полуденного зноя в жидкой тени. для разнообразия мелькнет в напитке игривая прохлада ' \
                   'ягод или василька, вырастет на мгновение смолистая хвоя или раскинется яблоня. а потом ' \
                   'опять польется знойная степная горечь, сначала резковатая, но с каждым глотком более мягкая, ' \
                   'ленивая, уходящая куда-то за горизонт в длительное послевкусие.' \
                   'пиво пахнет молодой травкой, ягодами, цветущим садом и чем-то этаким особенным, веселым, весенним.' \
                   ' вкус продолжает аромат, будто взял горсть красных и черных ягодок, растянулся под выбеленной ' \
                   'вишней, да съел неторопливо, запив прохладной водой.' \
                   'бывает такая горечь, которая даже не горечь, а сплошной надрыв, оголенный нерв. ' \
                   'а бывает напротив, крепкое, чрезвычайно даже наполненное, но так по-особенному приготовленное, ' \
                   'что оно не только не зажимает тебя в тиски, но даже в некотором роде освобождает тебя. ' \
                   'есть в нем и горечь, и сладость, и травяная терпкость, и домашнее, деревянное тепло шоколада' \
                   ' и перца, и что-то еще; темное, как будто глядящее из самой глубины солодовой души'

    example_text = re.sub("[^а-я, .\n]", "", example_text)

    start_index = random.randint(0, len(example_text) - MAXLEN - 1)
    for T in temperatures:
        print("Do----------Temperature", T)
        generated = ''
        sentence = example_text[start_index:start_index + MAXLEN]
        generated += sentence
        print("Generating with seed: " + sentence)
        print('')

        for i in range(300):
            char_to_int = dict((c, i) for i, c in enumerate(chars))
            int_to_char = dict((i, c) for i, c in enumerate(chars))

            seed = np.zeros((BATCH_SIZE, MAXLEN, len(chars)))
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


def get_sample_do2(model, temperatures):  # [0.2, 0.5, 1.0]
    # global params
    MAXLEN = 30
    STEP = 1
    BATCH_SIZE = 500

    raw_text = open('data/dost_best.txt', encoding="utf-8").read()
    raw_text = raw_text.lower()
    raw_text_ru = re.sub("[^а-я, .]", "", raw_text)
    chars = sorted(list(set(raw_text_ru)))

    example_text = 'белая плотная шапка пены, большое облако, зависшее над полем созревшей пшеницы, ' \
                   'один только вид такой красоты заставляет сердце биться чаще, прогоняя из головы дурные мысли. ' \
                   'но только попробовав на вкус, почувствовав, как льется свежесть спелой пшеницы сквозь казавшиеся ' \
                   'такими плотными облака пены, можно ощутить всю полноту вкуса, почувствовать спрятавшиеся среди ' \
                   'колосьев яблоки, уловить невесть откуда взявшийся оттенок сладкой выпечки, а в конце ' \
                   'горечь, легкая и даже приятная. ' \
                   'плотный как туман ранним осенним утром, подсвеченный встающим ' \
                   'солнцем и такой же освежающий, как тот туман, напиток, похожий своим видом на осень, на вкус ' \
                   'больше походит на лето — пшеничный, со спелыми яблоками и горчинкой, легкой, едва уловимой. ' \
                   'описать этот вкус коротко так же тяжело, как описать воздух ранним весенним утром, однако стоит ' \
                   'сделать один глоток, как перед глазами встает поле, бескрайнее и золотое, полное созревших ' \
                   'колосьев пшеницы, за которым начинается яблоневый сад, окружающий усадьбу. и все они: и пшеница, ' \
                   'и яблоки, и легкий аромат выпечки к чаю из дома в саду переплетаются, ненавязчиво, где-то далеко,' \
                   ' но след оставляют четкий и явственный.' \
                   'ни горечи, ни тяжести, ни намека на тот обычный напиток в этом вкусе не найти. ' \
                   'с первого глотка — только легкость и свежесть антоновки сделаешь глоток, и пиво расцветает, ' \
                   'словно хочет улететь на воздух. а потом, чуть запоздав, подходят и пшеничные ноты, ' \
                   'которые звучат где-то далеко, как соловей в чаще за горячим полем.' \
                   'вкус раскинулся шатром сочной золотой пшеницы и чем-то еще еле уловимым, небольшим, таинственным, ' \
                   'что может показаться пряным ароматом бутонов гвоздики или утренней выпечкой.' \
                   'плотное и мягкое тело напитка словно в беспамятстве расплескалось на дне бокала, ' \
                   'в попытках скрыться от жаркой сладости солода — так усталые путники пытаются укрыться ' \
                   'от полуденного зноя в жидкой тени. для разнообразия мелькнет в напитке игривая прохлада ' \
                   'ягод или василька, вырастет на мгновение смолистая хвоя или раскинется яблоня. а потом ' \
                   'опять польется знойная степная горечь, сначала резковатая, но с каждым глотком более мягкая, ' \
                   'ленивая, уходящая куда-то за горизонт в длительное послевкусие.' \
                   'пиво пахнет молодой травкой, ягодами, цветущим садом и чем-то этаким особенным, веселым, весенним.' \
                   ' вкус продолжает аромат, будто взял горсть красных и черных ягодок, растянулся под выбеленной ' \
                   'вишней, да съел неторопливо, запив прохладной водой.' \
                   'бывает такая горечь, которая даже не горечь, а сплошной надрыв, оголенный нерв. ' \
                   'а бывает напротив, крепкое, чрезвычайно даже наполненное, но так по-особенному приготовленное, ' \
                   'что оно не только не зажимает тебя в тиски, но даже в некотором роде освобождает тебя. ' \
                   'есть в нем и горечь, и сладость, и травяная терпкость, и домашнее, деревянное тепло шоколада' \
                   ' и перца, и что-то еще; темное, как будто глядящее из самой глубины солодовой души'

    example_text = re.sub("[^а-я, .\n]", "", example_text)

    start_index = random.randint(0, len(example_text) - MAXLEN - 1)
    for T in temperatures:
        print("Do----------Temperature", T)
        generated = ''
        sentence = example_text[start_index:start_index + MAXLEN]
        generated += sentence
        print("Generating with seed: " + sentence)
        print('')

        for i in range(300):
            char_to_int = dict((c, i) for i, c in enumerate(chars))
            int_to_char = dict((i, c) for i, c in enumerate(chars))

            seed = np.zeros((BATCH_SIZE, MAXLEN, len(chars)))
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


def get_sample_mega(model, temperatures):  # [0.2, 0.5, 1.0]
    # global params
    MAXLEN = 30
    STEP = 1
    BATCH_SIZE = 350

    raw_text = open('data/mega_sample.txt', encoding="utf-8").read()
    raw_text = raw_text.lower()
    raw_text_ru = re.sub("[^а-я, .\n]", "", raw_text)
    chars = sorted(list(set(raw_text_ru)))

    example_text = 'белая плотная шапка пены, большое облако, зависшее над полем созревшей пшеницы, ' \
                   'один только вид такой красоты заставляет сердце биться чаще, прогоняя из головы дурные мысли. ' \
                   'но только попробовав на вкус, почувствовав, как льется свежесть спелой пшеницы сквозь казавшиеся ' \
                   'такими плотными облака пены, можно ощутить всю полноту вкуса, почувствовать спрятавшиеся среди ' \
                   'колосьев яблоки, уловить невесть откуда взявшийся оттенок сладкой выпечки, а в конце ' \
                   'горечь, легкая и даже приятная. ' \
                   'плотный как туман ранним осенним утром, подсвеченный встающим ' \
                   'солнцем и такой же освежающий, как тот туман, напиток, похожий своим видом на осень, на вкус ' \
                   'больше походит на лето — пшеничный, со спелыми яблоками и горчинкой, легкой, едва уловимой. ' \
                   'описать этот вкус коротко так же тяжело, как описать воздух ранним весенним утром, однако стоит ' \
                   'сделать один глоток, как перед глазами встает поле, бескрайнее и золотое, полное созревших ' \
                   'колосьев пшеницы, за которым начинается яблоневый сад, окружающий усадьбу. и все они: и пшеница, ' \
                   'и яблоки, и легкий аромат выпечки к чаю из дома в саду переплетаются, ненавязчиво, где-то далеко,' \
                   ' но след оставляют четкий и явственный.' \
                   'ни горечи, ни тяжести, ни намека на тот обычный напиток в этом вкусе не найти. ' \
                   'с первого глотка — только легкость и свежесть антоновки сделаешь глоток, и пиво расцветает, ' \
                   'словно хочет улететь на воздух. а потом, чуть запоздав, подходят и пшеничные ноты, ' \
                   'которые звучат где-то далеко, как соловей в чаще за горячим полем.' \
                   'вкус раскинулся шатром сочной золотой пшеницы и чем-то еще еле уловимым, небольшим, таинственным, ' \
                   'что может показаться пряным ароматом бутонов гвоздики или утренней выпечкой.' \
                   'плотное и мягкое тело напитка словно в беспамятстве расплескалось на дне бокала, ' \
                   'в попытках скрыться от жаркой сладости солода — так усталые путники пытаются укрыться ' \
                   'от полуденного зноя в жидкой тени. для разнообразия мелькнет в напитке игривая прохлада ' \
                   'ягод или василька, вырастет на мгновение смолистая хвоя или раскинется яблоня. а потом ' \
                   'опять польется знойная степная горечь, сначала резковатая, но с каждым глотком более мягкая, ' \
                   'ленивая, уходящая куда-то за горизонт в длительное послевкусие.' \
                   'пиво пахнет молодой травкой, ягодами, цветущим садом и чем-то этаким особенным, веселым, весенним.' \
                   ' вкус продолжает аромат, будто взял горсть красных и черных ягодок, растянулся под выбеленной ' \
                   'вишней, да съел неторопливо, запив прохладной водой.' \
                   'бывает такая горечь, которая даже не горечь, а сплошной надрыв, оголенный нерв. ' \
                   'а бывает напротив, крепкое, чрезвычайно даже наполненное, но так по-особенному приготовленное, ' \
                   'что оно не только не зажимает тебя в тиски, но даже в некотором роде освобождает тебя. ' \
                   'есть в нем и горечь, и сладость, и травяная терпкость, и домашнее, деревянное тепло шоколада' \
                   ' и перца, и что-то еще; темное, как будто глядящее из самой глубины солодовой души'

    example_text = re.sub("[^а-я, .\n]", "", example_text)

    start_index = random.randint(0, len(example_text) - MAXLEN - 1)
    for T in temperatures:
        print("Do----------Temperature", T)
        generated = ''
        sentence = example_text[start_index:start_index + MAXLEN]
        generated += sentence
        print("Generating with seed: " + sentence)
        print('')

        for i in range(300):
            char_to_int = dict((c, i) for i, c in enumerate(chars))
            int_to_char = dict((i, c) for i, c in enumerate(chars))

            seed = np.zeros((BATCH_SIZE, MAXLEN, len(chars)))
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

path = 'models_chehov/'
json_file = open(path + 'current_model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
trained_model_che = model_from_json(loaded_model_json)
trained_model_che.load_weights(path + 'weights_ep_23_loss_1.439_val_loss_1.570.hdf5')
trained_model_che.compile(loss='categorical_crossentropy', optimizer='rmsprop')

path = 'models_dostoevsky/'
json_file = open(path + 'current_model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
trained_model_do = model_from_json(loaded_model_json)
trained_model_do.load_weights(path + 'weights_ep_4_loss_1.397_val_loss_1.383.hdf5')
trained_model_do.compile(loss='categorical_crossentropy', optimizer='rmsprop')

path = 'models_dostoevsky/best_try/'
json_file = open(path + 'current_model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
trained_model_do2 = model_from_json(loaded_model_json)
trained_model_do2.load_weights(path + 'weights_ep_8_loss_1.185_val_loss_1.292.hdf5')
trained_model_do2.compile(loss='categorical_crossentropy', optimizer='rmsprop')

path = 'models_mega/'
json_file = open(path + 'current_model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
trained_model_mega = model_from_json(loaded_model_json)
trained_model_mega.load_weights(path + 'weights_ep_4_loss_1.273_val_loss_1.291.hdf5')
trained_model_mega.compile(loss='categorical_crossentropy', optimizer='rmsprop')

for i in range(1000):
    # get_sample_chehov(trained_model_che, [0.6, 0.7, 0.8])
    # get_sample_do(trained_model_do, [0.6, 0.7, 0.8])
    # get_sample_do2(trained_model_do2, [0.7, 0.8])
    get_sample_mega(trained_model_mega, [0.6, 0.7, 0.8])

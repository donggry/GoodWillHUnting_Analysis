import numpy as np
import random
import sys, math
import time
import pickle
from datetime import datetime

class Classifier:
    def __init__(self, featureGenerator):
        self.featureGenerator = featureGenerator
        self._C_SIZE = 0
        self._V_SIZE = 0
        self._classes_list = []
        self._classes_dict = {}
        self._vocab = {}

    def setClasses(self, trainingData):
        for (label, line) in trainingData:
            if label not in self._classes_dict.keys():
                self._classes_dict[label] = len(self._classes_list)
                self._classes_list.append(label)
        self._C_SIZE = len(self._classes_list)
        return

    def getClasses(self):
        return self._classes_list

    def setVocab(self, trainingData):
        index = 0;
        for (label, line) in trainingData:
            line = self.featureGenerator.getFeatures(line)
            for item in line:
                if (item not in self._vocab.keys()):
                    self._vocab[item] = index
                    index += 1
        self._V_SIZE = len(self._vocab)
        return

    def getVocab(self):
        return self._vocab

    def train(self, trainingData):
        pass

    def classify(self, testData, params):
        pass

    def getFeatures(self, data):
        return self.featureGenerator.getFeatures(data)

    def save_classifier(classifier):
        f = open('./../../model/model_3.pickle', 'wb')
        pickle.dump(classifier, f, -1)
        f.close()

class FeatureGenerator:
    def getFeatures(self, text):
        text = text.lower()
        return text.split()


class NaiveBayesClassifier(Classifier):
    def __init__(self, fg, alpha=0.05): # alpha 0.05 (default)
        Classifier.__init__(self, fg)
        self.__classParams = []
        self.__params = [[]]
        self.__alpha = alpha

    def getParameters(self):
        return (self.__classParams, self.__params)

    def train(self, trainingData):
        self.setClasses(trainingData)
        self.setVocab(trainingData)
        self.initParameters()
        lda = [[], [], [], [], [], [], [], [], [], [], []]
        for a, i in self._classes_dict.items():
            if ("Auto & Home Improvement" in a):
                lda[i] = ['car', 'tool', 'light', 'kit', 'air', 'mount', 'battery', 'device', 'vehicle', 'power',
                          'seat', 'portable', 'storage', 'wall', 'universal', 'help', 'floor', 'holder', 'fan', 'cable']

            elif('Entertainment' in a):
                lda[i] = ['dvd', 'melissa', 'doug', 'bluray', 'toy', 'baby', 'kid', 'trend', 'book', 'season', 'play',
                          'little', 'lab', 'bluraydvd', 'edition', 'girl', 'pack', 'game', 'collection', 'block']
            elif ("Men's Fashion" in a):
                lda[i] = ['tshirt', 'sock', 'backpack', 'cotton', 'men', 'short', 'funny', 'unisex', 'shirt', 'bag',
                          'sleeve', 'tee', 'canvas', 'casual', 'elite', 'custom', 'shoe' 'comfortable', 'classic',
                          'sweatshirt']
            elif ('Home & Garden' in a):
                lda[i] = ['table', 'chair', 'steel', 'design', 'sheet', 'glass', 'storage', 'cover', 'lamp', 'cotton',
                          'stainless', 'home', 'collection', 'rug', 'pet', 'food', 'piece', 'oz', 'patio', 'area']

            elif ("Women's Fashion" in a):
                lda[i] = ['woman', 'dress', 'sunglass', 'top', 'sandal', 'comfortable', 'lace', 'design', 'costume',
                          'heel', 'adult', 'bra', 'skirt', 'toe', 'casual', 'high', 'style', 'wedge', 'boot',
                          'platform']

            elif ("Jewelry & Watches" in a):
                lda[i] = ['gold', 'silver', 'white', 'sterling', 'diamond', 'necklace', 'earring', 'bracelet', 'round',
                          'pendant', 'watch', 'stud', 'ring', 'gemstone', 'genuine', 'black', 'carat', 'crystal',
                          'jewelry', 'steel']

            elif ('Baby, Kids & Toys' in a):
                lda[i] = ['dvd', 'melissa', 'doug', 'bluray', 'toy', 'baby', 'kid', 'trend', 'book', 'season', 'play',
                          'little', 'lab', 'bluraydvd', 'edition', 'girl', 'pack', 'game', 'collection', 'block']

            elif ('Health & Beauty' in a):
                lda[i] = ['oz', 'pack', 'hair', 'help', 'oil', 'brush', 'body', 'spray', 'skin', 'men', 'gel',
                          'support', 'cream', 'natural', 'makeup', 'supplement', 'unisex', 'nail', 'woman', 'kit']

            elif ('Sports & Outdoors' in a):
                lda[i] = ['team', 'bike', 'mlb', 'logo', 'inch', 'bicycle', 'double', 'sport', 'throw', 'light', 'play',
                          'fitness', 'golf', 'style', 'bag', 'knife', 'raschel', 'exercise ', 'lamp', 'tiffany']

            elif ('Grocery, Alcohol & Tobacco' in a):
                lda[i] = ['pack', 'oz', 'organic', 'tea', 'baby', 'food', 'ounce', 'count', 'bag', 'bar', 'coffee',
                           'fruit', 'apple', 'happy', 'chocolate', 'green', 'kraft', 'cereal', 'snack', 'butter']

            elif ('Electronics' in a):
                lda[7] = ['insten', 'case', 'screen', 'protector', 'usb', 'cable', 'iphone', 'galaxy', 'black',
                          'samsung', 'camera', 'charger', 'clear', 'apple', 'wireless', 'phone', 'speaker', 'pack',
                          'touch', 'ipad']
        tf_idf = [[], [], [], [], [], [], [], [], [], [], []]
        for a, i in self._classes_dict.items():
            if ("Auto & Home Improvement" in a):
                tf_idf[i] = ['outlet', 'holdback', 'puller', 'tool', 'zuo', 'vehicle', 'compressor', 'faucet', 'dent',
                             'mount', 'truck', 'desyne', 'gps', 'seat', 'windshield', 'crg', 'footage', 'ceil',
                             'dashboard', 'cam', 'trunk', 'battery', 'rainfall', 'motocross', 'tire']
            elif ('Entertainment' in a):
                tf_idf[i] = ['dvd', 'bluray', 'bluraydvd', 'bd', 'vol', 'documentary', 'comedy', 'season', 'frontline',
                             'anniversary', 'book', 'film', 'tale', 'story', 'edition', 'history', 'nintendo',
                             'complete', 'drama', 'nova', 'episode', 'crime', 'death', 'doctor', 'return']
            elif ("Men's Fashion" in a):
                tf_idf[i] = ['tshirt', 'funny', 'sock', 'pullover', 'compression', 'gildan', 'sweatshirt', 'unisex',
                             'backpack', 'crewneck', 'nla', 'sleeve', 'casual', 'tee', 'cotton', 'sweater', 'shirt',
                             'canvas', 'men', 'bag', 'vneck', 'short', 'custom', 'athletic', 'hoodie']
            elif ('Home & Garden' in a):
                tf_idf[i] = ['kitchenaid', 'crestview', 'import', 'cheungs', 'glade', 'glassescase', 'chair', 'rug',
                             'patio', 'lamp', 'duvet', 'ravenna', 'monarch', 'comforter', 'mod', 'zuo', 'curtain',
                             'sheet',
                             'crib', 'nonstick', 'superior', 'oz', 'ziploc', 'furniture', 'ink']
            elif ("Women's Fashion" in a):
                tf_idf[i] = ['skirt', 'costume', 'mlc', 'strappy', 'woman', 'sandal', 'bra', 'beston', 'sunglass',
                             'heel', 'eyewear', 'sakkas', 'riverberry', 'platform', 'ax', 'adult', 'bikini', 'dress',
                             'scarf',
                             'stiletto', 'racerback', 'toe', 'lace', 'wedge', 'casual']
            elif ("Jewelry & Watches" in a):
                tf_idf[i] = ['earring', 'carat', 'sterling', 'ctw', 'gemstone', 'cz', 'necklace', 'kidsgirls',
                             'tungsten', 'zirconia', 'bracelet', 'pendant', 'stud', 'cufflink', 'silver', 'coi', 'vs1',
                             'tcw',
                             'plated', 'cttw', 'cubic', 'topaz', 'bangle', 'watch', 'diamond']
            elif ('Baby, Kids & Toys' in a):
                tf_idf[i] = ['melissa', 'doug', 'brictek', 'diaper', 'laq', 'thames', 'tedcotoys', 'lab', 'trend',
                             'acorn', 'puddy', 'flashcard', 'toy', 'toddler', 'kidorable', 'drone', 'rc', 'vary',
                             'playset',
                             'ecr4kids', 'babyaspen', 'truck', 'maternity', 'stacker', 'sandtastik']
            elif ('Health & Beauty' in a):
                tf_idf[i] = ['oz', 'edt', 'vibrator', 'serum', 'supplement', 'makeup', 'vitamin', 'parker', 'hair',
                             'soap', 'spray', 'anal', 'eau', 'compression', 'oil', 'lotion', 'razor', 'brush', 'facial',
                             'fragrance', 'massager', 'shampoo', 'deodorant', 'treatment', 'herb']
            elif ('Sports & Outdoors' in a):
                tf_idf[i] = ['raschel', 'mlb', 'col', 'tiffany', 'bike', 'knife', 'throw', 'humminbird', 'nfl',
                             'handlebar', 'bicycle', 'voit', 'minn', 'cob', 'sherpa', 'lamp', 'reel', 'duffel', 'crg',
                             'kota', 'okuma', 'nba', 'logo', 'sweatshirt', 'bedrest']
            elif ('Grocery, Alcohol & Tobacco' in a):
                tf_idf[i] = ['oz', 'organic', 'quaker', 'tea', 'cereal', 'kraft', 'ounce', 'gerber', 'pack', 'granola',
                             'lipton', 'tazo', 'mccormick', 'roast', 'planter', 'flavor', 'oatmeal', 'macaroni',
                             'chocolate',
                             'cheddar', 'yogurt', 'happytot', 'butter', 'count', 'vaporizer']
            elif ('Electronics' in a):
                tf_idf[i] = ['insten', 'samsung', 'protector', 'iphone', 'ipad', 'ipod', 'hdmi', 'sony', 'refurb',
                             'headphone', 'playstation', 'adapter', 'speaker', 'stereo', 'audio', 'tpu', 'xbox', 'dell',
                             'controller', 'nintendo', 'antigrease', 'swann', 'zte', 'screen', 'htc']


        for (cat, document) in trainingData:
            for feature in self.getFeatures(document):
                self.countFeature(feature, cat, self._classes_dict[cat],lda,tf_idf)

    def countFeature(self, feature, cat, class_index,lda,tf_idf):
        counts = 1
        bool = 0
        bool2=0
        if (feature in lda[class_index]):
            bool = 1
        if(feature in tf_idf[class_index]):
            bool2=1
        self._counts_in_class[class_index][self._vocab[feature]] = self._counts_in_class[class_index][
                                                                       self._vocab[feature]] + counts
        if (bool == 1):
            self._counts_in_class[class_index][self._vocab[feature]] = self._counts_in_class[class_index][
                                                                           self._vocab[feature]] + 1
            bool = 0
        if (bool == 1):
            self._counts_in_class[class_index][self._vocab[feature]] = self._counts_in_class[class_index][
                                                                               self._vocab[feature]] + 1
            bool2 = 0

        print(feature)

        self._total_counts[class_index] = self._total_counts[class_index] + counts
        self._norm = self._norm + counts

    def classify(self, testData):
        post_prob = self.getPosteriorProbabilities(testData)
        return self._classes_list[self.getMaxIndex(post_prob)]

    def getPosteriorProbabilities(self, testData):
        post_prob = np.zeros(self._C_SIZE)
        for i in range(0, self._C_SIZE):
            for feature in self.getFeatures(testData):
                post_prob[i] += self.getLogProbability(feature, i)
            post_prob[i] += self.getClassLogProbability(i)
        return post_prob

    def getFeatures(self, testData):
        return self.featureGenerator.getFeatures(testData)

    def initParameters(self):
        self._total_counts = np.zeros(self._C_SIZE)
        self._counts_in_class = np.zeros((self._C_SIZE, self._V_SIZE))
        self._norm = 0.0

    def getLogProbability(self, feature, class_index):
        return math.log(self.smooth(self.getCount(feature, class_index), self._total_counts[class_index]))

    def getCount(self, feature, class_index):
        if feature not in self._vocab.keys():
            return 0
        else:
            return self._counts_in_class[class_index][self._vocab[feature]]

    def smooth(self, numerator, denominator):
        return (numerator + self.__alpha) / (denominator + (self.__alpha * len(self._vocab)))

    def getClassLogProbability(self, class_index):
        return math.log(self._total_counts[class_index] / self._norm)

    def getMaxIndex(self, posteriorProbabilities):
        maxi = 0
        maxProb = posteriorProbabilities[maxi]
        for i in range(0, self._C_SIZE):
            if (posteriorProbabilities[i] >= maxProb):
                maxProb = posteriorProbabilities[i]
                maxi = i
        return maxi


class Dataset:
    def __init__(self, filename, level, num_of_training_data):
        lines = open(filename, "r").read().split('\n')
        nutshell = ""
        category = ""
        self.__dataset = []
        before_dataset = []

        # add ny Hana (parsing input data and make before_dataset(not shuffle))
        for line in lines:
            id_nts_ctg = line.split('||')  # id || nutshell || category

            # nutshell
            if (id_nts_ctg.__len__() <= 2): continue  # constraint1

            nutshell = id_nts_ctg[1]  # nutshell = '~~~~~~'

            # add constraints by Hana (160722) : remove sentenses under 2 words
            nutshells = nutshell.split(' ')
            if (nutshells.__len__() <= 2): continue  # constraint2

            # category
            categories = id_nts_ctg[2].split(" > ")  # category = 1 > 2 > 3
            if (categories.__len__() <= 2): continue  # constraint3

            if (level == 1):
                category = categories[0]  # Level 1
            elif (level == 2):
                category = categories[0] + ' / ' + categories[1]  # Level 2
            else:
                category = categories[0] + ' / ' + categories[1] + ' / ' + categories[2]  # Level 3

            before_dataset.append([category, nutshell])

        random.shuffle(before_dataset)
        self.__dataset = before_dataset[0:num_of_training_data]
        self.__D_SIZE = num_of_training_data
        self.__trainSIZE = int(0.6 * self.__D_SIZE)
        self.__testSIZE = int(0.3 * self.__D_SIZE)
        self.__devSIZE = 1 - (self.__trainSIZE + self.__testSIZE)

    def setTrainSize(self, value):
        self.__trainSIZE = int(value * 0.01 * self.__D_SIZE)
        return self.__trainSIZE

    def setTestSize(self, value):
        self.__testSIZE = int(value * 0.01 * self.__D_SIZE)
        return self.__testSIZE

    def setDevelopmentSize(self):
        self.__devSIZE = int(1 - (self.__trainSIZE + self.__testSIZE))
        return self.__devSIZE

    def getDataSize(self):
        return self.__D_SIZE

    def getTrainingData(self):
        return self.__dataset[0:self.__trainSIZE]

    def getTestData(self):
        return self.__dataset[self.__trainSIZE:(self.__trainSIZE + self.__testSIZE)]

    def getDevData(self):
        return self.__dataset[0:self.__devSIZE]


# ============================================================================================

if __name__ == "__main__":

    level = int(raw_input('level (1-3) : '))
    ratio = str(raw_input('ratio of training:test (82, 73, 64, 55) : '))
    num_of_training_data = int(raw_input('number of training data : '))
    print('\n')

    infile = "./../../../data/160602.txt"
    #outfile = open("./../../output/160429_1.txt", 'w')
    outfile = open('test.txt', 'w')

    if len(sys.argv) > 1:
        filename = sys.argv[1]

    data = Dataset(infile, level, num_of_training_data)

    ratio_training = int(ratio[0] + '0')
    ratio_test = int(ratio[1] + '0')
    data.setTrainSize(ratio_training)
    data.setTestSize(ratio_test)

    train_set = data.getTrainingData()
    test_set = data.getTestData()

#    print(train_set[0:10])
#    print('\n')
#    print(test_set[0:10])
#    print('\n')

    test_data = [test_set[i][1] for i in range(len(test_set))]
    actual_labels = [test_set[i][0] for i in range(len(test_set))]

    fg = FeatureGenerator()
    alpha = 0.5  # smoothing parameter

    nbClassifier = NaiveBayesClassifier(fg, alpha)

    # training start
    now1 = datetime.now()
    nbClassifier.train(train_set)
    print(nbClassifier._classes_dict)
    now2 = datetime.now()
    # training end

    training_time = now2 - now1

    #nbClassifier.save_classifier(level, ratio, num_of_training_data)

    # accuracy test
    print('\n> test start ...\n')
    outfile.write('\n> test start ...\n')
    correct = 0
    total = 0

    eunsoo = np.zeros((11, 11))
    cat_dic = {}
    cat_dic['Auto & Home Improvement'] = 0
    cat_dic['Home & Garden'] = 1
    cat_dic["Men's Fashion"] = 2
    cat_dic['Electronics'] = 3
    cat_dic["Women's Fashion"] = 4
    cat_dic['Jewelry & Watches'] = 5
    cat_dic['Baby, Kids & Toys'] = 6
    cat_dic['Health & Beauty'] = 7
    cat_dic['Sports & Outdoors'] = 8
    cat_dic['Grocery, Alcohol & Tobacco'] = 9
    cat_dic['Entertainment'] = 10


    for line in test_data:
        best_label = nbClassifier.classify(line)
        #print(str(total) + '. ' + line + '\n\t' + best_label + ' =?= ' + actual_labels[total])
        #outfile.write('\n' + str(total) + '. ' + line + '\n\t' + best_label + ' =?= ' + actual_labels[total])
        if best_label == actual_labels[total]:
            correct += 1
            #print('O')
            #outfile.write(' -> O')
        else:
            #print('X')
            #outfile.write(' -> X')

            print(str(total) + '. ' + line + '\n\t' + best_label + ' =/= ' + actual_labels[total])
            outfile.write('\n' + str(total) + '. ' + line + '\n\t' + best_label + ' =/= ' + actual_labels[total])

            if ("Auto & Home Improvement" in actual_labels[total]):
                eunsoo[0][cat_dic[best_label]] += 1
            elif ('Home & Garden' in actual_labels[total]):
                eunsoo[1][cat_dic[best_label]] += 1
            elif ("Men's Fashion" in actual_labels[total]):
                eunsoo[2][cat_dic[best_label]] += 1
            elif ('Electronics' in actual_labels[total]):
                eunsoo[3][cat_dic[best_label]] += 1
            elif ("Women's Fashion" in actual_labels[total]):
                eunsoo[4][cat_dic[best_label]] += 1
            elif ("Jewelry & Watches" in actual_labels[total]):
                eunsoo[5][cat_dic[best_label]] += 1
            elif ('Baby, Kids & Toys' in actual_labels[total]):
                eunsoo[6][cat_dic[best_label]] += 1
            elif ('Health & Beauty' in actual_labels[total]):
                eunsoo[7][cat_dic[best_label]] += 1
            elif ('Sports & Outdoors' in actual_labels[total]):
                eunsoo[8][cat_dic[best_label]] += 1
            elif ('Grocery, Alcohol & Tobacco' in actual_labels[total]):
                eunsoo[9][cat_dic[best_label]] += 1
            elif ('Entertainment' in actual_labels[total]):
                eunsoo[10][cat_dic[best_label]] += 1

        total += 1

    acc = 1.0 * correct / total

    print('\n> test end ...\n')
    outfile.write('\n> test end ...\n')
    print('=' * 60)
    outfile.write('=' * 60)
    print(' RESULT')
    outfile.write(' RESULT')
    print('=' * 60)
    outfile.write('=' * 60)
    print(' - Level : ' + str(level))
    outfile.write('\n - Level : ' + str(level))
    print(' - Ratio of training:test : ' + str(ratio_training) + ':' + str(ratio_test))
    outfile.write('\n - Ratio of training:test : ' + str(ratio_training) + ':' + str(ratio_test))
    print(' - Amount of data : ' + str(num_of_training_data))
    outfile.write('\n - Amount of data : ' + str(num_of_training_data))
    temp1 = ' - Training time : %d' % training_time.total_seconds()
    print(temp1)
    outfile.write('\n' + temp1)
    temp2 = ' - Accuracy : %0.3f' % acc
    print(temp2)
    outfile.write('\n' + temp2)
    print(' - Amount of Category : ' + str(nbClassifier.getClasses().__len__()))
    outfile.write('\n - Amount of Category : ' + str(nbClassifier.getClasses().__len__()))
    print('=' * 60)
    outfile.write('=' * 60)

    print(nbClassifier._classes_dict)
    print(eunsoo)
    outfile.write(eunsoo)

    outfile.close()










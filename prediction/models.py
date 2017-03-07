from __future__ import unicode_literals

from django.db import models

import math
import json
import numpy as np
from tabulate import tabulate

import sys
sys.path.append('illustration2vec')
import i2v

class Classifier:
    characters = json.load(open('characters.json'))
    tags = json.load(open('general_tags.json'))
    weights = np.load('weights.npy')
    illust2vec = i2v.make_i2v_with_chainer('illustration2vec/illust2vec_tag_ver200.caffemodel',
            'illustration2vec/tag_list.json')

    @classmethod
    def num_characters(self):
        return len(self.characters)

    @classmethod
    def num_tags(self):
        return len(self.tags)

    @classmethod
    def predict(self, img):
        predictions = self.illust2vec.estimate_specific_tags([img], self.tags)[0]

        scores = np.ndarray(len(self.tags), np.float32)
        for (i, g) in enumerate(self.tags):
            scores[i] = predictions[g]
        log_prob = np.dot(self.weights, scores)

        pred = list(reversed(sorted(zip(log_prob, self.characters))))

        print('odds: %f' % (math.exp(pred[0][0] - pred[1][0])))
        print(tabulate(pred[:20], headers=['Score', 'Character']))

        return [c for (p, c) in pred]

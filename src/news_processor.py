import os
import string

from src.city import City


class NewsProcessor:
    def __init__(self, pos_path=os.path.join(os.path.dirname(os.getcwd()), 'res', 'word', 'positive.txt'),
                 neg_path=os.path.join(os.path.dirname(os.getcwd()), 'res', 'word', 'negative.txt'),
                 stop_path=os.path.join(os.path.dirname(os.getcwd()), 'res', 'word', 'stopword.txt')):
        self.pos_words = self.remove_weird_char(
            list(map(str.strip, open(pos_path, 'r', errors='ignore').read().strip().split(','))))
        self.neg_words = self.remove_weird_char(
            list(map(str.strip, open(neg_path, 'r', errors='ignore').read().strip().split(','))))
        self.stop_words = self.remove_weird_char(
            list(map(str.strip, open(stop_path, 'r', errors='ignore').read().strip().split(','))))

    def count_words(self, text_path, rm_stopwords=True):
        def count(path):
            words = self.remove_weird_char(
                list(map(str.strip, open(path, 'r', errors='ignore').read().strip().lower().translate(
                    str.maketrans('', '', string.punctuation)).split())))
            if rm_stopwords:
                words, stops = self.filter_stop(words)
                return dict(zip(words, [words.count(p) for p in words])), dict(
                    zip(stops, [stops.count(p) for p in stops]))
            return dict(zip(words, [words.count(p) for p in words]))

        if os.path.isdir(text_path):
            words, stops = [], []
            for file in os.listdir(text_path):
                if file.endswith('.txt'):
                    w, s = count(os.path.join(text_path, file))
                    words.append(w)
                    stops.append(s)
            return words, stops
        else:
            return count(text_path)

    def remove_weird_char(self, word_list):
        def only_ascii(char):
            if ord(char) < 48 or ord(char) > 127:
                return ''
            else:
                return char

        return [''.join(list(map(only_ascii, w))) for w in word_list]

    def count_dicts(self, word_dicts):
        return sum([sum(word_dict.values()) for word_dict in word_dicts])

    def combine_dicts(self, word_dicts):
        aux = {}
        for word_dict in word_dicts:
            for k, v in word_dict.items():
                if k in aux:
                    aux[k] += v
                else:
                    aux[k] = v
        return aux

    def filter_stop(self, words):
        word, stop = [], []
        stop_words = ' '.join(self.stop_words)
        [(word, stop)[self.rabin_karp(w, stop_words)].append(w) for w in words]
        return word, stop

    def rabin_karp(self, pattern, text, d=256, q=101):
        M = len(pattern)
        N = len(text)
        p = 0
        t = 0
        h = pow(d, M - 1) % q
        for i in range(M):
            p = (d * p + ord(pattern[i])) % q
            t = (d * t + ord(text[i])) % q
        for j in range(N - M):
            if p == t:
                match = True
                for i in range(M):
                    if pattern[i] != text[j + i]:
                        match = False
                        break
                if match:
                    return True
            if j < N - M:
                t = (t - h * ord(text[j])) % q
                t = (t * d + ord(text[j + M])) % q
                t = (t + q) % q
        return False

    def filter_pos(self, word_dict):
        return {k: v for k, v in word_dict.items() if k in self.pos_words}

    def filter_neg(self, word_dict):
        return {k: v for k, v in word_dict.items() if k in self.neg_words}

    def filter_neutral(self, word_dict):
        return {k: v for k, v in {k: v for k, v in word_dict.items() if k not in self.pos_words}.items() if
                k not in self.neg_words}

    def process_all(self, city_dict, res_dir=os.path.join('..', 'res')):
        for c in [line.split(':')[0].strip() for line in
                  open(os.path.join(res_dir, 'airport code references.txt'), 'r').read().strip().split('\n')]:
            city_dict[c].news_dicts, city_dict[c].stop_dicts = self.count_words(os.path.join(res_dir, 'news', c))
            city_dict[c].pos_dicts = [self.filter_pos(news_dict) for news_dict in city_dict[c].news_dicts]
            city_dict[c].neg_dicts = [self.filter_neg(news_dict) for news_dict in city_dict[c].news_dicts]
            city_dict[c].neu_dicts = [self.filter_neutral(news_dict) for news_dict in city_dict[c].news_dicts]
            city_dict[c].pol_senti = self.count_dicts(city_dict[c].pos_dicts) - self.count_dicts(city_dict[c].neg_dicts)
        return city_dict


if __name__ == '__main__':
    news_processor = NewsProcessor()
    print(news_processor.neg_words)
    print(news_processor.pos_words)
    print(news_processor.stop_words)
    news_dicts, stop_dicts = news_processor.count_words(os.path.join(os.path.dirname(os.getcwd()), 'res', 'news', 'ATL'))
    print()
    [print(d) for d in news_dicts]
    [print(d) for d in stop_dicts]
    print()
    print(news_processor.combine_dicts(stop_dicts))
    neg = [news_processor.filter_neg(news_dict) for news_dict in news_dicts]
    print()
    [print(d) for d in neg]
    pos = [news_processor.filter_pos(news_dict) for news_dict in news_dicts]
    print()
    [print(d) for d in pos]
    neutral = [news_processor.filter_neutral(news_dict) for news_dict in news_dicts]
    print()
    [print(d) for d in neutral]
    print()
    # full code
    ref_code = os.path.join('..', 'res', 'airport code references.txt')
    city_ref = dict(
        (line.split(':')[0].strip(), City(line.split(':')[0].strip(), line.split(':')[1].strip())) for line in
        open(ref_code, 'r').read().strip().split('\n'))
    news_processor.process_all(city_ref)
    [print(v) for c, v in city_ref.items()]

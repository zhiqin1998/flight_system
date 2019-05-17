import os
import string


class NewsProcessor:
    def __init__(self, pos_path=os.path.join('..', 'res', 'word', 'positive.txt'),
                 neg_path=os.path.join('..', 'res', 'word', 'negative.txt'),
                 stop_path=os.path.join('..', 'res', 'word', 'stopword.txt')):
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
                words = [w for w in words if w not in self.stop_words]
            return dict(zip(words, [words.count(p) for p in words]))

        if os.path.isdir(text_path):
            ans = []
            for file in os.listdir(text_path):
                if file.endswith('.txt'):
                    ans.append(count(os.path.join(text_path, file)))
            return ans
        else:
            return count(text_path)

    def remove_weird_char(self, word_list):
        def only_ascii(char):
            if ord(char) < 48 or ord(char) > 127:
                return ''
            else:
                return char

        return [''.join(list(map(only_ascii, w))) for w in word_list]

    def filter_pos(self, word_dict):
        return {k: v for k, v in word_dict.items() if k in self.pos_words}

    def filter_neg(self, word_dict):
        return {k: v for k, v in word_dict.items() if k in self.neg_words}

    def filter_neutral(self, word_dict):
        return {k: v for k, v in {k: v for k, v in word_dict.items() if k not in self.pos_words}.items() if
                k not in self.neg_words}


if __name__ == '__main__':
    news_processor = NewsProcessor()
    print(news_processor.neg_words)
    print(news_processor.pos_words)
    print(news_processor.stop_words)
    news_dicts = news_processor.count_words(os.path.join('..', 'res', 'news', 'ATL'))
    print()
    [print(d) for d in news_dicts]
    neg = [news_processor.filter_neg(news_dict) for news_dict in news_dicts]
    print()
    [print(d) for d in neg]
    pos = [news_processor.filter_pos(news_dict) for news_dict in news_dicts]
    print()
    [print(d) for d in pos]
    neutral = [news_processor.filter_neutral(news_dict) for news_dict in news_dicts]
    print()
    [print(d) for d in neutral]

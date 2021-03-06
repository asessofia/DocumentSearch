import datetime
import os
import ntpath
import re
from collections import Counter
import random


class SearchFile:

    def __init__(self, input_dir: str, search_method: str, token: str, pattern: str = None,
                 preprocessed_data: dict = None):
        self.input_dir = input_dir
        self.search_method = search_method
        self.token = token
        self.pattern = pattern
        self.preprocessed_data = preprocessed_data

    def simple_search(self):
        """
        This method will search user given token in file and count is using the count method of string.
        First file's content is read as string and then the occurrences of user given work is counter in the string.
        """
        print("\n\nResult of simple search with token: {}".format(self.token))
        for file in self.file_generator():
            with open(file) as f:
                data = f.read()
                occurrences = data.count(self.token)
                print("{}: {}".format(ntpath.basename(file), occurrences))

    def search_really_large_files(self, start=0):
        """
        Instead of reading the whole file at once in memory this method reads the file in chunks of bytes.
        How many bytes to read at once is define by bsize variable. Increasing bsize will increase the performance of this method.
        """
        print("\n\nResult of searching really large files by reading in chunks with token: {}".format(self.token))
        for file in self.file_generator():
            with open(file, 'rb') as f:
                file_size = os.path.getsize(file)
                bsize = 4096
                if start > 0:
                    f.seek(start)
                overlap = len(str.encode(self.token)) - 1
                occurrences = 0
                while True:
                    if overlap <= f.tell() < file_size:
                        f.seek(f.tell() - overlap)
                    buffer = f.read(bsize)
                    if buffer:
                        pos = buffer.find(str.encode(self.token))
                        if pos >= 0:
                            occurrences += buffer.decode().count(self.token)
                    else:
                        break
            print("{}: {}".format(ntpath.basename(file), occurrences))

    def search_regex(self):
        """
        This method matches a regex against the file and prints the number of matches.
        :return: None
        """
        if self.pattern:
            print("\n\nResult of searching all the words that match a regex with pattern: {}".format(self.pattern))
            reg = re.compile(self.pattern)
            for file in self.file_generator():
                with open(file) as f:
                    matches = sum(len(reg.findall(line)) for line in f)

                    print("{}: {}".format(ntpath.basename(file), matches))
        else:
            print("\n\nNo pattern to match")

    def search_preprocessed_data(self):
        """
        This will fetch the count of words from already prepared and preprocessed data.
        This data is generated by method "preprocess"
        """
        print("\n\nResult of searching pre-processed data with token: {}".format(self.token))
        for file in self.file_generator():
            occurrence = self.preprocessed_data[ntpath.basename(file)].get(self.token)
            occurrence = occurrence if occurrence else 0
            print("{}: {}".format(file, occurrence))

    def file_generator(self):
        """
        This is a simple generator used to get path of all files in input_dir. 
        """
        for root, sub_dir, files in os.walk(self.input_dir):
            for file in files:
                yield os.path.join(root, file)

    def make_search(self):
        """
        Calls one of the method described above as per the user choice.
        :return: None
        """
        if self.search_method == 'simple search':
            self.simple_search()
        elif self.search_method == 'regex search':
            self.search_regex()
        elif self.search_method == 'preprocessed search':
            self.search_preprocessed_data()
        elif self.search_method == 'large files':
            self.search_really_large_files()


def preprocess(input_dir):
    """
    This method is used to preprocess the data for indexing purpose before user makes the search.
    """
    file_dict = {}
    for root, sub_dir, files in os.walk(input_dir):
        for file in files:
            word_frequency = Counter()
            with open(os.path.join(root, file)) as f:
                for line in f:
                    word_frequency += Counter(re.sub('[^a-zA-Z0-9 \n\.]', ' ', line).split())
            file_dict[ntpath.basename(file)] = dict(word_frequency)
    return file_dict


def two_million_test(preprocessed_data):
    word_list = []
    for root, sub_dir, files in os.walk('sample_text'):
        for file in files:
            with open(os.path.join(root, file)) as f:
                word_list += re.sub('[^a-zA-Z0-9 \n\.]', ' ', f.read()).split()
    for _ in range(1000000):
        current_method = random.choice(search_methods)
        search_obj = SearchFile('sample_text', current_method, random.choice(word_list), '\w{1,4}',
                                preprocessed_data=preprocessed_data)
        now = datetime.datetime.now()
        search_obj.make_search()
        time_dict[current_method] += datetime.datetime.now() - now
        method_execution_count[current_method] += 1
    print("\n\nAverage time taken in seconds for each method")
    for key, value in time_dict.items():
        print("{}: executed {} times in {} seconds".format(key, method_execution_count[key], value.seconds))


if __name__ == '__main__':
    search_methods = ['simple search', 'regex search', 'preprocessed search', 'large files']
    time_dict = {
        'simple search': datetime.timedelta(0),
        'regex search': datetime.timedelta(0),
        'preprocessed search': datetime.timedelta(0),
        'large files': datetime.timedelta(0)
    }
    method_execution_count = {
        'simple search': 0,
        'regex search': 0,
        'preprocessed search': 0,
        'large files': 0
    }

    preprocessed_data = preprocess('sample_text')

    two_million_test(preprocessed_data)

    #search_object = SearchFile(input_dir='sample_text', search_method=search_methods[0], token='', pattern='',
    #                           preprocessed_data=preprocessed_data)

    # print("Please choose a method you want to use for searching.")

    # print("1) Simple search")
    # print("2) Regex search")
    # print("3) Preprocessed search")
    # print("4) Large Files")

    # choice = input("Enter your choice: ")

    # if choice == '1':
    #     tokens = input("Please enter space separated words to find in files: ")
    #     for token in tokens.split(' '):
    #         search_object.token = " {} ".format(token)
    #         search_object.search_method = search_methods[0]
    #         search_object.make_search()

    # elif choice == '2':
    #     patterns = input("Please enter space separated regex to find in files: ")
    #     for pattern in patterns.split(' '):
    #         search_object.pattern = pattern
    #         search_object.search_method = search_methods[1]
    #         search_object.make_search()

    # elif choice == '3':
    #     tokens = input("Please enter space separated words to find in files: ")
    #     for token in tokens.split(' '):
    #         search_object.token = token
    #         search_object.search_method = search_methods[2]
    #         search_object.make_search()

    # elif choice == '4':
    #     tokens = input("Please enter space separated words to find in files: ")
    #     for token in tokens.split(' '):
    #         search_object.token = " {} ".format(token)
    #         search_object.search_method = search_methods[3]
    #         search_object.make_search()

    # else:
    #     print("Please enter a valid choice from 1 to 4")

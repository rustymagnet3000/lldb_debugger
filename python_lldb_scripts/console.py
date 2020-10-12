#!/usr/bin/python

class Console:
    def __init__(self):
        pass

    @staticmethod
    def single_value(arg1):
        print('[+]' + str(arg1))

    @staticmethod
    def single_value_subheading(arg1):
        print('\t' + str(arg1))

    @staticmethod
    def single_label_and_value(arg0, arg1):
        print('\t' + arg0 + ': ' + arg1)

    @staticmethod
    def banner(arg1):
        print('\n[-]' + ('*' * 10) + ' ' + arg1 + ' ' + ('*' * 10) + '[-]')

    @staticmethod
    def single_list(arg1):
        print(arg1)
        for i in arg1:
            print('[+]' + i)

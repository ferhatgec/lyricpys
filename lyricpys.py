# MIT License
#
# Copyright (c) 2021 Ferhat Geçdoğan All Rights Reserved.
# Distributed under the terms of the MIT License.
#
# lyricpys - song lyrics engine interpreter (implementation of lyricpps)
# -----------------------------------------
# lyricpys uses tree to store datas instead of plain-text parsing.
#
# github.com/ferhatgec/lyricpys
# github.com/ferhatgec/lyricpps
#
# an example:
#
# from: 0.0 to: 0.19 {(
#    A rat bit my sister Nell%
#    With Whitey on the moon%
#    Her face and arms began to swell%
#    And Whitey's on the moon
#  )}
#
# from: 0.20 to: 0.33 {(
#     I can't pay no doctor bills%
#     But Whitey's on the moon%
#     Ten years from now%
#     I'll be payin' still%
#     While Whitey's on the moon%
#     You know the man%
#     Just upped my rent last night%
#     Whitey's on the moon%
# )}
#
# from: 0.34 to: 0.49 {(
#     No hot water, no toilets, no lights%
#     But Whitey's on the moon%
#     I wonder why he's uppin' me?%
#     'Cause Whitey's on the moon%
#     I was already givin' him like 50 a week%
#     Whitey's on the moon
# )}
#
# from: 0.50 to: 1.04 {(
#     Taxes takin' my whole damn check%
#     Junkies makin' me a nervous wreck%
#     The price of food is goin' up%
#     And if all that crap wasn't enough%
#     A rat bit my sister Nell%
#     With Whitey on the moon
# )}
#
# from: 1.05 to: 1.47 {(
#     Her face and arms began to swell%
#     And Whitey's on the moon%
#     Was all that money I made last year%
#     For Whitey on the moon?%
#     How come I ain't got no money here?%
#     Hmm, Whitey on the moon%
#     You know I just 'bout had my fill%
#     Of Whitey on the moon%
#     I think I'll send these doctor bills%
#     Airmail special%
#     To Whitey on the moon
# )}

from enum import IntEnum
from typing import List


class LyricPyTokens(IntEnum):
    Undef = -1
    From = 0
    To = 1
    Data = 2
    End = 3


class LyriPysTree:
    class LyriPysChild:
        def __init__(self):
            self.child = None
            self.token = LyricPyTokens
            self.val = ''
            self.start = 0.0
            self.end = 0.0

    def __init__(self):
        self.child: List[LyriPysTree.LyriPysChild] = []
        self.token = LyricPyTokens
        self.val = ''
        self.start = 0.0
        self.end = 0.0


class LyriPys:
    def __init__(self):
        self.init: List[LyriPysTree] = []
        self.list = [
            'from:',
            'to:',
            '{(',
            ')}'
        ]

    def match(self, data: str) -> LyricPyTokens:
        for i in range(0, len(self.list)):
            if self.list[i] == data:
                return LyricPyTokens(i)

        return LyricPyTokens.Undef

    def parse(self, __data: str):
        tok = []
        current, data = '', ''
        __type = LyricPyTokens.Undef

        for current in __data.split():
            if current == '\n':
                continue

            if len(self.init) - 1 > 0:
                last = self.get()

                if last == LyricPyTokens.From:
                    self.init[len(self.init) - 1].start = float(current)
                    self.init[len(self.init) - 1].token = LyricPyTokens.Undef
                elif last == LyricPyTokens.To:
                    self.init[len(self.init) - 1].end = float(current)
                    self.init[len(self.init) - 1].token = LyricPyTokens.Undef
                elif last == LyricPyTokens.Data:
                    if not self.match(current) == LyricPyTokens.End:
                        data += current

                        if data.endswith('%'):
                            data = data[:-1]
                            data += '\n'
                        else:
                            data += ' '
                    else:
                        self.set_val(data)
                        data = ''
                elif last == LyricPyTokens.End:
                    print(data)

            if __type == LyricPyTokens.Data and self.match(current) != LyricPyTokens.End:
                continue

            __type = self.match(current)

            if __type == LyricPyTokens.From:
                val = LyriPysTree()
                val.token = __type
                self.init.append(val)
            elif __type == LyricPyTokens.To:
                self.set_tok(__type)
            elif __type == LyricPyTokens.Data:
                self.set_tok(__type)
            elif __type == LyricPyTokens.End:
                pass

        self.init.remove(self.init[0])

    def get(self):
        __len = len(self.init) - 1

        if __len > 0:
            return self.init[__len].token

        return LyricPyTokens.Undef

    def set_tok(self, __type):
        __len = len(self.init) - 1

        if __len > 0:
            self.init[__len].token = __type
        else:
            val = LyriPysTree()
            val.token = __type

            self.init.append(val)

    def set_val(self, __data):
        __len = len(self.init) - 1

        if __len > 0:
            self.init[__len].val = __data

    def visit(self):
        if len(self.init) > 0:
            last = self.init[len(self.init) - 1]
            for val in self.init:
                print(end=f'start: {val.start}\nend: {val.end}\ndata: {val.val}')
                if val.start != last.start and val.end != last.end:
                    print(end=f'\n---\n')

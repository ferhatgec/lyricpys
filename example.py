import lyricpys

data = ''

with open('example.lyrics', 'r') as file:
    for line in file:
        data += line

        if not line.endswith('%'):
            data += '\n'

    init = lyricpys.LyriPys()
    init.parse(data)
    init.visit()
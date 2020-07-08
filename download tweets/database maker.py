import csv
import os.path
from itertools import cycle

users = [line.rstrip('\n') for line in open('input.txt')]  # every new line is a new user as contained in input.txt
final = {}  # a dictionary used to contain the source, target, and weight columns
input_file = 'data.csv'  # the name of the output file

with open(input_file, 'w') as out:  # python authorized to create a new file

    for user in users:  # every new line in users (from input.txt) is declared here as a 'user'

        if os.path.exists("files/" + user + ".csv"):  # if the file exists, no change

            user = user

        else:  # if the file does not exist (usually because the user does not exist)

            print(user)  # output the missing user
            li_users = cycle(users)  # use an iteration library to set up for going to the next user
            user = next(li_users)  # go to the next user, i.e. skip the current one
        print(user)
        with open(('files/' + user + '.csv'), newline='') as userFile:  # go to the raw file for the user

            writer = csv.writer(out)  # initialize a writer

            for row in userFile:  # look through every row

                if '@' in row:  # if the row names a user (will be used for target column)
                    print("yay")
                    listUser = row.split(' ')  # make list containing every word separately - can isolate target user @
                    for x in listUser:  # for every element in the list / every word in each tweet

                        if len(x) > 1 and '@' in x and '\\' not in x:  # if it is a valid username
                            x = x[x.index("@"):(len(x))]

                            # ^ set minimum length, first character @, no backslash

                            y = x  # initialize a new value that stores the name

                            for i in range(30):  # remove all the following characters and repeat 30 times

                                # twitter names cannot contain these characters
                                # the repeat is because some users use many, many commas in succession like ,,,,,

                                y = y.replace('"', '')
                                y = y.replace("'", '')
                                y = y.replace('@', '')
                                y = y.replace(':', '')
                                y = y.replace(',', '')
                                y = y.replace('!', '')
                                y = y.replace('$', '')
                                y = y.replace('%', '')
                                y = y.replace('^', '')
                                y = y.replace('&', '')
                                y = y.replace('*', '')
                                y = y.replace('(', '')
                                y = y.replace('.', '')
                                y = y.replace(')', '')
                                y = y.replace('-', '')
                                y = y.replace('=', '')
                                y = y.replace('+', '')
                                y = y.replace('{', '')
                                y = y.replace('}', '')
                                y = y.replace('[', '')
                                y = y.replace(']', '')
                                y = y.replace('|', '')
                                y = y.replace('\\', '')
                                y = y.replace(';', '')
                                y = y.replace('?', '')
                                y = y.replace('/', '')
                                y = y.replace('<', '')
                                y = y.replace('>', '')
                                y = y.replace('`', '')
                                y = y.replace('~', '')

                            y = y.lower()  # set to lowercase
                            y = y.replace('\r', '')  # a strange phenomenon that causes a line break: remove \r

                            if (user + ' ' + y) in final:  # if this string is in the dictionary

                                final[str(user + ' ' + y)] += 1  # increase weight of user naming target

                            else:  # if the string is not in the dictionary

                                final[str(user + ' ' + y)] = 1  # add string to dictionary with weight as value

                if '#' in row:  # if tag contained somewhere
                    listHash = row.split(' ')  # make list containing every word separately - can isolate target tag #

                    for z in listHash:  # for every element in the list / every word in each tweet

                        if len(z) > 1 and '#' in z and '\\' not in z and not (z[1].isdigit()):  # valid tag

                            # ^ set minimum length, first character #, no backslash, actual tag cannot start with number
                            z = z[z.index("#"):(len(z))]
                            for i in range(30):  # remove all the following characters and repeat 30 times

                                # twitter tags cannot contain these characters
                                # the repeat is because some users use many, many commas in succession like ,,,,,

                                z = z.replace('"', '')
                                z = z.replace("'", '')
                                z = z.replace('@', '')
                                z = z.replace(':', '')
                                z = z.replace(',', '')
                                z = z.replace('!', '')
                                z = z.replace('$', '')
                                z = z.replace('%', '')
                                z = z.replace('^', '')
                                z = z.replace('&', '')
                                z = z.replace('*', '')
                                z = z.replace('(', '')
                                z = z.replace('.', '')
                                z = z.replace(')', '')
                                z = z.replace('"', '')
                                z = z.replace("'", '')
                                z = z.replace('-', '')
                                z = z.replace('=', '')
                                z = z.replace('+', '')
                                z = z.replace('{', '')
                                z = z.replace('}', '')
                                z = z.replace('[', '')
                                z = z.replace(']', '')
                                z = z.replace('|', '')
                                z = z.replace('\\', '')
                                z = z.replace(';', '')
                                z = z.replace('?', '')
                                z = z.replace('/', '')
                                z = z.replace('<', '')
                                z = z.replace('>', '')
                                z = z.replace('`', '')
                                z = z.replace('~', '')

                            z = z.lower()  # set to lowercase

                            z = z.replace('\r', '')  # a strange phenomenon that causes a line break: remove \r

                            if (user + ' ' + z) in final:  # if this string is in the dictionary

                                final[str(user + ' ' + z)] += 1  # increase weight of user naming target

                            else:  # if the string is not in the dictionary

                                final[str(user + ' ' + z)] = 1  # add string to dictionary with weight as value

    for key, value in final.items():  # after all users have been classified

        listZ = str(key).split(' ')  # split the string "user + (space) + target" into [user], [target]

        writer.writerow([listZ[0]] + [listZ[1]] + [value])  # output the dictionary columns to the new file
    

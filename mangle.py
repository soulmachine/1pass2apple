import csv
import json
import sys

if len(sys.argv) < 2:
    print("missing 1pass export filename")
    exit(1)

filename = sys.argv[1]
w = csv.writer(sys.stdout)
w.writerow(['Title', 'URL', 'Username', 'Password', 'Notes', 'OTPAuth'])

with open(filename, 'r') as file:
    for line in file:
        if not line.startswith("{"):
            continue

        data = json.loads(line)
        title = data['title']
        username = ''
        password = ''
        otpauth = ''
        note = ''
        url = ''
        
        if 'typeName' in data:
            if data['typeName'] == 'system.folder.Regular':
                sys.stderr.write("[{}] skipping folder\n".format(title))
                continue                

        if 'trashed' in data:
            if data['trashed']:
                sys.stderr.write('[{}] skipping trash entry\n'.format(title))
                continue               

        if 'URLs' in data['secureContents']:
            # just use the first URL we found
            url = data['secureContents']['URLs'][0]['url']

        # try this password field first but use the one in data['secureContents']['fields'] if it exists later
        if 'password' in data['secureContents']:
            password = data['secureContents']['password']

        if 'fields' in data['secureContents']:
            for field in data['secureContents']['fields']:
                if field['name'] == 'Password' or field['name'] == 'password':
                    password = field['value']

                if field['name'] == 'Username' or field['name'] == 'username':
                    username = field['value']
                
                if field['name'] == 'Title' or field['name'] == 'title':
                    title = field['value']

        # if we still haven't found a password try designation
        if password == '':
            if 'fields' in data['secureContents']:
                for field in data['secureContents']['fields']:
                    if 'designation' in field:
                        if field['designation'] == 'password':
                            password = field['value']

        # if we still haven't found a username try designation
        if username == '':
            if 'fields' in data['secureContents']:
                for field in data['secureContents']['fields']:
                    if 'designation' in field:
                        if field['designation'] == 'username':
                            username = field['value']
        if not username:
            if 'notesPlain' in data['secureContents'] and data['typeName'] == 'securenotes.SecureNote':
                username = data['secureContents']['notesPlain']

        if 'sections' in  data['secureContents']:
            for section in data['secureContents']['sections']:
                if 'fields' in section:
                    for field in section['fields']:
                        if field['t'] == 'one-time password':
                            otpauth = field['v']
                            break

        # if note is still empty try to grab other possible entries
        # this might work for typeName's like wallet.government.SsnUS or others
        if note == '':
            if 'name' in data['secureContents']:
                note = f"name: {data['secureContents']['name']}\n\n"
        
            if 'number' in data['secureContents']:
                note += f"number: {note,data['secureContents']['number']}\n\n"

        if data['typeName'] == 'securenotes.SecureNote':
            if 'sections' in  data['secureContents']:
                for section in data['secureContents']['sections']:
                    if section['title'] != '' and 'fields' in section:
                        note += f"{section['title']}:\n"
                        for field in section['fields']:
                            if field['t'] and field['k'] == 'string':
                                note += f"{field['t']}: {field['v']}\n"
        w.writerow([title, url, username, password, note, otpauth])
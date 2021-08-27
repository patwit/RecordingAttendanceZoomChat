from os import write

zfile = 'participants_Jul_20.csv'
cfile = 'meeting_saved_chat_Jul_20.txt'
nfile = 'NameList.csv'

zoom_file = open('zoom/' + zfile)
chat_file = open('zoom/' + cfile)
name_file = open('zoom/' + nfile)

zfile = zfile[0:zfile.find('.')] + '_out.csv'
cfile = cfile[0:cfile.find('.')] + '_out.txt'
nfile = nfile[0:nfile.find('.')] + '_out.csv'

print(zfile)
print(cfile)
print(nfile)

zoom_file_out = open('zoom/' + zfile,'w')
chat_file_out = open('zoom/' + cfile,'w')
name_file_out = open('zoom/' + nfile,'w')


# Get name and id number from zoom chat in class
zoom_dict = dict()
name_list = []
email_list = []
n = 0
for s in zoom_file:
    #The first 4 lines are not the participants
    if n < 4:
        n = n+1
        continue
    s = s.strip()


    #print(s)
    if '(' in s:
        i = s.find('(')
        #print('i=',i)
        if s.startswith('\'') :
            name = s[1:i-1]
        else :
            name = s[0:i-1]
        i = s.find(',')
        i2 = s.find(',',i+1)
        email  = s[i+1:i2]
        #print('name =',name,'email =',email)
        zoom_dict[email] = name
    else :
        i = s.find(',',1)
        #print('i == ',i)
        name = s[1:i]
        i2 = s.find(',',i+1)
        #print(i2)
        email = s[i+1:i2]
        #print('name =', name, ' email =', email)
        zoom_dict[email] = name
    #print('name =', name, ' email =', email)
    name_list.append(name)
    email_list.append(email)
#print(name_list)
#print(email_list)

#print('Participants List')
zoom_record = dict(zip(email_list,name_list))
#print(zoom_dict)
print('Zoom record')
#print(zoom_record)
for i in zoom_record :
    print(i, zoom_record[i])

# 0 - not check in yet
# 1 - checking in
# 2 - Late
# 3 - checking out
check_in = 0
check_in_list = []
check_late_list = []
check_out_list = []
name_chat = []
id_chat = []
for s in chat_file:
    s = s.strip()
    s = s.lower()
    #print(s)

    if 'check in' in s :
        check_in = 1
        continue
    elif 'late' in s :
        check_in = 2
        continue
    elif 'check out' in s:
        check_in = 3
        continue

    if '613' in s or '623' in s or '633' in s :
        if check_in == 1 : #check in
            i = s.find('from')
            #print(i)
            i2 = s.find(':', i)
            id_num = s[i2+2:]
            #print(id_num)
            check_in_list.append(id_num)
            id_chat.append(id_num)
        elif check_in == 2 : #late
            i = s.find('from')
            i2 = s.find(':', i)
            id_num = s[i2+2:]
            #print(id_num)
            check_late_list.append(id_num)
            id_chat.append(id_num)
        elif check_in == 3 : #check out
            i = s.find('from')
            i2 = s.find(':', i)
            id_num = s[i2+2:]
            #print(id_num)
            check_out_list.append(id_num)
            id_chat.append(id_num)
        else : 
            print('not yet')
        i = s.find('to')
        name = s[14:i-1]
        name_chat.append(name)
        #print(name)
#print('Check in', check_in_list)
#print('Late', check_late_list)
#print('Check out', check_out_list)
#print('Name chat', name_chat)
#print('id chat', id_chat)
chat_record = dict(zip(id_chat,name_chat))
print('Chat')
print(chat_record)


# Creating a list of id and email
n = 0
email_namelist = []
id_namelist = []
for s in name_file :
    if n <1:
        n = n+1
        continue
    s = s.strip()
    i = s.find(',')
    email = s[0:i]
    id = s[i+1:]
    email_namelist.append(email)
    id_namelist.append(id)
class_list = dict(zip(id_namelist,email_namelist))
print('Name List')
print(class_list)

#print('Checkingxxx')



for k in chat_record:
    name = chat_record[k]
#    print(k,'->',name)
    email2 = ''
    for k2 in zoom_record :
        if zoom_record[k2] == name :
            email2 = k2
#            print(name,'->',k2)
            break

    for k3 in class_list :
        if class_list[k3] == email2 :
            id = k3
#            print(email2,'->',id)
            break
    
    #print(k, name, email, id)
    if(k != id) : 
        print("Alert")
        print(k, name, email2, id)
    #print(name, '->', zoom_record[name])
    #print(zoom_record[chat_record[k]], '->', class_list[class_list[chat_record[k]]])
#attendance = dict()
read_f = open('zoom/ID_List.csv')
write_f = open('zoom/output.txt', 'w')
output = dict()
for s in read_f:
    s = s.strip()
    #print(s)
    i = s.find(',')
    id = s[0:i]
    #print('id : ',id)
    output[id] = 0
#print('output : ')
#print(output)
print('Output : ')
print(output)


for i in output:
    if i in check_in_list:
        output[i] = 1

for i in output:
    if i in check_late_list:
        output[i] = 0.5

for i in output:
    if i in check_out_list:
        output[i] = output[i] + 1

print('AFter check')
print(output)

for i in output:
    if output[i] == 2:
        output[i] = 'P'
    elif output[i] == 1.5:
        output[i] = 'L'
    else :
        output[i] = 'U'

print(check_in_list)
print(check_late_list)
print(check_out_list)


#print(output)
for i in output:
    write_f.write(i+','+output[i]+'\n')
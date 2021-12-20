
name_list_f = open('zoom/NameList.csv')
zoom_f = open('zoom/participants_Aug_31.csv')
meeting_f = open('zoom/meeting_saved_chat_Aug_31.txt')
output_f = open('zoom/output_Aug_31.txt','w')

email_id_list = dict()
for name in name_list_f :
    name = name.strip()
    name_temp = name.split(',')
    #print(name)
    #print(name_temp)
    #print(name_temp[0])
    email_id_list[name_temp[1]] = name_temp[0]
print('Name list)')
print(email_id_list)

i = 0
zoom_email_list = dict()
for name in zoom_f:
    if i < 4:
        i = i+1
        continue
    name = name.strip()
    name_temp = name.split(',')
    #print(name_temp)
    zoom_email_list[name_temp[1]] = name_temp[0]
print('Zoom')
print(zoom_email_list)

state = 'start'
check_in = []
late = []
check_out = []
for check in meeting_f:
    check = check.strip()
    check = check.lower()
    if 'ผู้ช่วยศาสตราจารย์ภัทรวิทย์ พลพินิจ' in check and 'check in' in check:
        state = 'check in'
        continue
        print(check)
    elif 'ผู้ช่วยศาสตราจารย์ภัทรวิทย์ พลพินิจ' in check and 'late' in check:
        state = 'late'
        continue
        print(check)
    elif 'ผู้ช่วยศาสตราจารย์ภัทรวิทย์ พลพินิจ' in check and 'check out' in check:
        state = 'check out'
        continue
        print(check)
    
    # print(state)
    #print(check)
    if state == 'check in':
        check = check.split(':')
        #print(check)
        id = check[3].strip()
        #print(id)
        first3_id = id[0:3]
        #print(first3_id)
        if first3_id != '633' and first3_id != '623' and first3_id != '613':
            #print('Err :',first3_id)
            continue
        j = check[2].find('from')
        #print(j)
        meeting_name = check[2][j+5:].strip()
        #print(id, meeting_name)
        if id not in check_in:
            check_in.append(id)
        #print(meeting_name, id)
    #elif state == 'late':
    #elif state == 'check out':
    elif state == 'late':
        check = check.split(':')
        id = check[3].strip()
        first3_id = id[0:3]
        if first3_id != '633' and first3_id != '623' and first3_id != '613':
            continue
        j = check[2].find('from')
        meeting_name = check[2][j+5:].strip()
        if id not in late:
            late.append(id)
    elif state == 'check out':
        check = check.split(':')
        id = check[3].strip()
        first3_id = id[0:3]
        if first3_id != '633' and first3_id != '623' and first3_id != '613':
            continue
        j = check[2].find('from')
        meeting_name = check[2][j+5:].strip()
        if id not in check_out:
            check_out.append(id)        
print('Check in',len(check_in))
print('Late', len(late))
print('Check out', len(check_out))


class_check = dict()
for id in email_id_list:
    if id in check_in:
        class_check[id] = 1
    elif id in late:
        class_check[id] = 0.5
    else :
        class_check[id] = 0

    if id in check_out:
        class_check[id] = class_check[id]  + 1

print('Class room')
#print(class_check)

for student in class_check:
    if class_check[student] == 2 :
        class_check[student] = 'P'
        output_f.write(student + ',P\n')
    elif class_check[student] == 1.5 :
        class_check[student] = 'L'
        output_f.write(student + ',L\n')
    else :
        output_f.write(student + ',U\n')

output_f.close()
print('Class room : ')
#print(class_check)
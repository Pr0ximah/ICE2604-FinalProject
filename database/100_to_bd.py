import db_tool as db
import json
import scources
from pymysql.converters import escape_string

myjson = scources.myjson
s = db.sql_tool("ROOT", "testdb", "100_pdf_metadata")
for i in myjson:
    item = myjson[i]
    record = []
    for j in item:
        
        if j == 'keywords' or j == 'ref_paper':
            thing = ",".join(item[j])
            record.append(thing)

        elif j == 'author':
            dic=item[j]
            affiliation = dic['affiliation']
            name = dic['name']
            affiliation_content = ",".join(affiliation)
            name_content = ",".join(name)
            affiliation_content = escape_string(affiliation_content)
            name_content = escape_string(name_content)
       
 
            record.append(affiliation_content)
            record.append(name_content)

        elif j == 'abstract':
            record.append(escape_string(item[j]))
            
        elif j == 'link':
            record.append(escape_string(item[j]))

        elif j == 'extras':
            pass

        else:
            record.append(item[j])
                   
    # print(record)
    s.insert(record)
    s.save()

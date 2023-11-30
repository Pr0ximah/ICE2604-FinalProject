import json
from elasticsearch import Elasticsearch 

es = Elasticsearch(['http://localhost:9200'])

def get_json(string):
    return json.dumps(string, sort_keys=True, indent=4, separators=(',', ':'))

def json_print(string):
    print(json.dumps(string, sort_keys=True, indent=4, separators=(',', ':')))
    return

with open('MetaData.json','r',encoding='utf8')as fp:
    json_data = json.load(fp)

mappings = {
    "mappings" : {
      "properties" : {
        "id" : {
            "type" : "long",
        },
        "title" : {
          "type" : "text",
        },
        "year" : {
          "type" : "long",
        },
        "authors" :{
            "type" : "list",
        },
        "keywords" : {
            "type" : "list",
        }
      }
    }
}

paper_id = []
title = []
year = []
authors = []
keywords = []

for value in json_data.values():
    paper_id.append(value["paper_id"])
    title.append(value["title"])
    year.append(value["year"])
    authors.append(value["author"]["name"])
    keywords.append(value["keywords"])

# es.indices.delete(index = 'mydatabase')
es.indices.create(index ='mydatabase',body =mappings,ignore=400)
for i in range(100):
    body = {"paper_id":paper_id[i],"title":title[i],"year":year[i],"authors":authors[i],"keywords":keywords[i]}
    res = es.index(index="mydatabase",id=i,body=body)

def search_title(str):
    query = {
        "query":{
            "match":{
                "title": str
            }
        }
        ,"sort": [
            {
                "_score":{
                    "order": "desc"
                }
            }
        ]
        ,"size":1000
    }
    result = es.search(index="mydatabase",body=query)
    hit = result["hits"]["hits"]
    return hit

def search_year(time):
    time = int(time)
    query = {
        "query":{
            "match":{
                "year": time
            }
        }
        ,"size":1000
    }
    result = es.search(index="mydatabase",body=query)
    hit = result["hits"]["hits"]
    return hit

def search_author(str):
    query = {
        "query":{
            "match":{
                "authors": str
            }
        }
        ,"sort": [
            {
                "_score":{
                    "order": "desc"
                }
            }
        ]
        ,"size":1000
    }
    result = es.search(index="mydatabase",body=query)
    hit = result["hits"]["hits"]
    return hit

def search_keywords(str):
    query = {
        "query":{
            "match":{
                "keywords": str
            }
        }
        ,"sort": [
            {
                "_score":{
                    "order": "desc"
                }
            }
        ]
        ,"size":1000
    }
    result = es.search(index="mydatabase",body=query)
    hit = result["hits"]["hits"]
    return hit

def get_result(type: str, content: str):
    res = ''
    if type == 'Title':
        res = search_title(content)
    elif type == 'Year':
        res = search_year(content)
    elif type == 'Author':
        res = search_author(content)
    elif type == 'Keywords':
        res = search_keywords(content)
    return get_json(res)
    
if __name__ == '__main__':
    # json_print(search_title("of"))
    # json_print(search_year("1990"))
    # json_print(search_author("R. Arjmandzadeh"))
    # json_print(search_keywords("mantle"))
    print(get_result('Year', '1981'))
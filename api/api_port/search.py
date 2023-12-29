import json
from elasticsearch import Elasticsearch, ConnectionError
from api_port.db_tool import sql_tool
# from api.api import dict_all
error_name = ""

dict_all = {}

def get_json_data():
    datadepot = sql_tool("ADMINROOT", "ice2604_final_project", "100_pdf_metadata")
    s = datadepot.fetch_all()
    for i in s:
        dict_elem = {}
        dict_elem["date"]=i[0]
        if i[1]:
            dict_elem["ref_paper"]=i[1].split(",")
        else:
            dict_elem["ref_paper"]=[]
        if i[2]:
            dict_elem["conference"]=i[2]
        else:
            dict_elem["conference"]=""
        if i[3]:
            dict_elem["keywords"]=i[3].split(",")
        else:
            dict_elem["keywords"]=[]
        dict_elem["year"]=int(i[4])
        if i[5]:
            dict_elem["author"]={"affiliation":i[5].split(","), "name":i[6].split(",")}
        else:
            dict_elem["author"] = {"affiliation": "", "name": ""}
        dict_elem["last_page"]=i[7]
        dict_elem["link"]=i[8]
        dict_elem["abstract"]=i[9]
        dict_elem["title"]=i[10]
        dict_elem["paper_id"]=i[11]
        if i[12] is not None:
            dict_elem["volume"]=int(i[12])
        dict_elem["update_time"]=i[13]
        dict_elem["journal"]=i[14]
        dict_elem["issn"]=i[15]
        dict_elem["first_page"]=i[16]
        dict_elem["publisher"]=i[17]
        dict_elem["doi"]=i[18]
        dict_all[i[11]]=dict_elem

get_json_data()

# es = Elasticsearch()
es = Elasticsearch(["http://localhost:9200"])

def get_json(string):
    return json.dumps(string, sort_keys=True, indent=4, separators=(",", ":"))

def json_print(string):
    print(json.dumps(string, sort_keys=True, indent=4, separators=(',', ':')))
    return

json_data = dict_all

body = {
    "mappings": {
      "properties": {
        "data": {
          "type": "text",  
        },
        "paper_id":{
            "type": "text",
            
        },
        "title": {
            "type": "text",
        },
        "year" : {
          "type" : "long",
        },
        "authors" :{
            "type" : "list",
        },
        "keywords" : {
            "type" : "list",
        },
        "link" : {
            "type" : "text"
        },
        "first_page" : {
            "type" : "long"
        },
        "abstract" : {
            "type" : "text"
        },
        "journal" : {
            "type" : "text"
        },
        "doi" : {
            "type" : "text"
        },
      }
    }
}

date = []
paper_id = []
title = []
year = []
authors = []
keywords = []
link = []
first_page = []
abstract = []
journal = []
doi = []

for value in json_data.values():
    date.append(value["date"])
    paper_id.append(value["paper_id"])
    title.append(value["title"])
    year.append(value["year"])
    authors.append(value["author"]["name"])
    keywords.append(value["keywords"])
    link.append(value["link"])
    first_page.append(value["first_page"])
    abstract.append(value["abstract"])
    journal.append(value["journal"])
    doi.append(value["doi"])
try:
    # es.indices.delete(index = 'mydatabase')
    es.indices.create(index ='mydatabase',body=body,ignore=400)
    for i in range(len(json_data)):
        mapping = {"date":date[i],"paper_id":paper_id[i],"title":title[i],"year":year[i],"authors":authors[i],"keywords":keywords[i],"link":link[i],"first_page":first_page[i],"abstract":abstract[i],"journal":journal[i],"doi":doi[i]}
        # mapping = {"title":title[i]}
        res = es.index(index="mydatabase",id=i,body=mapping)

    def search_title(str):
        query = {
            "query":{
                "wildcard":{
                    "title": "*" + str.lower() + "*"
                },
                
                # "match":{
                #     "title": str
                # }
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
        query2 = {
            "query": {
                "match": {
                    "title": {
                        "query": str,
                        "fuzziness": "2"
                    }
                }
            }
            ,"size":1000
        }
        result = es.search(index="mydatabase",body=query2)
        
        hit = result["hits"]["hits"]
        return hit

    def search_year(time):
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
                "wildcard":{
                    "authors": "*" + str.lower() + "*"
                }
                # "match":{
                #     "authors": str
                # }
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
        query2 = {
            "query": {
                "match": {
                    "authors": {
                        "query": str,
                        "fuzziness": "0"
                    }
                }
            },
            "size":1000
        }
        result = es.search(index="mydatabase",body=query2)
        hit = result["hits"]["hits"]
        return hit

    def search_keywords(str):
        query = {
            "query":{
                "wildcard":{
                    "keywords": "*" + str.lower() + "*"
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
        query2 = {
            "query": {
                "match": {
                    "keywords": {
                        "query": str,
                        "fuzziness": "2"
                    }
                }
            }
            ,"size":1000
        }
        result = es.search(index="mydatabase",body=query2)
        hit = result["hits"]["hits"]
        return hit


    def add_search(str):
        if(str.isdigit()):
            return search_year(int(str))
        else:
            hit1 = search_title(str)
            hit2 = search_author(str)
            hit3 = search_keywords(str)
            return hit1+hit2+hit3

except ConnectionError:
    print("连接错误:无法连接到Elasticsearch。")
    error_name = "ConnectionError"
except NameError:
    print("输入错误:根据年份查询需要输入数字")
    error_name = "NameError"
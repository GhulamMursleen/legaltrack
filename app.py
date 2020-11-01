import flask
import csv
import math
import pandas as pd
from fuzzywuzzy import process,fuzz
from werkzeug.utils import secure_filename
from flask import  abort,request,send_file,jsonify, make_response
from Untitled import Model
model=Model()

from flask_cors import CORS, cross_origin
app = flask.Flask(__name__)
cors = CORS(app)

app.config['CORS_HEADERS'] = 'Content-Type'
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "Api is working for Legal Contracts";
@app.route('/clause/search', methods = ['GET', 'POST'])
def search():
    
   if request.method == "OPTIONS": # CORS preflight
        return _build_cors_prelight_response()
   elif request.method == 'GET':
      
      content = request.get_json()
      print(content)
      Filename="./contractCollection.csv"
      df = pd.read_csv(Filename, error_bad_lines=False)
      df = df.fillna("False")
      result=[]
      clause_category=""
      tag=""
      cont_type=""
      text=""
      no_of_records=""
      try:
          print("try")
          cont_type=content["cont_type"];
          clause_category=content["clause_category"]
          tag=content["tag"];
          
          text=content["text"];
          no_of_records=content["records"];
      except:
          return _corsify_actual_response(jsonify("parameters error"))
      if cont_type!="" and clause_category!="":
        contain_values = df[df['name'].str.contains(cont_type)   ]
        result=contain_values[df['ClausesCategories'].str.contains(clause_category)]
        if (len(result))==0:
                result=[1,2]
      elif cont_type!="":
            result = df[df['name'].str.contains(cont_type)   ]
            if (len(result))==0:
                result=[1,2]
      elif clause_category!="":
            result=df[df['ClausesCategories'].str.contains(clause_category)]
            if (len(result))==0:
                result=[1,2]
      else:
        result=[1,2]
      #print ("result",len(result))
    
      if len(result)>0:
        Filename="./ClausesCategoriesCollection.csv"
        df2 = pd.read_csv(Filename, error_bad_lines=False)
        df2 = df2.fillna("False")
        if clause_category!="":#########if category is empty
            contain_values = df2[df2['name'].str.contains(clause_category)   ] ##if caluse category exist
            if len(contain_values)>0:
                 ids=int(contain_values["_id"])
                 Filename="./ClauseCollection.csv"
                 df3 = pd.read_csv(Filename, error_bad_lines=False)
                 df3 = df3.fillna("False")
                 #df3['clauseID']=pd.to_numeric(df3['clauseID'])
                 rows=df3.loc[(df3['tags'] == tag) &(df3['clauseID'] == ids)]
                 data=[]
                 for index, row in rows.iterrows():
                     if (len(data)<no_of_records*10):
                         print("row",row["_id"])
                         #data.append({"name":row["name"],"description":row["description"]})
                         data.append({"description":row["description"]})
                 #print("data",data)
                 if len(data)==0:
                      rows=df3.loc[(df3['clauseID'] == ids)]
                      data=[]
                      for index, row in rows.iterrows():
                         if (len(data)<no_of_records*10):
                             print("row",row["_id"])
                             #data.append({"name":row["name"],"description":row["description"]})
                             data.append({"description":row["description"]})
                      return _corsify_actual_response(jsonify(data))
                 return _corsify_actual_response(jsonify(data))
                 ####return data
                 #print("rows",rows,df3.dtypes)
            elif tag!="":  ####################if category does not exist in records but tag exist 
                 #ids=int(contain_values["_id"])
                 Filename="./ClauseCollection.csv"
                 df3 = pd.read_csv(Filename, error_bad_lines=False)
                 df3 = df3.fillna("False")
                 #df3['clauseID']=pd.to_numeric(df3['clauseID'])
                 rows=df3.loc[(df3['tags'] == tag)]
                 data=[]
                 for index, row in rows.iterrows():
                     if (len(data)<no_of_records*10):
                         #print("row",row["_id"])
                         #data.append({"name":row["name"],"description":row["description"]})
                         data.append({"description":row["description"]})
                     else:
                         break
                 #print("data tag exist",data)
                 return _corsify_actual_response(jsonify(data))
                 ####return data
            elif text!="":#########tag does not exist but text exist
                 Filename="./ClauseCollection.csv"
                 df3 = pd.read_csv(Filename, error_bad_lines=False)
                 df3 = df3.fillna("False")
                 entities=df3['name'].tolist()
                 descriptions=df3['description'].tolist()
                 results=process.extract(text, descriptions, scorer=fuzz.token_sort_ratio)
                 #print(results)
                 data=[]
                 print(results[0][0],results[0][1])
                 for x in results:
                     if (len(data)<no_of_records*10):
                         #data.append({"name":entities[descriptions.index(x[0])],"description":x[0]})
                         data.append({"description":x[0]})
                     else:
                         break
                 #print("data",data)
                 return _corsify_actual_response(jsonify(data))
            else: ############if text not exist
                #print("g aya no")
                return _corsify_actual_response(jsonify({}))
                
        elif tag!="": ############if clause category does not exist but tag exist
                 Filename="./ClauseCollection.csv"
                 df3 = pd.read_csv(Filename, error_bad_lines=False)
                 df3 = df3.fillna("False")
                 #df3['clauseID']=pd.to_numeric(df3['clauseID'])
                 rows=df3.loc[(df3['tags'] == tag)]
                 data=[]
                 for index, row in rows.iterrows():
                     if (len(data)<no_of_records*10):
                         print("row",row["_id"])
                         #data.append({"name":row["name"],"description":row["description"]})
                         data.append({"description":row["description"]})
                 #print("data if tag exist only",len(data))
                 return _corsify_actual_response(jsonify(data))
        elif text!="":#########tag does not exist but text exist
                 Filename="./ClauseCollection.csv"
                 df3 = pd.read_csv(Filename, error_bad_lines=False)
                 df3 = df3.fillna("False")
                 entities=df3['name'].tolist()
                 descriptions=df3['description'].tolist()
                 results=process.extract(text, descriptions, scorer=fuzz.token_sort_ratio)
                 #print(results)
                 data=[]
                 #print(results[0][0],results[0][1])
                 for x in results:
                     if (len(data)<no_of_records*10):
                         #data.append({"name":entities[descriptions.index(x[0])],"description":x[0]})
                         data.append({"description":x[0]})
                     else:
                         break
                 #print("data",data)
                 return _corsify_actual_response(jsonify(data))
        else: ############if text not exist
            return _corsify_actual_response(jsonify({}))
      #print(clause_category)
      #data = request.values
      #print("coming",request.form["id"])
      
      
      #id=str(request.form["id"])
      #print(id,type(id))
      #response=model.recommendation(id)
      
      
   else:
      return _corsify_actual_response(jsonify("error"))
  
#################contracts/types ##########get  no parameter  #################post contract/types   ###########3 parameters
@app.route('/contracts/types', methods = ['GET', 'POST', 'PUT', 'DELETE'])
def requestcontracttypes():
    
   if request.method == "OPTIONS": # CORS preflight
        return _build_cors_prelight_response()
   elif request.method == "PUT":
            newrow=[]
            content = request.get_json()
            try:
                print("content",content)
                newrow.append(content["id"])
                newrow.append(content["name"])
                newrow.append(content["clausecategories"])
            except:
                return _corsify_actual_response(jsonify("Please try again!!!!! Parameters error"))
            lines=[]
            with open('./ClausesCategoriesCollection.csv',encoding='utf8') as readFile:
            
                reader = csv.reader(readFile)
            
                for row in reader:
                    
                    print(row,len(row))
                    if row[0] == str(newrow[0]):
                           lines.append(newrow)
                    else:
                        lines.append(row)
                        
            
            with open('ClausesCategoriesCollection.csv', 'w',encoding='utf8', newline='') as writeFile:
            
                writer = csv.writer(writeFile)
            
                writer.writerows(lines)
            
                return _corsify_actual_response(jsonify("Record Updated Successfully"))
            return _corsify_actual_response(jsonify("Please Try Again Later!!!!!!!!"))
   elif request.method == "DELETE":
            content = request.get_json()
            ids=0
            try:
                ids=content["id"]
                
            except:
                return _corsify_actual_response(jsonify("Parameters error"))
            lines=[]
            with open('./contractCollection.csv',encoding='utf8') as readFile:
            
                reader = csv.reader(readFile)
            
                for row in reader:
                    
                    print(row,len(row))
                    if len(row)>0 and row[0] == str(ids):
                           pass
                    elif len(row)==0:
                        pass
                    else:
                        lines.append(row)
                        
            
            with open('contractCollection.csv', 'w',encoding='utf8', newline='') as writeFile:
            
                writer = csv.writer(writeFile)
            
                writer.writerows(lines)
            
                return _corsify_actual_response(jsonify("Record Deleted Successfully"))
            return _corsify_actual_response(jsonify("Please Try Again Later!!!!!!!!"))
   elif request.method == 'GET':
            Filename="./contractCollection.csv"         
            df = pd.read_csv(Filename, usecols = ['_id', 'name'])
            df = df.fillna("False")
            number=3
            totalpages=math.ceil(len(df)/10)
            content = request.get_json()
            
            try:
                number=content["page"]
                if number<=totalpages:
                    number=number*10
                else:
                    return _corsify_actual_response(jsonify("Page does not exist"))
            except:
                return _corsify_actual_response(jsonify("Parameters error"))
            #print("len(df)",len(df),totalpages)
            df = df.iloc[number:]
            #print("len(df)",len(df),totalpages)
            array=[]
            for index, row in df.iterrows() :
                if len(array) <10:
                    array.append({"id":row[0],"name":row[1]})
                else:
                    break
            array2=[]
            array2.append({"pages":totalpages})
            array2.append({"data":array})
            array=array2
            #print(array)
      
            return _corsify_actual_response(jsonify(array))
   elif request.method == 'POST':
          row=[]
          content = request.get_json()
          try:
                row.append(content["id"])
                row.append(content["name"])
                row.append(content["clausecategories"])
          except:
                return _corsify_actual_response(jsonify("Parameters error"))
          with open("./contractCollection.csv",encoding='utf8', mode='a+', newline='') as Data:
                employee_writer = csv.writer(Data, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                employee_writer.writerow(row)
                return _corsify_actual_response(jsonify("successful"))
          
          return _corsify_actual_response(jsonify("Please try again!!!!!"))
   
   else:
      return _corsify_actual_response(jsonify("Please try again!!!!!"))

#################clause/categories ##########get  no parameter  #################caluse/categories post  ###########add no parameter 
@app.route('/clause/categories', methods = ['GET', 'POST', 'PUT', 'DELETE'])
def calusecategories():
    
   if request.method == "OPTIONS": # CORS preflight
        return _build_cors_prelight_response()
   elif request.method == "PUT":
            newrow=[]
            content = request.get_json()
            try:
                print("content",content)
                newrow.append(content["id"])
                newrow.append(content["name"])
            except:
                return _corsify_actual_response(jsonify("Please try again!!!!! Parameters error"))
            lines=[]
            with open('./ClausesCategoriesCollection.csv',encoding='utf8') as readFile:
            
                reader = csv.reader(readFile)
            
                for row in reader:
                    
                    print(row,len(row))
                    if row[0] == str(newrow[0]):
                           lines.append(newrow)
                    else:
                        lines.append(row)
                        
            
            with open('ClausesCategoriesCollection.csv', 'w',encoding='utf8', newline='') as writeFile:
            
                writer = csv.writer(writeFile)
            
                writer.writerows(lines)
            
                return _corsify_actual_response(jsonify("Record Updated Successfully"))
            return _corsify_actual_response(jsonify("Please Try Again Later!!!!!!!!"))
   elif request.method == "DELETE":
            content = request.get_json()
            ids=0
            try:
                ids=content["id"]
                
            except:
                return _corsify_actual_response(jsonify("Parameters error"))
            lines=[]
            with open('./ClausesCategoriesCollection.csv',encoding='utf8') as readFile:
            
                reader = csv.reader(readFile)
            
                for row in reader:
                    
                    print(row,len(row))
                    if len(row)>0 and row[0] == str(ids):
                           pass
                    elif len(row)==0:
                        pass
                    else:
                        lines.append(row)
                        
            
            with open('ClausesCategoriesCollection.csv', 'w',encoding='utf8', newline='') as writeFile:
            
                writer = csv.writer(writeFile)
            
                writer.writerows(lines)
            
                return _corsify_actual_response(jsonify("Record Deleted Successfully"))
            return _corsify_actual_response(jsonify("Please Try Again Later!!!!!!!!"))
   elif request.method == 'GET':
            Filename="./ClausesCategoriesCollection.csv"         
            df = pd.read_csv(Filename, usecols = ['_id', 'name'])
            df = df.fillna("False")
            #json = df.to_dict
            number=3
            totalpages=math.ceil(len(df)/10)
            content = request.get_json()
            
            try:
                number=content["page"]
                if number<=totalpages:
                    number=number*10
                else:
                    return _corsify_actual_response(jsonify("Page does not exist"))
            except:
                return _corsify_actual_response(jsonify("Parameters error"))
            #print("len(df)",len(df),totalpages)
            df = df.iloc[number:]
            #print("len(df)",len(df),totalpages)
            array=[]
            for index, row in df.iterrows() :
                if len(array) <10:
                    array.append({"id":row[0],"name":row[1]})
                else:
                    break
            array2=[]
            array2.append({"pages":totalpages})
            array2.append({"data":array})
            array=array2
            #print(array)
      
            return _corsify_actual_response(jsonify(array))
   elif request.method == 'POST':
            row=[]
            content = request.get_json()
            try:
                row.append(content["id"])
                row.append(content["name"])
            except:
                return _corsify_actual_response(jsonify("Please try again!!!!! Parameters error"))
            #row.append(request.form["id"])
            #row.append(request.form["name"])
            #row.append(15)
            #row.append("Mursleen")
            
            with open("./ClausesCategoriesCollection.csv",encoding='utf8', mode='a+', newline='') as Data:
                            employee_writer = csv.writer(Data, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                            employee_writer.writerow(row)
                            print('done')
                            return _corsify_actual_response(jsonify("successful"))
      
            return _corsify_actual_response(jsonify("Please try again"))
   
   else:
      return _corsify_actual_response(jsonify("Please try again"))
#################clause/tags ##########get  no parameter only get
@app.route('/clause/tags', methods = ['GET', 'POST'])
def clausetags():
    
   if request.method == "OPTIONS": # CORS preflight
        return _build_cors_prelight_response()
   elif request.method == 'GET':
            Filename="./ClauseCollection.csv"         
            df = pd.read_csv(Filename, usecols = [ 'tags'])
            df=df.drop_duplicates()
            df=df.drop_duplicates()
            df=df.dropna()
            #values = df.unique()
            #print("values",df)
            
            array3=[]
            for index, row in df.iterrows() :
                array3.append({"tag":row[0]})
            #print(array3)
            return _corsify_actual_response(jsonify(array3))
   
   else:
      return _corsify_actual_response(jsonify("Please try again!!!!!error"))
#################caluse/categories post  ###########add no parameter
@app.route('/legal/clauses', methods = ['GET','POST', 'PUT', 'DELETE'])
def legalclauses():
    
   if request.method == "OPTIONS": # CORS preflight
        return _build_cors_prelight_response()
   elif request.method == "PUT":
            newrow=[]
            content = request.get_json()
            try:
                print("content",content)
                newrow.append(content["id"])
                newrow.append(content["name"])
                newrow.append(content["text"])
                newrow.append(content["tags"])
                newrow.append(content["clauseid"])
            except:
                return _corsify_actual_response(jsonify("Please try again!!!!! Parameters error"))
            lines=[]
            with open('./ClauseCollection.csv',encoding='utf8') as readFile:
            
                reader = csv.reader(readFile)
            
                for row in reader:
                    
                    print(row,len(row))
                    if row[0] == str(newrow[0]):
                           lines.append(newrow)
                    else:
                        lines.append(row)
                        
            
            with open('ClauseCollection.csv', 'w',encoding='utf8', newline='') as writeFile:
            
                writer = csv.writer(writeFile)
            
                writer.writerows(lines)
            
                return _corsify_actual_response(jsonify("Record Updated Successfully"))
            return _corsify_actual_response(jsonify("Please Try Again Later!!!!!!!!"))
   elif request.method == "DELETE":
            content = request.get_json()
            ids=0
            try:
                ids=content["id"]
                
            except:
                return _corsify_actual_response(jsonify("Parameters error"))
            lines=[]
            with open('./ClauseCollection.csv',encoding='utf8') as readFile:
            
                reader = csv.reader(readFile)
            
                for row in reader:
                    
                    print(row,len(row))
                    if len(row)>0 and row[0] == str(ids):
                           pass
                    elif len(row)==0:
                        pass
                    else:
                        lines.append(row)
                        
            
            with open('ClauseCollection.csv', 'w',encoding='utf8', newline='') as writeFile:
            
                writer = csv.writer(writeFile)
            
                writer.writerows(lines)
            
                return _corsify_actual_response(jsonify("Record Deleted Successfully"))
            return _corsify_actual_response(jsonify("Please Try Again Later!!!!!!!!"))
   elif request.method == 'GET':
            Filename="./ClauseCollection.csv"         
            df = pd.read_csv(Filename, usecols = ['_id', 'name','description','tags','clauseID'])
            df = df.fillna("False")
            #json = df.to_dict
            number=3
            totalpages=math.ceil(len(df)/10)
            content = request.get_json()
            
            try:
                number=content["page"]
                if number<=totalpages:
                    number=number*10
                else:
                    return _corsify_actual_response(jsonify("Page does not exist"))
            except:
                return _corsify_actual_response(jsonify("Parameters error"))
            #print("len(df)",len(df),totalpages)
            df = df.iloc[number:]
            #print("len(df)",len(df),totalpages)
            array=[]
            for index, row in df.iterrows() :
                if len(array) <10:
                    array.append({"id":row[0],"name":row[1],"description":row[2],"tags":row[3],"clauseid":row[4]})
                else:
                    break
            array2=[]
            array2.append({"pages":totalpages})
            array2.append({"data":array})
            array=array2
            #print(array)
      
            return _corsify_actual_response(jsonify(array))
   elif request.method == 'POST':
            content = request.get_json()
            row=[]
            try:
                row.append(content["id"])
                row.append(content["name"])
                row.append(content["text"])
                row.append(content["tags"])
                row.append(content["clauseid"])
            except:
                return _corsify_actual_response(jsonify("Please try again!!!!! Parameters error"))
            #row.append(15)
            #row.append("Mursleen")
            #row.append("Mursleen")
            #row.append("Mursleen")
            #row.append(15)
            
            with open("./ClauseCollection.csv",encoding='utf8', mode='a+', newline='') as Data:
                            employee_writer = csv.writer(Data, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                            employee_writer.writerow(row)
                            print('done')
                            #return _corsify_actual_response(jsonify("success"))
                            return _corsify_actual_response(jsonify("successful"))
            return _corsify_actual_response(jsonify("error"))
   
   else:
      return _corsify_actual_response(jsonify("Please try again!!!!! error"))
#####################mergecall
@app.route('/clause/category/merge', methods = ['GET', 'POST'])
def merge():
    
   if request.method == "OPTIONS": # CORS preflight
        return _build_cors_prelight_response()
   elif request.method == 'GET':
                  #################contract types
                Filename="./contractCollection.csv"         
                df = pd.read_csv(Filename, usecols = ['_id', 'name'])
                df = df.fillna("False")
                #json = df.to_dict
                array=[]
                for index, row in df.iterrows() :
                    array.append({"id":row[0],"name":row[1]})
                #print(array)
                
                        #################clause categories
                Filename="./ClausesCategoriesCollection.csv"         
                df = pd.read_csv(Filename, usecols = ['_id', 'name'])
                df = df.fillna("False")
                #json = df.to_dict
                array2=[]
                for index, row in df.iterrows() :
                    array2.append({"id":row[0],"name":row[1]})
                #print(array2)
                
                        #################clause tags
                Filename="./ClauseCollection.csv"         
                
                df = pd.read_csv(Filename, usecols = [ 'tags'])
                df = df.fillna("False")
                df=df.drop_duplicates()
                df=df.drop_duplicates()
                df=df.dropna()
                #values = df.unique()
                #print("values",df)
                
                array3=[]
                for index, row in df.iterrows() :
                    array3.append({"tag":row[0]})
                #print(array3)
                
                
                #############################mergeall
                merge=[]
                merge.append(array)
                merge.append(array2)
                merge.append(array3)
                #print(merge)
                return _corsify_actual_response(jsonify(merge))
  
   
   else:
      return _corsify_actual_response(jsonify("Please try again!!!!! error"))
def _build_cors_prelight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    #response.headers.add('Access-Control-Allow-Headers', "*")
    #response.headers.add('Access-Control-Allow-Methods', "*")
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

if __name__ == '__main__':
    app.run(host= "0.0.0.0", port = 3000, threaded=True,debug=True, use_reloader=True)
import google.generativeai as palm
import pyTigerGraph as tg
import pandas as pd
import streamlit as st

@st.cache_resource()
def load_model(api_token="AIzaSyAc69h0_vY3yDqCgmCXQuZdCWmV7pKObII"):
    palm.configure(api_key=api_token)
    return palm
@st.cache_data()
def get_output(model,prompt,model_id="models/text-bison-001"):
    completion=model.generate_text(model=model_id,prompt=prompt,temperature=0.99,max_output_tokens=1024,)
    gsql_query= completion.result.strip('`gsql')
    gsql_query = gsql_query.replace("CREATE", "ADD")

    if "UNDIRECTED EDGE" not in gsql_query:
         gsql_query = gsql_query.replace("EDGE", "UNDIRECTED EDGE")
    
    return gsql_query


@st.cache_data()
def get_prompt(topic,dataset,business_req):
    sys_prompt = """ 
    --------------------------------------------------------------- Creating the Vertex---------------------------------------------------------------
    Syntax:CREATE VERTEX VERTEX_NAME_ (PRIMARY_ID attibute1 datatype, attibute2 datatype, attibute3 datatype)  WITH primary_id_as_attribute="true";
    example:CREATE VERTEX Movie_ (PRIMARY_ID movie_id UINT , name STRING, year UINT)  WITH primary_id_as_attribute="true";

    CREATE VERTEX User_ (PRIMARY_ID user_id UINT, name STRING, age UINT, gender STRING, postalCode STRING)  WITH primary_id_as_attribute="true";


    use can you different datatypes like:STRING, INT, UINT, DATETIME,FLOAT,DOUBLE,BOOL,LIST.
    for any time or date related data use DATETIME Even for TIMESTAMP use DATETIME as datatype and dont use any other datatype other than STRING, 
    INT, UINT, DATETIME,FLOAT,DOUBLE,BOOL,LIST

    --Creating the edges---
    syntax:CREATE UNDIRECTED EDGE EDGE_NAME_  (FROM vertex_name_ , TO vertex_name_);
    example:CREATE UNDIRECTED EDGE Friend_Of_ (FROM User_ , TO User_);
    example:CREATE UNDIRECTED EDGE Customer_Order_ (FROM Customer_ , TO Products_);

    --for comment---
    for commneting any line use //
    example: //this is comment


    --------------------------------------------------------------- Reserved Keywords---------------------------------------------------------------
    dont use above keywords while creating schema struture like for example Order ,order,ORDER all are same so instaesd of this use Order_details etc
    If you are using Reserved Keyword like Order make it as unreserved keyword like Orders put  extra s for reserved Keyword

    The list of reserved keywords consists of various terms used within a specific domain or programming language.These keywords are predefined 
    and should not be utilized as vertex names, edge names, or attribute names in a graph database or any system that employs them.To maintain the 
    system's integrity and prevent conflicts or errors during query execution,it's important to select names for vertices, edges, and attributes 
    that do not coincide with these reserved keywords.This practice helps ensure that queries and data operations are correctly interpreted by 
    the system. Here is the list of reserved keywords separated by commas:

    ACCUM, ADD, ALL, ALLOCATE, ALTER, AND, ANY, AS, ASC, AVG, BAG, BATCH, BETWEEN, BIGINT,ORDERBLOB, BOOL, BOOLEAN, BOTH, BREAK, BY, CALL,
    CASCADE, CASE, CATCH, CHAR, CHARACTER, CHECK, CLOB, COALESCE, COMPRESS, CONST, CONSTRAINT,CONTINUE, COST, COUNT, CREATE, CURRENT_DATE, 
    CURRENT_TIME, CURRENT_TIMESTAMP, CURSOR, KAFKA, S3,DATETIME, DATETIME_ADD, DATETIME_SUB, DAY, DATETIME_DIFF, DATETIME_TO_EPOCH, DATETIME_FORMAT, 
    DECIMAL,DECLARE, DELETE, DESC, DISTRIBUTED, DO, DOUBLE, DROP, EDGE, ELSE, ELSEIF, EPOCH_TO_DATETIME, END, ESCAPE,EXCEPTION, EXISTS, FALSE, FILE,
    SYS.FILE_NAME, FILTER, FIXED_BINARY, FLOAT, FOR, FOREACH, FROM, GLOBAL, GRANTS,GRAPH, GROUP, GROUPBYACCUM, HAVING, HOUR, HEADER, HEAPACCUM, IF, 
    IGNORE, SYS.INTERNAL_ID, IN, INDEX,INPUT_LINE_FILTER, INSERT, INT, INTERSECT, INT8, INT16, INT32, INT32_T, INT64_T, INTEGER, INTERPRET, INTO, 
    IS, ISEMPTY, JOB,JOIN, JSONARRAY, JSONOBJECT, KEY, LEADING, LIKE, LIMIT, LIST, LOAD, LOADACCUM, LOG, LONG, MAP, MINUTE, NOBODY, NOT, NOW, NULL,
    OFFSET, ON, OR, ORDER, PINNED, POST_ACCUM, POST-ACCUM, PRIMARY, PRIMARY_ID, PRINT, PROXY, QUERY, QUIT, RAISE, RANGE, REDUCE, REPLACE,
    RESET_COLLECTION_ACCUM, RETURN, RETURNS, SAMPLE, SECOND, SELECT, SELECTVERTEX, SET, STATIC, STRING, SUM, TARGET, TEMP_TABLE, THEN, TO, TO_CSV,
    TO_DATETIME, TRAILING, TRANSLATESQL, TRIM, TRUE, TRY, TUPLE, TYPE, TYPEDEF, UINT, UINT8, UINT16, UINT32, UINT8_T, UINT32_T, UINT64_T, UNION, UPDATE,
    UPSERT, USING, VALUES, VERTEX, WHEN, WHERE, WHILE, WITH, GSQL_SYS_TAG, _INTERNAL_ATTR_TAG.
    dont use above keywords while creating schema struture like for example Order ,order,ORDER all are same so instaesd of this use Order_details etc
    If you are using Reserved Keyword like Order make it as unreserved keyword like Orders put  extra s for reserved Keyword

    -------------------------------------------------------------------------------------------------------------------------------------------------
    You are helpful assistant,you will use the above knowledge to create GSQL queries .
    From the bellow context  extract vertices that can have edge between them and Create a Graph Schema Struture using GSQL.

    """
    context = """
    ```context
    Analyze the given dataset and identify opportunities to create more additional vertices by splitting column headers and analyzing each column headers 
    for a more detailed graph representation.For each new vertex, establish a PRIMARY ID based on the most relevant attributes found in the dataset.
    Ensure that attributes are not duplicated across multiple vertices to maintain normalization.Your goal is to maximize! the number of vertices that can 
    be interconnected with other vertices to get more insights.Please provide the resulting graph schema structure in GSQL format with the correct syntax,
    detailing the newly created vertices and their relevant attributes. Additionally, describe the relationships between these vertices.
    if any, and the existing ones. This will help create a more comprehensive and interconnected graph representation of the data.


    If you are using Reserved Keyword like 'Order' inorder to make it as vertex name or edge name make it as Order_ by putting extra '_' for reserved Keyword Inorder to maintain consistancy
    """
    
    prompt = f""" 
        {sys_prompt} \n 
         {context}\n 
         Topic:{topic}\n
          Dataset:\n
        {dataset}\n 
        ``` 
        {business_req}
         """
    return prompt



# def set_graph_connection(hostname,graphname,secret):
#     conn = tg.TigerGraphConnection(host=hostname,graphname=graphname,tgCloud=True, gsqlSecret=secret)
    
#     try:
#         authToken=conn.getToken(secret)
#         authToken=authToken[0]
#         conn = tg.TigerGraphConnection(host=hostname,graphname=graphname,tgCloud=True, gsqlSecret=secret,apiToken=authToken)
        
#     except:
#         st.write("Got a error while connecting to graph")
        
#     return conn


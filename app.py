import pandas as pd
import streamlit as st 
from main import load_model,get_prompt,get_output
from PIL import Image
import pyTigerGraph as tg


with st.sidebar:
    image = Image.open('ns_logo.jpg')
    st.image(image)
    st.header("Automatic Schema Generation")

topic = st.text_input('Topic')
#business_req=st.text_input("Business Requirements","Please enter business requirement!")

api_token=st.text_input("API_Key")

model=load_model(api_token)

uploaded_files = st.file_uploader("Choose a CSV file", accept_multiple_files=True)
if uploaded_files is not None:
    files={}
    for i,file in enumerate(uploaded_files):
        files[i]=pd.read_csv(file)
else:
    st.write("Please upload files!")
    
if len(uploaded_files)>0:
    business_req=st.text_input("Prompt")

else:
    business_req=""

dataset=""
if len(uploaded_files)>0:
    for i in range(len(files)):
        data=files[i][:10].to_string()
        dataset=dataset+"\n"+ data

gsql_query=""
if len(dataset)>0 and len(topic)>0 and len(business_req)>0:   
  prompt=get_prompt(topic,dataset,business_req)

  gsql_query=get_output(model,prompt)
  



edit_dict={}
if len(gsql_query)>0:
    edit_dict["GSQL_Ouput"]=gsql_query
    gsql_query=st.data_editor(edit_dict)
    
    #if st.button("Accept"):
    text_contents = gsql_query["GSQL_Ouput"]
    output=f"""#Importing libraries
import pyTigerGraph as tg
import json
import pandas as pd

#Establish the connection with tigergraph

hostName = "enter graph url here"
userName = "enter user name"
passWord = "enter password"
graphName="enter graph name"
secret="enter secret key for the same graph"
conn = tg.TigerGraphConnection(host=hostName,graphname=graphName,tgCloud=True, gsqlSecret=secret)
authToken=conn.getToken(secret)
authToken=authToken[0]

conn = tg.TigerGraphConnection(host=hostName,graphname=graphName,tgCloud=True, gsqlSecret=secret,apiToken=authToken)

conn.gsql('ls')

#Create Schema
result=conn.gsql('''Use Specify GraphName
{text_contents}''')
print(result)
             """
    output_file = "create_schema.py"

    # with open(output_file, "w") as file:
    #     file.write(output)
    #     file.close()
     
    bt=st.download_button('Download Code', 
                           data=output,
                           file_name=output_file,
                           mime="py")
     
    if st.button("Regenerate"):
        st.cache_resource.clear()
        st.cache_data.clear()
        st.rerun()
        

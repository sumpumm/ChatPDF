import requests

def upload_file(uploaded_file):
    file_path=None
    response = requests.post(
                "http://127.0.0.1:5000/upload",
                files={"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)},
            )
    response_data=response.json()
    try:
        if response.status_code == 200:
            if "error" in response_data:
                 return {"error": response_data['error']},file_path
            else:
                return {"success": "Files uploaded successfully!"},response_data['file_path']
        else:
            return {"error": f"Request failed with error {response.status_code}"},file_path
    except Exception as e:
            return {"error": f"An error occurred: {e}"},file_path
        
def api_response(token,file_path,user_query,session_id,temp,top_k,prompt):
    payload={"file_path":file_path,"question":user_query,"session_id":session_id,"temperature":temp,"top_k":top_k,"prompt":prompt}
       
    headers = {
    "Authorization": f"Bearer {token}"
    } 
    response=requests.post("http://127.0.0.1:5000/chat",headers=headers,json=payload)
    
    if response.status_code == 200:
        try:
            response_data = response.json()
            response_message = response_data.get('response')
            session_id = response_data.get('session_id')  
        except Exception as e:
            response_message = f"Error: Failed to parse response JSON. {str(e)}"
    else:
        try:
            response_data = response.json()
            response_message = response_data.get('response', "Error response not found")
        except Exception as e:
            response_message = f"Error: Failed to parse error response JSON. {str(e)}"

    return response_message, session_id
        
        
def api_register_user(username, email, full_name, password):
    payload={"username":username,
             "email":email,
             "full_name":full_name,
             "password":password
             }
    response=requests.post("http://127.0.0.1:5000/register",json=payload)
    
    if response.status_code==200:
        try:
            response_data = response.json()
            response_result=response_data.get('result')
            response_message=response_data.get('message')
        except Exception as e:
            response_result=False
            response_message = f"Error: Failed to parse response JSON. {str(e)}"
    else:
        response_data = response.json()
        response_result=response_data.get('result')
        response_message=response_data.get('message')
    
    return response_result,response_message


def api_user_login(username,password):
    payload={"username":username,"password":password}
    response=requests.post("http://127.0.0.1:5000/token",data=payload)
    
    if response.status_code==200:
        response_data=response.json()
        response_token=response_data.get('access_token')
        response_session_id=response_data.get('session_id')
        response_result=response_data.get('success')
        return response_token,response_session_id,response_result
    else:
        response_result=False
        return None,None,response_result
    

def api_user_logout(token: str):
    payload={"token":token}
    response=requests.post("http://127.0.0.1:5000/logout",json=payload)
    
    if response.status_code == 200:
        try:
            response_data=response.json()
            response_data_response=response_data.get('response')
        except Exception as e:
            response_data_response= f"Error: Failed to parse response JSON. {str(e)}"
    else:
        try:
            response_data = response.json()
            response_data_response = response_data.get('response', "Error response not found")
        except Exception as e:
            response_data_response = f"Error: Failed to parse error response JSON. {str(e)}"

    return response_data_response
        
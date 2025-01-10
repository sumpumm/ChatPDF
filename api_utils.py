import requests


def upload_file(uploaded_file):
    file_path=None
    response = requests.post(
                "http://127.0.0.1:8000/upload",
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
        
def api_response(file_path,user_query,session_id,temp,top_k,prompt):
    payload={"file_path":file_path,"question":user_query,"temperature":temp,"top_k":top_k,"prompt":prompt}
    if session_id:
        payload["session_id"]=session_id
        
    response=requests.post("http://127.0.0.1:8000/chat",json=payload)
    
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
        
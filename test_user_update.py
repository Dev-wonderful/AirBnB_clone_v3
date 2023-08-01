#!/usr/bin/python3
"""Testing file
"""
import json
import requests

if __name__ == "__main__":
    """ Get one state
    """
    r = requests.get("http://localhost:5000/api/v1/users")
    r_j = r.json()
    user_id = r_j[0].get('id')

    """ PUT /api/v1/states/<state_id>
    """
    r = requests.put("http://localhost:5000/api/v1/users/{}".format(user_id), data=json.dumps({ 'email': "NewName@gmail.com" }), headers={ 'Content-Type': "application/json" })
    print(r.status_code)
    r_j = r.json()
    print(r_j)
    print(r_j.get('id') == user_id)
    print(r_j.get('email') == "NewName@gmail.com")

    """ Verify if the state is updated
    """
    r = requests.get("http://localhost:5000/api/v1/users")
    r_j = r.json()
    for user_j in r_j:
        if user_j.get('id') == user_id:
            print(user_j.get('email') == "NewName@gmail.com")
            print(user_j)
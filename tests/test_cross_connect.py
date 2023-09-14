from fastapi.testclient import TestClient
from fastapi import HTTPException
from  app.main import app
import requests
import settings
from tests.get_payload import valid_payload, invalid_payload

client = TestClient(app)



# def test_root():
#     response = client.get("/")
#     assert response.status_code == 200
#     assert response.json() == {"message":
#                 "Welcome to QCL Transaction Handler. Please go to "
#                 "'/docs' route for Swagger/OpenAPI Documentation."
#             }
    

# def test_server_ping():
#     response = client.get("/health/server/")
#     assert response.status_code == 200
#     assert response.json() == {"status": "ok"}
    

# def test_server_ping1():
#     response = client.get("/health/server")
#     assert response.status_code == 503
#     assert response == {"detail": "Service Unavailable"}





def test_process_crossconnect_order_invalid_case():
    endpoint = settings.API_BASE_URL + settings.ORDER_SUB_URL
    reponse = requests.post(endpoint, json=invalid_payload)
    assert reponse.status_code == 422


def test_process_crossconnect_order():
    endpoint = settings.API_BASE_URL + settings.ORDER_SUB_URL
    reponse = requests.post(endpoint, json=valid_payload)
    assert reponse.status_code == 200
    valid_payload["qcl_generic_data_object"]["qcl_source_id"] == "ZOH"
    valid_payload["qcl_generic_data_object"]["qcl_source_id"] == "ONS"
    valid_payload["qcl_generic_data_object"]["qcl_destination_id"] == "EQX"
    valid_payload["qcl_generic_data_object"]["qcl_destination_id"] == "CYX"
    




    

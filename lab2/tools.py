from tavily import TavilyClient
from langchain.tools import tool
import csv
import os
from datetime import datetime

tavily_client = TavilyClient()
@tool
def WebSearch(daignoses:str, location:str)->str:
    """search for the nearst hospital based on daignoses and location"""
    query = f"nearest hospital for {daignoses} near {location}"
    response = tavily_client.search(query)
    return response


@tool
def StoreCase(patient_name:str, symptoms:str, summary:str)->str:
    """store the patient case data into a csv file"""
    file_name = "patient_cases.csv"
    file_exists = os.path.exists(file_name)

    with open(file_name, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["timestamp", "patient_name", "symptoms", "summary"])
        if not file_exists:
            writer.writeheader()
        writer.writerow({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "patient_name": patient_name,
            "symptoms": symptoms,
            "summary": summary
        })

    return f"case for {patient_name} stored successfully in {file_name}"
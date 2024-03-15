import os
import json
import numpy as np
import torch
import matplotlib.pyplot as plt

data_folder = "data"

# Process and extract data var
def extract_data(filename, var):
    data = []
    symbol = None
    if filename.endswith(".json"):
        filepath = os.path.join(data_folder, filename)
        
        with open(filepath, 'r') as file:
            try:
                res_data = json.load(file)
            except json.JSONDecodeError:
                print(f"Error decoding JSON from file: {filepath}")

        for _, info in res_data.items():
            symbol = info['ticker'] if not symbol else symbol
            if info['resultsCount'] <= 0: continue
            result = info['results'][0]
            data.append(result[var])
        return symbol, data
    else:
        print(filename)
        return None

var = "vw"
data = []
companies = []
for filename in os.listdir(data_folder):
    symbol, from_json = extract_data(filename, var)
    companies.append(symbol)
    if len(data) <= 0: data = np.array([from_json])
    else: data = np.vstack((data, from_json))

# print(companies)
# print(data)
# fake_data = np.random.rand(10000,10000)
    

def covariance(data):
    n, m = len(data), len(data[0])
    center = np.ones((m,m))/m
    Expects = data @ center
    C = data - Expects
    C = C @ C.T
    return C/(m-1)

def PCA(data, companies):
    C = covariance(data)
    eig_vals, eig_vects = np.linalg.eig(C)
    print(eig_vals)
    idx = np.argsort(eig_vals, axis=0)[::-1]
    print(idx)
    sorted_companies = [companies[i] for i in idx]
    print(sorted_companies)

    cumsum = np.cumsum(eig_vals[idx]) / np.sum(eig_vals[idx])
    xint = range(1, len(cumsum) + 1)
    plt.plot(xint, cumsum)

    plt.xlabel("Number of components")
    plt.ylabel("Cumulative explained variance")
    plt.xticks(xint)
    plt.show()

PCA(data[:10], companies[:10])







            



        

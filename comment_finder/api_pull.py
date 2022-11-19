import pandas as pd
import json
import requests
import argparse
import threading
import queue

api_key = ""

def pull_data(item):
    title, year = item[0], int(item[1])
    url = f'http://www.omdbapi.com/'
    params = {
        "apikey": api_key,
        "t" : title,
        "y" : year,
        'plot' : 'full'
    }
    k = requests.get(url, params=params)
    return json.loads(k.text)

def thread_worker():
    while True:
        try:
            item = q.get(timeout=1)
            data = pull_data(item)
            end_q.put(data)
            print(f'\r{q.qsize()}', end='')
        except queue.Empty:
            break
    return

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="Input csv file to work on, it should have title and year")
    parser.add_argument("api_key", help="api_key")
    parser.add_argument("--save_name", default="out.csv", help="name of save file")
    parser.add_argument("--thread_num", default=20, help="number of threads to work")
    args = parser.parse_args()

    api_key     = args.api_key
    input_csv   = pd.read_csv(args.input_file)
    titles      = input_csv.movie_title.values
    years       = input_csv.movie_release_year.values
    title_year  = [(i,k) for i, k in zip(titles, years)]
    
    q = queue.Queue()
    for k in title_year:
        q.put(k)

    end_q = queue.Queue()

    threads = []
    for _ in range(args.thread_num):
        th = threading.Thread(target=thread_worker, daemon=True)
        th.start()
        threads.append(th)
        
    for each_thread in threads:
        each_thread.join()

    values = []
    while True:
        try:
            res_obj = end_q.get(timeout=1)
            values.append(res_obj)
        except queue.Empty:
            break

    end_df = pd.DataFrame(values)
    end_df.to_csv(args.save_name)
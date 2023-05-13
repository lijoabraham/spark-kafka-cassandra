from time import sleep
from queue_dao import QueueDAO
import pandas as pd

class Producer:
    def run(self):
        dao= QueueDAO('kafka')
        df = pd.read_csv('./data/indexProcessed.csv')
        df.rename(columns={'Index':'s_index', 'Date' : 's_date',
                           'Open' : 'open', 'High' : 'high',
                            'Low' : 'low', 'Close' : 'close', 
                            'Adj Close' : 'adj_close', 'Volume' : 'volume','CloseUSD' : 'close_usd'}, inplace=True)
        for e in range(1000):
            dict_stock = df.sample(1).to_dict(orient="records")[0]
            print(f"data : {str(dict_stock)}")
            # exit("producer end")
            dao.send_message('topic_test', dict_stock)
            sleep(5)

if __name__ == '__main__':
    p = Producer()
    p.run()
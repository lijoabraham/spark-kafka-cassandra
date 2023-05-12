from time import sleep
from queue_dao import QueueDAO
import pandas as pd

# CREATE KEYSPACE IF NOT EXISTS stock_market WITH REPLICATION = { 'class' : 'NetworkTopologyStrategy', 'datacenter1' : 1 };
# USE stock_market;
# CREATE TABLE stock_market.data (    s_index text,     s_date date,     open float,     high float,     low float,     close float,     adj_close float,     volume float,     close_usd float,     PRIMARY KEY (s_date, s_index));

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
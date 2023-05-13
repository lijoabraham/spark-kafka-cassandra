CREATE KEYSPACE IF NOT EXISTS stock_market WITH REPLICATION = { 'class' : 'NetworkTopologyStrategy', 'datacenter1' : 1 };
USE stock_market;
CREATE TABLE stock_market.data (s_index text,s_date date,open float,high float,low float,close float,adj_close float,volume float,close_usd float,PRIMARY KEY (s_date, s_index));


DROP TABLE stock_info_data;

CREATE TABLE stock_info_data (
	trade_date DATE,
	stock_open FLOAT,
	high FLOAT,
	low FLOAT,
	stock_close FLOAT,
	volume INT,
	dividend INT,
	split INT,
	adj_open FLOAT,
	adj_high FLOAT,
	adj_low FLOAT,
	adj_close FLOAT,
	adj_volume INT
);

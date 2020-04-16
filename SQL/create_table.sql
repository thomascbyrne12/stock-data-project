-- creates our table for stock trading data

DROP TABLE stock_info_data;

CREATE TABLE stock_info_data (
	trade_date DATE,
	stock_open FLOAT(32),
	high FLOAT(32),
	low FLOAT(32),
	stock_close FLOAT(32),
	volume INT,
	dividend INT,
	split INT,
	adj_open FLOAT(32),
	adj_high FLOAT(32),
	adj_low FLOAT(32),
	adj_close FLOAT(32),
	adj_volume INT
);

SELECT * FROM stock_info_data;

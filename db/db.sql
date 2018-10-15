CREATE TABLE `Members` (
	`Id`	integer PRIMARY KEY AUTOINCREMENT,
	`F_name`	varchar ( 25 ),
	`L_name`	varchar ( 25 ),
	`Member_no`	varchar ( 10 ) UNIQUE,
	`Phone_no`	varchar ( 10 ),
	`Mem_exp_date`	date,
	`Reach_moment`	varchar ( 6 ),
	`Birth_date`	date,
	`Email`	varchar ( 255 ),
	`Last_donation`	NUMERIC,
	`Date_last_donation`	date,
	`Donation_ok`	varchar ( 6 ),
	`Election_year`	varchar ( 6 ),
	`Comment`	TEXT,
	`Address`	varchar ( 255 )
);
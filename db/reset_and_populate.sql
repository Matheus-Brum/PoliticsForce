DROP TABLE Members;
DROP TABLE Sessions;
DROP TABLE Users;
commit
PRAGMA foreign_keys = ON;
CREATE TABLE Members (
	Id	integer PRIMARY KEY AUTOINCREMENT,
	F_name	varchar ( 25 ),
	L_name	varchar ( 25 ),
	Member_no	varchar ( 10 ) UNIQUE,
	Phone_no	varchar ( 10 ),
	Mem_exp_date	date,
	Reach_moment	varchar ( 6 ),
	Birth_date	date,
	Email	varchar ( 255 ),
	Last_donation	NUMERIC,
	Date_last_donation	date,
	Donation_ok	varchar ( 6 ),
	Election_year	varchar ( 6 ),
	Comment	TEXT,
	Address	varchar ( 255 )
);

CREATE TABLE Sessions (
	Id_session varchar (32) PRIMARY KEY,
	SessionEmail	TEXT,
	FOREIGN KEY (SessionEmail) REFERENCES Members(Email)
);

CREATE TABLE Users (
	Member_no	varchar ( 10 ) UNIQUE PRIMARY KEY,
	Password	varchar ( 128 ),
	Salt		varchar ( 32 ),
	Niveau	INTEGER,
	Circonscription	TEXT,
	FOREIGN KEY(Member_no) REFERENCES Members(Member_no)
);

--MEMBERS ONLY

INSERT INTO Members VALUES (1, 'aa', 'aaa', '1234567890', '1111111111', '01/01/2010', 'midi', '01/01/1990', 'aa@gmail.com', 100, '01/01/2010', 'oui', 'oui', 'testaa', 'H3P2B1,Portland,ME,US');

INSERT INTO Members VALUES (2, 'bb', 'bbb', '1234567891', '2222222222', '01/01/2010', 'midi', '01/01/1990', 'bb@gmail.com', 200, '01/01/2010', 'oui', 'oui', 'testbb', 'h7m3b1,Mont-Joli,QC,CA');

INSERT INTO Members VALUES (3, 'cc', 'ccc', '1234567892', '3333333333', '01/01/2010', 'midi', '01/01/1990', 'cc@gmail.com', 300, '01/01/2010', 'oui', 'oui', 'testcc', '123456,A1A1A1,Alberton,PE,CA');

--A USER FOR TESTS PURPOSES
-- password real value is 'abc'

INSERT INTO Users VALUES ('1234567890', 'ead8096097859e4b593f30471c7ceb16ee884e0a62b331ec863bbb23c24bdfb320678192b2f5511ce06e2ef6c8f75352bb00b6e7a063bce0b1c6976d688743f8', '6477e6a0f6ad4689ad029e140070ccfa', 3, 'Rive-nord');
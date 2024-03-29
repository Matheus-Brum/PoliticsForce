DROP TABLE Members;
DROP TABLE Sessions;
DROP TABLE Users;
DROP TABLE NationalCommittee;
DROP TABLE RegionalCommittee;
DROP TABLE CirconscriptionCommittee;
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
	Address	varchar ( 255 ),
	Committee	varchar (40)
);

CREATE TABLE Sessions (
	Id_session varchar (32) PRIMARY KEY,
	SessionEmail	varchar (255),
	SessionCommittee  varchar (40),
	SessionLevel integer,
	FOREIGN KEY (SessionEmail) REFERENCES Members(Email)
);

CREATE TABLE Users (
	Member_no	varchar ( 10 ) UNIQUE PRIMARY KEY,
	Password	varchar ( 128 ),
	Salt		varchar ( 32 ),
	Level	INTEGER ,
	FOREIGN KEY(Member_no) REFERENCES Members(Member_no)
);

CREATE TABLE NationalCommittee (
    Id integer UNIQUE PRIMARY KEY,
    Name varchar (40) UNIQUE
);

CREATE TABLE RegionalCommittee (
    Id integer UNIQUE PRIMARY KEY,
    Name varchar (40) UNIQUE,
    Parent_id integer,
    FOREIGN KEY(Parent_id) REFERENCES NationalCommittee(Id)
);

CREATE TABLE CirconscriptionCommittee (
    Id integer UNIQUE PRIMARY KEY,
    Name varchar (40) UNIQUE,
    Parent_id integer,
    FOREIGN KEY(Parent_id) REFERENCES CirconscriptionCommittee(Id)
);

--MEMBERS ONLY
--empty row for admin purposes
--INSERT INTO Members VALUES (1, null, null, '9999999999', null, null, null, null, null, null, null, null, null, null, null, null);

INSERT INTO Members VALUES (2, 'aa', 'aaa', '1234567890', '1111111111', '01/01/2010', 'midi', '01/01/1990', 'aa@gmail.com', 100, '01/01/2010', 'oui', 'oui', 'testaa', 'H3P2B1,Portland,ME,US', 'Canada');

INSERT INTO Members VALUES (3, 'bb', 'bbb', '1234567891', '2222222222', '01/01/2010', 'midi', '01/01/1990', 'bb@gmail.com', 200, '01/01/2010', 'oui', 'oui', 'testbb', 'h7m3b1,Mont-Joli,QC,CA', 'Ontario');

INSERT INTO Members VALUES (4, 'cc', 'ccc', '1234567892', '3333333333', '01/01/2010', 'midi', '01/01/1990', 'cc@gmail.com', 300, '01/01/2010', 'oui', 'oui', 'testcc', '123456,A1A1A1,Alberton,PE,CA', 'Toronto');

INSERT INTO Members VALUES (5, 'dd', 'ddd', '1234567893', '4444444444', '01/01/2010', 'midi', '01/01/1990', 'dd@gmail.com', 400, '01/01/2010', 'oui', 'oui', 'testdd', 'G4A1F5,Laval,QC,CA', 'Québec');

--COMMITTEES
INSERT INTO NationalCommittee VALUES (1, 'Canada');

INSERT INTO RegionalCommittee VALUES (1, 'Ontario', 1);

INSERT INTO RegionalCommittee VALUES (2, 'Québec', 1);

INSERT INTO CirconscriptionCommittee VALUES (1, 'Toronto', 1);

--ADMIN ACCOUNT

-- password real value is 'admin123'
INSERT INTO Users VALUES ('9999999999', '65779326784d5d4163bdc2a12f2dee671280c81858043d30ac548a1c2036a50101523c07aeeb47d61c1ee3833c747ddfb1625a97ab73755a2f1e72fad611d14c', '0e11af9e6aba48ef870ec3ac338c568d', 4);

--A USER FOR TESTS PURPOSES

-- password real value is 'abc'
INSERT INTO Users VALUES ('1234567890', 'ead8096097859e4b593f30471c7ceb16ee884e0a62b331ec863bbb23c24bdfb320678192b2f5511ce06e2ef6c8f75352bb00b6e7a063bce0b1c6976d688743f8', '6477e6a0f6ad4689ad029e140070ccfa', 3);

-- password real value is 'def'
INSERT INTO Users VALUES ('1234567893', '303cb8e6c3615b01acfaa3378f4d9abc829d5ef1b2bd351d3c14a48f7dcf7085da1a40a184b8d9958f4f76d60a64b32568eddd7098377b6e1c8bc49359e6d1ea', 'cf3cade5a613459f9e91cb02b4cb4842', 2);

-- Create the event_type table
CREATE TABLE event_type (
  type_id SERIAL PRIMARY KEY,
  type_title TEXT NOT NULL
);

-- Insert data into the event_type table
INSERT INTO event_type (type_title) VALUES
('Technical'),
('Gaming'),
('Cultural'),
('Sports'),
('Trivia');


-- Create the location table
CREATE TABLE location (
  location_id SERIAL PRIMARY KEY,
  location_name VARCHAR(100) NOT NULL
);

-- Insert data into the location table
INSERT INTO location (location_name) VALUES
('Main Auditorium'),
('Mini Auditorium'),
('COEP Ground'),
('Academic Complex'),
('Cognizant Lab');


-- Create the branch table
CREATE TABLE branch (
  branch_id SERIAL PRIMARY KEY,
  branch_name VARCHAR(30) NOT NULL
);

-- Insert data into the branch table
INSERT INTO branch (branch_name) VALUES
('Civil'),
('Computer'),
('Electrical'),
('E&TC'),
('Instrumentation'),
('Mechanical'),
('Metallurgy'),
('Production');


-- Create the events table
CREATE TABLE events (
  event_id SERIAL PRIMARY KEY,
  event_title VARCHAR(100) NOT NULL,
  event_price INT NOT NULL,
  participants INT NOT NULL,
  type_id INT NOT NULL,
  location_id INT NOT NULL,
  date DATE NOT NULL
);

-- Add foreign key constraint for type_id
ALTER TABLE events
  ADD CONSTRAINT fk_event_type
  FOREIGN KEY (type_id)
  REFERENCES event_type(type_id)
  ON DELETE CASCADE;

-- Add foreign key constraint for location_id
ALTER TABLE events
  ADD CONSTRAINT fk_location
  FOREIGN KEY (location_id)
  REFERENCES location(location_id);

-- Insert data into the events table
INSERT INTO events (event_title, event_price, participants, type_id, location_id, date) VALUES
('Codeathon', 50, 10, 1, 1, '2024-05-06'),
('Esports Tournament', 50, 15, 2, 2, '2024-05-07'),
('Art Exhibition', 50, 10, 3, 3, '2024-05-08'),
('Charity Fun Run', 50, 10, 4, 4, '2024-05-09'),
('Tech Talk Series', 50, 15, 1, 3, '2024-05-10'),
('Knowledge Challenge: Trivia Night', 50, 10, 5, 5, '2024-05-11');


-- Create the participants table
CREATE TABLE participants (
  p_id SERIAL PRIMARY KEY,
  event_id INT NOT NULL,
  fullname VARCHAR(100) NOT NULL,
  email VARCHAR(300) NOT NULL,
  mobile CHAR(10) NOT NULL,
  college VARCHAR(300) NOT NULL,
  branch_id INT NOT NULL,
);

-- Add foreign key constraint for event_id
ALTER TABLE participants
  ADD CONSTRAINT fk_event
  FOREIGN KEY (event_id)
  REFERENCES events(event_id)
  ON DELETE CASCADE;

-- Add foreign key constraint for branch_id
ALTER TABLE participants
  ADD CONSTRAINT fk_branch
  FOREIGN KEY (branch_id)
  REFERENCES branch(branch_id);


-- Create the admin table
CREATE TABLE admin (
  username VARCHAR(100) PRIMARY KEY,
  password VARCHAR(100) NOT NULL
);

-- Insert data into the admin table
INSERT INTO admin (username, password) VALUES
('Admin1', 'password1'),
('Admin2', 'password2');

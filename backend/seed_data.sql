-- SQLite seed data
-- Contains both positive (income) and negative (expense) absolute values
-- Uses proper transaction types and categories for the ML model to rely on

INSERT INTO transactions (description, amount, transaction_type, category, auto_tagged, status, timestamp, created_at, updated_at, is_duplicate) VALUES 
('Monthly Salary Direct Deposit', 4500.00, 'income', 'salary', 1, 'categorized', datetime('now', '-5 days'), datetime('now', '-5 days'), datetime('now', '-5 days'), 0),
('Uber Ride to Airport', -35.50, 'expense', 'transportation', 1, 'categorized', datetime('now', '-4 days'), datetime('now', '-4 days'), datetime('now', '-4 days'), 0),
('Whole Foods Market Groceries', -125.40, 'expense', 'groceries', 1, 'categorized', datetime('now', '-3 days'), datetime('now', '-3 days'), datetime('now', '-3 days'), 0),
('Netflix Standard Subscription', -15.49, 'expense', 'entertainment', 1, 'categorized', datetime('now', '-2 days'), datetime('now', '-2 days'), datetime('now', '-2 days'), 0),
('Apartment Rent', -1400.00, 'expense', 'rent', 1, 'categorized', datetime('now', '-2 days'), datetime('now', '-2 days'), datetime('now', '-2 days'), 0),
('Freelance Design Work', 850.00, 'income', 'salary', 0, 'verified', datetime('now', '-1 days'), datetime('now', '-1 days'), datetime('now', '-1 days'), 0),
('Starbucks Morning Coffee', -5.75, 'expense', 'dining', 1, 'categorized', datetime('now'), datetime('now'), datetime('now'), 0),
-- Last Month
('Monthly Salary Direct Deposit', 4500.00, 'income', 'salary', 1, 'categorized', datetime('now', '-1 month'), datetime('now', '-1 month'), datetime('now', '-1 month'), 0),
('Apartment Rent', -1400.00, 'expense', 'rent', 1, 'categorized', datetime('now', '-1 month', '+2 days'), datetime('now', '-1 month', '+2 days'), datetime('now', '-1 month', '+2 days'), 0),
('Electric Bill', -85.20, 'expense', 'utilities', 0, 'verified', datetime('now', '-1 month', '+5 days'), datetime('now', '-1 month', '+5 days'), datetime('now', '-1 month', '+5 days'), 0),
('Dinner at Gordon Ramsay', -210.00, 'expense', 'dining', 1, 'categorized', datetime('now', '-1 month', '+15 days'), datetime('now', '-1 month', '+15 days'), datetime('now', '-1 month', '+15 days'), 0),
-- Three Months Ago
('Monthly Salary Direct Deposit', 4500.00, 'income', 'salary', 1, 'categorized', datetime('now', '-3 months'), datetime('now', '-3 months'), datetime('now', '-3 months'), 0),
('Apartment Rent', -1400.00, 'expense', 'rent', 1, 'categorized', datetime('now', '-3 months', '+2 days'), datetime('now', '-3 months', '+2 days'), datetime('now', '-3 months', '+2 days'), 0),
('Target Store Run', -89.43, 'expense', 'shopping', 1, 'categorized', datetime('now', '-3 months', '+12 days'), datetime('now', '-3 months', '+12 days'), datetime('now', '-3 months', '+12 days'), 0),
('Uber Ride Home', -22.50, 'expense', 'transportation', 1, 'categorized', datetime('now', '-3 months', '+16 days'), datetime('now', '-3 months', '+16 days'), datetime('now', '-3 months', '+16 days'), 0),
-- Six Months Ago
('Monthly Salary Direct Deposit', 4500.00, 'income', 'salary', 1, 'categorized', datetime('now', '-6 months'), datetime('now', '-6 months'), datetime('now', '-6 months'), 0),
('Apartment Rent', -1400.00, 'expense', 'rent', 1, 'categorized', datetime('now', '-6 months', '+2 days'), datetime('now', '-6 months', '+2 days'), datetime('now', '-6 months', '+2 days'), 0),
('Flight to New York', -450.00, 'expense', 'travel', 0, 'verified', datetime('now', '-6 months', '+10 days'), datetime('now', '-6 months', '+10 days'), datetime('now', '-6 months', '+10 days'), 0),
('Freelance Client Bonus', 1500.00, 'income', 'salary', 0, 'verified', datetime('now', '-6 months', '+20 days'), datetime('now', '-6 months', '+20 days'), datetime('now', '-6 months', '+20 days'), 0),
-- One Year Ago (12 Months)
('Monthly Salary Direct Deposit', 4200.00, 'income', 'salary', 1, 'categorized', datetime('now', '-12 months'), datetime('now', '-12 months'), datetime('now', '-12 months'), 0),
('Apartment Rent', -1350.00, 'expense', 'rent', 1, 'categorized', datetime('now', '-12 months', '+2 days'), datetime('now', '-12 months', '+2 days'), datetime('now', '-12 months', '+2 days'), 0),
('New Laptop', -1299.99, 'expense', 'shopping', 1, 'categorized', datetime('now', '-12 months', '+11 days'), datetime('now', '-12 months', '+11 days'), datetime('now', '-12 months', '+11 days'), 0),
-- 18 Months Ago
('Monthly Salary Direct Deposit', 4200.00, 'income', 'salary', 1, 'categorized', datetime('now', '-18 months'), datetime('now', '-18 months'), datetime('now', '-18 months'), 0),
('Apartment Rent', -1350.00, 'expense', 'rent', 1, 'categorized', datetime('now', '-18 months', '+2 days'), datetime('now', '-18 months', '+2 days'), datetime('now', '-18 months', '+2 days'), 0),
('Car Insurance', -150.00, 'expense', 'insurance', 1, 'categorized', datetime('now', '-18 months', '+14 days'), datetime('now', '-18 months', '+14 days'), datetime('now', '-18 months', '+14 days'), 0),
-- Two Years Ago (24 Months)
('Monthly Salary Direct Deposit', 4000.00, 'income', 'salary', 1, 'categorized', datetime('now', '-24 months'), datetime('now', '-24 months'), datetime('now', '-24 months'), 0),
('Apartment Rent', -1300.00, 'expense', 'rent', 1, 'categorized', datetime('now', '-24 months', '+2 days'), datetime('now', '-24 months', '+2 days'), datetime('now', '-24 months', '+2 days'), 0),
('Birthday Dinner', -180.50, 'expense', 'dining', 1, 'categorized', datetime('now', '-24 months', '+22 days'), datetime('now', '-24 months', '+22 days'), datetime('now', '-24 months', '+22 days'), 0);

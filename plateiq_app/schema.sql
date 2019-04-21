DROP TABLE IF EXISTS invoices;

CREATE TABLE invoices (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  seller TEXT NOT NULL,
  buyer TEXT NOT NULL,
  description TEXT,
  digitized INTEGER NOT NULL,
  invoice_datetime datetime default current_timestamp
);

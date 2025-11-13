# Mechanic Shop

## Entities

- Tech
- Customer
- Invoice
- Junction Table: invoice_mechanic

## Entity Attributes

- Tech: ID, name, title
- Customer: ID, first_name, last_name, email, address, phone_number
- Invoice: ID, date, status, total_cost, customer_id, vehicle
- Junction Table: invoice_mechanic: invoice_id, tech_id

## Relationships

- Customer -> 1tM Invoice
- Tech -> MtM Invoice (via invoice_mechanic)

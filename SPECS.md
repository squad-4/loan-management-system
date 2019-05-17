# Client and Loan Management System

## Objective

The main objective of this project is to create an API to manage clients and the loan payments control system from a fin-tech.

## Purpose

The purpose of this challenge is to test your ability to implement a solution given an abstract problem. You may find a problem in the asked task that you need to explain the problem and propose a solution to fix it.

## Problem

A fin-tech needs to create and manage the clients and keep track of the amount of money loaned and the missed/made payments. It also needs a place to retrieve the volume of outstanding debt at some point in time.

## Business Rules

- If a client contracted a loan in the past and paid all without missing any payment, you can decrease by 0.02% his tax rate.
- If a client contracted a loan in the past and paid all but missed until 3 monthly payments, you can increase by 0.04% his tax rate.
- If a client contracted a loan in the past and paid all but missed more than 3 monthly payments or didn’t pay all the loan, you need to deny the new one. 

## Limitations

Loans are paid back in monthly instalments.

## Endpoints

### POST /clients

#### Summary

Create a client in the system.

#### Payload

- **name**: the client name.
- **surname**: the client surname.
- **email**: the client email.
- **telephone**: the client telephone.
- **cpf**: the client (Cadastro de Pessoa Física) identification.

#### Example of sent data

```json
{
    "name": "Felicity",
    "surname": "Jones",
    "email": "felicity@gmail.com",
    "telephone": "11984345678",
    "cpf": "34598712387"
}
```

#### Reply

- **client_id**: unique id of a client. 

#### Example of received data

```json
{
    "client_id": 1
}
```

### POST /loans

#### Summary

Create a loan application. Loans are automatically accepted.

#### Payload


- **client_id**: the client's identification that contracted a loan.
- **amount**: loan amount in dollars.
- **term**: number of months that will take until the loan gets paid-off.
- **rate**: interest rate as decimal.
- **date**: when the loan was requested (origination date as an ISO 8601 string). 

#### Example of sent data

```json
{
    "client_id": 1,
    "amount": 1000,
    "term": 12,
    "rate": 0.05,
    "date": "2019-05-09 03:18Z"
}
```

#### Reply

- **loan_id**: unique id of the loan.
- **instalment**: monthly loan payment.

#### Example of received data

```json
{
    "loan_id": "000-0000-0000-0000",
    "instalment": 85.60
}
```

#### Notes

**Loan payment formula**

```
r = rate / term
instalment = [r + r / ((1 + r) ^ term - 1)] x amount
```

**Example**

For repaying a loan of $1000 at 5% interest for 12 months, the equation would be:

```
instalment = [(0.05 / 12) + (0.05 / 12) / ((1 + (0.05 / 12)) ^ 12 - 1] x 1000
instalment = 85.60  
```

### POST /loans/<:id>/payments

#### Summary

Create a record of a payment made or missed.

#### Payload

- **payment**: type of payment: made or missed.
- **date**: payment date.
- **amount**: amount of the payment made or missed in dollars.

#### Example of sent data (Payment made)

```json
{
    "payment": "made",
    "date": "2019-05-07 04:18Z",
    "amount": 85.60
}
```

#### Example of sent data (Payment missed)

```json
{
    "payment": "missed",
    "date":  "2019-05-07 04:18Z",
    "amount": 85.60
}
```

### POST /loans/<:id>/balance

#### Summary

Get the volume of outstanding debt (i.e., debt yet to be paid) at some point in time.

#### Payload

- date: loan balance until this date.

#### Example of sent data

```json
{
    "date": "2017-09-05 02:18Z"
}
```

#### Reply

- balance: outstanding debt of loan.

#### Example

```json
{
    "balance": 40
}
```

# 📄 Documentation: Form Automation & Notification System

## 🔹 Project Overview

This project automates the collection and handling of form submissions. When a user fills out a form (Google Form or custom HTML form), the system:

1. Stores the data into a database (Google Sheets or MySQL).
2. Sends an automatic confirmation email to the user.
3. Notifies the admin about the new registration.

The automation is powered by **n8n**.

---

## 🔹 Workflow Steps

1. **Webhook** – Captures the submitted form data.
2. **Database/Google Sheets** – Saves the form data into a structured record.
3. **User Email** – Sends a confirmation email to the user.
4. **Admin Email** – Sends a notification email to the admin.
5. **Webhook Response** – Sends a success message back to the frontend.

---

## 🔹 Node Details

### 1. Webhook Node

* Acts as the entry point for the workflow.
* Receives form data (name, email, phone, city, education, course).
* Triggered whenever a user submits the form.

---

### 2. Database / Google Sheets Node

* Stores each form submission.
* Each row/record contains the user’s details and submission time.
* Acts as the system’s data source for future reference.

---

### 3. Gmail Node (User Confirmation)

* Sends an automatic confirmation email to the user.
* Includes personalized details (like their name and selected course).
* Improves trust and ensures the user knows their form was received.

---

### 4. Gmail Node (Admin Notification)

* Notifies the admin about a new registration.
* Contains all the submitted details.
* Ensures the admin team can follow up quickly.

---

### 5. Respond to Webhook Node

* Sends a response back to the form frontend.
* Displays a confirmation message such as:
  *“Your registration has been received successfully.”*

---

## 🔹 Workflow Diagram

```
[ User Form Submission ]
          │
          ▼
   (Webhook Node)
          │
          ▼
(Database / Google Sheets)
          │
          ▼
(User Email) → (Admin Email)
          │
          ▼
 (Respond to Webhook)
```

---

## 🔹 Benefits of the System

* **Automation** – No need for manual handling of form submissions.
* **Data Centralization** – All entries stored in a database or spreadsheet.
* **Instant Feedback** – Users receive an immediate confirmation email.
* **Admin Awareness** – Admins are notified instantly about new submissions.
* **Scalability** – Can be connected with Slack, Telegram, Discord, or other channels for alerts.



# SQL-vuln-lab
An intentionally vulnerable Flask &amp; SQLite application for learning and practicing SQL Injection in a safe, local lab environment.




# Kingdom SQL Injection Lab

A deliberately vulnerable web application built with **Flask** and **SQLite** to provide a realistic environment for studying SQL Injection attacks and secure authentication mechanisms. The project is intended for cybersecurity education, university laboratories, workshops, and CTF-style training.

---

## Overview

Modern web applications frequently interact with databases, making SQL Injection one of the most important vulnerabilities every security professional should understand.

This lab recreates a simplified authentication system that intentionally contains insecure database queries. Students can safely analyze vulnerable code, observe application behavior, exploit the flaw in a controlled environment, and understand how proper defensive coding prevents the attack.

The application is designed for educational use only and should never be exposed to the public Internet.

---

## Features

* Intentionally vulnerable authentication system
* SQLite backend
* Flask-based web application
* Automatic database generation
* Secure and insecure query comparison
* Beginner-friendly project structure
* Suitable for demonstrations, practical classes and self-learning

---

## Learning Outcomes

After completing this lab, students should be able to:

* Understand how SQL Injection works
* Identify vulnerable SQL queries
* Analyze insecure authentication logic
* Extract information from backend databases
* Understand authentication bypass techniques
* Compare insecure queries with parameterized statements
* Apply secure coding practices to prevent SQL Injection

---

# Requirements

* Python 3.10 or later
* pip
* Flask

---

# Installation

Clone the repository.

```bash
git clone https://github.com/<your-username>/kingdom-sqli-lab.git
```

Move into the project directory.

```bash
cd kingdom-sqli-lab
```

Create a virtual environment (recommended).

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### Windows

```powershell
python -m venv venv
venv\Scripts\activate
```

Install dependencies.

```bash
pip install -r requirements.txt
```

or

```bash
pip install Flask
```

---

# Running the Lab

Start the application.

```bash
python app.py
```

The server starts on:

```
http://127.0.0.1:8080
```

Open the above address in your browser.

On the first execution, the application automatically creates the SQLite database if it does not already exist.

---

# Project Structure

```
kingdom-sqli-lab
│
├── app.py
├── requirements.txt
├── README.md
├── LICENSE
└── kingdom_lab.db        # Generated automatically
```

---

# Vulnerable Code Example

The following authentication logic intentionally concatenates user-controlled input into an SQL query.

```python
query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
cursor.execute(query)
```

This implementation is **deliberately insecure** and exists solely for educational purposes.

Later in the lab, students can compare this approach with parameterized SQL statements to understand the recommended mitigation.

---

# Intended Environment

This project should only be executed in isolated environments such as:

* Localhost
* Virtual Machines
* University laboratory systems
* Personal learning environments
* CTF practice machines

---

# Security Notice

> **Warning**
>
> This application intentionally contains security vulnerabilities.
>
> Never deploy this project on a production server, cloud instance, VPS, public hosting platform, or any Internet-accessible environment.
>
> The code is intentionally insecure to support cybersecurity education and should only be executed inside an isolated laboratory.

---

# Educational Use Policy

This repository has been developed to assist students, instructors and cybersecurity enthusiasts in understanding offensive and defensive application security concepts.

Users are expected to:

* Use the project responsibly.
* Practice only in environments they own or are authorized to test.
* Follow applicable laws and institutional policies.
* Respect responsible disclosure principles.

The author does not encourage or endorse unauthorized testing of third-party systems.

---

# Contributing

Contributions that improve the educational value of the project are welcome.

Possible improvements include:

* Additional SQL Injection scenarios
* Blind SQL Injection modules
* UNION-based exercises
* Error-based demonstrations
* Secure implementation examples
* Docker support
* Automated lab deployment
* Better UI and documentation

Please open an Issue or submit a Pull Request.

---

# License

Distributed under the MIT License.

---

# Author

**Sriman Kundu**

Cybersecurity Student • Ethical Hacking • Application Security

---

If you find this project useful for learning or teaching, consider giving the repository a ⭐ to support future educational security labs.

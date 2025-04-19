# 💻 PyTaskMan

**PyTaskMan** is a simple command-line program written in Python that helps you manage your tasks directly from the Terminal. Add, update, mark or delete tasks, and organize them by their current status: `todo`, `in progress`, or `done`.

---

## 🚀 Features

- Add new tasks with ease
- Update task details
- Mark task status
- Delete completed or irrelevant tasks
- List tasks by:
  - Status (`todo`, `in progress`, `done`)
  - All tasks

---

## 🛠 Installation

1. Make sure you have **Python 3** installed on your machine.
2. Download `pytaskman.py` from this repository.
3. Open a terminal or command prompt and run the script:

```bash
python pytaskman.py
```

## 💡 Usage Example

Let’s say you have a busy week coming up. You can quickly jot down all the tasks you need to complete:

```bash
PyTaskMan> add Finish Python project
Task added successfully (ID: 1)

PyTaskMan> add Read AI research paper
Task added successfully (ID: 2)
```

Later in the week, mark or update tasks as they move forward:

```bash
PyTaskMan> mark 1 in progress
Task marked in progress successfully (ID: 1)

PyTaskMan update 2 Annotate AI research paper
Task updated successfully (ID: 2)
```

You can list tasks by status:

```bash
PyTaskMan> list in progress
Tasks [in progress]:
[1] Finish Python project - Status: IN PROGRESS
```

Or view all tasks:

```bash
PyTaskMan> list
All Tasks:
[1] Finish Python project - Status: IN PROGRESS
[2] Read AI research paper - Status: DONE
```

---

## 🧰 Technologies Used

- Python 3.13.3
- Standard Libraries:
  - `os` – Interacting with the operating system
  - `sys` – Command-line argument handling
  - `json` – Storing and loading task data
  - `time` – Timestamping tasks or managing time-based data

---

## 🤝 Contributing

Contributions, suggestions, and improvements are welcome!

To contribute:

1. Fork the repository
2. Create a new branch (`git checkout -b feature-name`)
3. Commit your changes (`git commit -m "Add feature"`)
4. Push to the branch (`git push origin feature-name`)
5. Open a Pull Request

For major changes, please open an issue first to discuss what you'd like to add or modify.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).  
You are free to use, modify, and distribute it with proper attribution.

---

**🐍 Made with Python by [Ayden Powell](https://github.com/Elio-togm)**
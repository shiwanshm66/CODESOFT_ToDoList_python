import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk
import json
import os

TASKS_FILE = "tasks.json"

def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as file:
            tasks = json.load(file)
            for task in tasks:
                task_list.insert("", "end", values=(task["task"], task["priority"], task["status"]))
    else:
        with open(TASKS_FILE, "w") as file:
            json.dump([], file)

def save_tasks():
    tasks = []
    for child in task_list.get_children():
        task_data = task_list.item(child)["values"]
        tasks.append({"task": task_data[0], "priority": task_data[1], "status": task_data[2]})
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file)

def add_task():
    task = task_entry.get()
    priority = priority_combo.get()
    if task != "":
        task_list.insert("", "end", values=(task, priority, "❌ Not Done"))
        task_entry.delete(0, tk.END)
        priority_combo.set("Medium")
        save_tasks()
    else:
        messagebox.showwarning("Warning", "Task cannot be empty!")

def delete_task():
    selected_item = task_list.selection()
    if selected_item:
        task_list.delete(selected_item)
        save_tasks()
    else:
        messagebox.showwarning("Warning", "Select a task to delete!")

def mark_done():
    selected_item = task_list.selection()
    if selected_item:
        for item in selected_item:
            values = list(task_list.item(item, "values"))
            values[2] = "✔️ Done"
            task_list.item(item, values=values)
        save_tasks()
    else:
        messagebox.showwarning("Warning", "Select a task to mark done!")

def mark_undone():
    selected_item = task_list.selection()
    if selected_item:
        for item in selected_item:
            values = list(task_list.item(item, "values"))
            values[2] = "❌ Not Done"
            task_list.item(item, values=values)
        save_tasks()
    else:
        messagebox.showwarning("Warning", "Select a task to mark undone!")

def edit_task():
    selected_item = task_list.selection()
    if selected_item:
        current_task = task_list.item(selected_item, "values")[0]
        new_task = simpledialog.askstring("Edit Task", "Modify task:", initialvalue=current_task)
        if new_task:
            values = list(task_list.item(selected_item, "values"))
            values[0] = new_task
            task_list.item(selected_item, values=values)
            save_tasks()
    else:
        messagebox.showwarning("Warning", "Select a task to edit!")

root = tk.Tk()
root.title("✅ Full-Fledged To-Do List App")
root.geometry("650x500")
root.config(bg="#f9f9f9")

title_label = tk.Label(root, text="📝 To-Do List", font=("Helvetica", 20, "bold"), bg="#f9f9f9")
title_label.pack(pady=10)

input_frame = tk.Frame(root, bg="#f9f9f9")
input_frame.pack(pady=5)

task_entry = tk.Entry(input_frame, font=("Helvetica", 14), width=25)
task_entry.grid(row=0, column=0, padx=5)

priority_combo = ttk.Combobox(input_frame, values=["High", "Medium", "Low"], font=("Helvetica", 12), width=10)
priority_combo.set("Medium")
priority_combo.grid(row=0, column=1, padx=5)

add_button = tk.Button(input_frame, text="Add Task", command=add_task, bg="#4CAF50", fg="white", font=("Helvetica", 12))
add_button.grid(row=0, column=2, padx=5)

columns = ("Task", "Priority", "Status")
task_list = ttk.Treeview(root, columns=columns, show="headings", height=12)

for col in columns:
    task_list.heading(col, text=col)
    task_list.column(col, width=180 if col == "Task" else 100, anchor="center")

task_list.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

scrollbar = ttk.Scrollbar(root, orient="vertical", command=task_list.yview)
task_list.configure(yscroll=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

button_frame = tk.Frame(root, bg="#f9f9f9")
button_frame.pack(pady=10)

tk.Button(button_frame, text="Mark Done", command=mark_done, width=12, bg="#2196F3", fg="white").grid(row=0, column=0, padx=5)
tk.Button(button_frame, text="Mark Undone", command=mark_undone, width=12, bg="#FF9800", fg="white").grid(row=0, column=1, padx=5)
tk.Button(button_frame, text="Edit Task", command=edit_task, width=12, bg="#9C27B0", fg="white").grid(row=0, column=2, padx=5)
tk.Button(button_frame, text="Delete Task", command=delete_task, width=12, bg="#f44336", fg="white").grid(row=0, column=3, padx=5)

load_tasks()

root.mainloop()

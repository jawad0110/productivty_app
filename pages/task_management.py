import flet as ft
import json
import os
import schedule
import time
from datetime import datetime
from plyer import notification
from .tasks.add_task import add_task_win

def save_tasks(tasks):
    with open('json/tasks.json', 'w') as file:
        json.dump(tasks, file)

def load_tasks():
    if os.path.exists('json/tasks.json'):
        with open('json/tasks.json', 'r') as file:
            return json.load(file)
    return []

def delete_task(task, tasks):
    tasks.remove(task)
    save_tasks(tasks)

def notify_task(task):
    notification.notify(
        title="Task Reminder",
        message=f"Reminder: {task['title']}",
        timeout=10
    )
    
    # Mark the task as notified and save
    task['notified'] = True
    save_tasks(load_tasks())
    
    # Cancel the scheduled job for this task
    for job in schedule.get_jobs():
        if job.tags and job.tags[0] == task['title']:
            schedule.cancel_job(job)
            break

def schedule_task(task):
    # Convert task time to datetime
    task_datetime_str = f"{task['date']} {task['time']}"
    task_datetime = datetime.strptime(task_datetime_str, "%Y-%m-%d %I:%M %p")
    
    if task_datetime > datetime.now() and not task.get('notified', False):
        # Calculate the time difference in seconds
        schedule_time = (task_datetime - datetime.now()).total_seconds()
        if schedule_time > 0:  # Only schedule if the time is in the future
            # Schedule the task with the remaining time
            job = schedule.every(schedule_time).seconds.do(notify_task, task).tag(task['title'])
            return job

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)  # Check every second

def tasks_btn(page, task, tasks, tasks_column):
    categories = ["Done", "In Progress", "To Do", "Canceled"]

    def get_background_color(status):
        colors = {
            "Done": "#4CAF50",
            "In Progress": "#2196F3",
            "To Do": "#9E9E9E",
            "Canceled": "#F44336"
        }
        return colors.get(status, "#4CAF50")

    def update_status(selected_status):
        task["status"] = selected_status
        status_dropdown.value = selected_status
        status_dropdown.bgcolor = get_background_color(selected_status)
        save_tasks(tasks)
        page.update()

    def get_priority_background_color(priority):
        colors = {
            "Low": "#9E9E9E",
            "Medium": "#FFA808",
            "High": "#F44336"
        }
        return colors.get(priority, "#9E9E9E")

    def update_priority(selected_priority):
        task["priority"] = selected_priority
        priority_dropdown.value = selected_priority
        priority_dropdown.bgcolor = get_priority_background_color(selected_priority)
        save_tasks(tasks)
        page.update()

    def delete_task_handler(e):
        delete_task(task, tasks)
        tasks_column.controls.remove(task_container)
        save_tasks(tasks)
        page.update()

    initial_status = task.get("status", "To Do")  # Default to "To Do"

    status_dropdown = ft.Dropdown(
        label="Status",
        hint_text="Choose status",
        options=[
            ft.dropdown.Option(cat, on_click=lambda e, cat=cat: update_status(cat))
            for cat in categories
        ],
        value=initial_status,
        width=140,
        height=60,
        bgcolor=get_background_color(initial_status),
        border_radius=20
    )

    priority_categories = ["Low", "Medium", "High"]

    initial_priority = task.get("priority", "Low")  # Default to "Low"

    priority_dropdown = ft.Dropdown(
        label="Priority",
        hint_text="Choose priority",
        options=[
            ft.dropdown.Option(cat, on_click=lambda e, cat=cat: update_priority(cat))
            for cat in priority_categories
        ],
        value=initial_priority,
        width=145,
        height=60,
        bgcolor=get_priority_background_color(initial_priority),
        border_radius=20
    )

    task_container = ft.Container(
        margin=10,
        padding=10,
        bgcolor='#6c757d',
        width=325,
        height=165,
        border_radius=12,
        alignment=ft.alignment.center_left,
        content=ft.Row(
            controls=[
                ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Text(
                                    value=task["title"],
                                    size=25,
                                    color="Black",
                                    font_family="Nohemi Bold"
                                ),
                                ft.IconButton(
                                    icon=ft.icons.DELETE,
                                    icon_color="#F44336",
                                    icon_size=30,
                                    on_click=delete_task_handler,
                                )
                            ],
                            expand=False,
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            vertical_alignment=ft.CrossAxisAlignment.END
                        ),
                        ft.Row(
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.Text(
                                            value=task["time"],
                                            size=15,
                                            color="#3B3B3B",
                                            font_family="Nohemi Light"
                                        )
                                    ]
                                ),
                                ft.Container(width=10),
                                ft.Text(
                                    value=task["date"],
                                    size=15,
                                    color="#3B3B3B",
                                    font_family="Nohemi Light"
                                )
                            ]
                        ),
                        ft.Row(
                            controls=[
                                ft.Row(
                                    controls=[status_dropdown],
                                ),
                                ft.Row(
                                    controls=[priority_dropdown],
                                )
                            ],
                            expand=False,
                        )
                    ],
                    expand=True
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.END
        )
    )
    return task_container

def TaskManagementPage(page: ft.Page):

    def on_column_scroll(e: ft.OnScrollEvent):
        pass
    
    page.fonts = {
        "Nohemi Black": "fonts/Nohemi-Black.ttf",
        "Nohemi Bold": "fonts/Nohemi-Bold.ttf",
        "Nohemi Regular": "fonts/Nohemi-Regular.ttf",
        "Nohemi Light": "fonts/Nohemi-Light.ttf"
    }

    tasks_column = ft.Column()

    tasks = load_tasks()
    
    def add_new_task(task_title, task_time, task_date):
        if task_title:
            task = {
                "title": task_title,
                "time": task_time,
                "date": task_date,
                "status": "To Do",
                "priority": "Low"  # Default priority
            }
            tasks.append(task)
            task_btn = tasks_btn(page, task, tasks, tasks_column)
            tasks_column.controls.append(task_btn)
            save_tasks(tasks)
            page.update()

            # Schedule the task
            schedule_task(task)

    add_task_dialog, show_add_task = add_task_win(page, add_new_task)

    for task in tasks:
        task_btn = tasks_btn(page, task, tasks, tasks_column)
        tasks_column.controls.append(task_btn)
        # Schedule the task
        schedule_task(task)

    return ft.View(
        route="/task_management",
        scroll=ft.ScrollMode.ALWAYS,
        on_scroll=on_column_scroll,
        controls=[
            ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.IconButton(
                                icon=ft.icons.HOME,
                                icon_color="#D9D9D9",
                                icon_size=30,
                                on_click=lambda _: page.go("/"),
                            ),
                            ft.Text(
                                " Task Management",
                                size=27,
                                font_family="Nohemi Black",
                                color="White",
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,  # Center the header horizontally
                        spacing=10,  # Adjust spacing as needed
                    ),
                    ft.Container(
                        content=tasks_column,
                        alignment=ft.alignment.center,  # Center the tasks column
                        margin=10,
                    ),
                    ft.Row(
                        controls=[
                            ft.FloatingActionButton(
                                icon=ft.icons.ADD,
                                on_click=lambda _: show_add_task(None),
                                width=50,
                                height=50,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.END,  # Align the button to the end
                    ),
                    add_task_dialog,
                ],
                alignment=ft.MainAxisAlignment.CENTER,  # Center the column contents
            )
        ]
    )

# Start the scheduling loop
if __name__ == "__main__":
    tasks = load_tasks()
    for task in tasks:
        schedule_task(task)
    run_schedule()

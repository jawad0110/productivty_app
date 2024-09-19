import flet as ft
from datetime import datetime

def create_time_picker(page, time_field):
    selected_time = None  # Variable to store the selected time

    def handle_change(e):
        nonlocal selected_time
        selected_time = time_picker.value
        time_field.text = selected_time.strftime("%I:%M %p")  # Update button text
        page.update()

    def handle_dismissal(e):
        page.add(ft.Text(f"TimePicker dismissed: {time_picker.value}"))

    def handle_entry_mode_change(e):
        page.add(ft.Text(f"TimePicker Entry mode changed to {e.entry_mode}"))

    time_picker = ft.TimePicker(
        confirm_text="Confirm",
        error_invalid_text="Time out of range",
        help_text="Pick your time slot",
        on_change=handle_change,
        on_dismiss=handle_dismissal,
        on_entry_mode_change=handle_entry_mode_change,
    )
    return time_picker

def create_date_picker(page, date_field):
    selected_date = None  # Variable to store the selected date

    def handle_change(e):
        nonlocal selected_date
        selected_date = e.control.value
        date_field.text = selected_date.strftime("%Y-%m-%d")  # Update button text
        page.update()

    def handle_dismissal(e):
        page.add(ft.Text(f"DatePicker dismissed"))

    date_picker = ft.DatePicker(
        first_date=datetime(year=2023, month=10, day=1),
        last_date=datetime(year=2024, month=10, day=1),
        on_change=handle_change,
        on_dismiss=handle_dismissal,
    )
    return date_picker

def add_task_win(page, add_task_callback):
    page.fonts = {
        "Nohemi Black": "fonts/Nohemi-Black.ttf",
        "Nohemi Bold": "fonts/Nohemi-Bold.ttf",
        "Nohemi Regular": "fonts/Nohemi-Regular.ttf",
        "Nohemi Light": "fonts/Nohemi-Light.ttf"
    }

    # Create time_picker and date_picker instances and pass the fields to update their text
    time_field = ft.ElevatedButton(
        "Pick time",
        icon=ft.icons.TIMER,
        on_click=lambda _: page.open(time_picker),
    )
    time_picker = create_time_picker(page, time_field)

    date_field = ft.ElevatedButton(
        "Pick date",
        icon=ft.icons.CALENDAR_MONTH,
        on_click=lambda _: page.open(date_picker),
    )
    date_picker = create_date_picker(page, date_field)

    def show_add_task(e):
        add_task_dialog.visible = True
        page.update()

    def hide_add_task(e):
        add_task_dialog.visible = False
        page.clean()
        page.update()

    def add_task_action(e):
        task_title = title_field.value
        task_time = time_field.text  # Get time from button text
        task_date = date_field.text  # Get date from button text

        if task_title and task_time and task_date:
            add_task_callback(task_title, task_time, task_date)
            hide_add_task(e)
        else:
            print("All fields are required")

    text_style = ft.TextStyle(
        font_family="Nohemi Bold",
        size=20
    )

    # Create input fields
    title_field = ft.TextField(label="Title", bgcolor="#E8EDF2", color="#8B8E91")

    # Define the "add task" dialog container
    add_task_dialog = ft.Container(
        visible=False,
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Text("Add Task", size=24, weight="bold", color="Black", style=text_style),
                        ft.IconButton(
                            icon=ft.icons.CLOSE,
                            on_click=hide_add_task,
                            icon_color="Black",
                            icon_size=20
                        )
                    ],
                    expand=False,
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.END
                ),
                title_field,
                ft.Container(height=30),
                ft.Column(
                    controls=[
                        ft.Text("Date", size=16, color="Black"),
                        date_field,
                    ]
                ),
                ft.Column(
                    controls=[
                        ft.Text("Time", size=16, color="Black"),
                        time_field
                    ]
                ),
                ft.Container(height=30),
                # Add Task button
                ft.ElevatedButton(text="Add Task", on_click=add_task_action),
            ],
        ),
        padding=ft.padding.all(15),
        border_radius=ft.border_radius.all(10),
        bgcolor="#D9D9D9",
        width=350,
        height=450
    )

    return add_task_dialog, show_add_task

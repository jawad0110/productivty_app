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


def add_reminder_win(page, add_reminder_callback):
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

    def show_add_reminder(e):
        add_reminder_dialog.visible = True
        page.update()

    def hide_add_reminder(e):
        add_reminder_dialog.visible = False
        page.clean()
        page.update()

    def add_reminder_action(e):
        reminder_title = title_field.value
        reminder_time = time_field.text  # Get time from button text

        if reminder_title and reminder_time:
            add_reminder_callback(reminder_title, reminder_time)
            hide_add_reminder(e)
        else:
            print("All fields are required")

    text_style = ft.TextStyle(
        font_family="Nohemi Bold",
        size=20
    )

    # Create input fields
    title_field = ft.TextField(label="Title", bgcolor="#E8EDF2", color="#8B8E91")

    # Define the "add reminder" dialog container
    add_reminder_dialog = ft.Container(
        visible=False,
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Text("Add reminder", size=24, weight="bold", color="Black", style=text_style),
                        ft.IconButton(
                            icon=ft.icons.CLOSE,
                            on_click=hide_add_reminder,
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
                        ft.Text("Time", size=16, color="Black"),
                        time_field
                    ]
                ),
                ft.Container(height=30),
                # Add reminder button
                ft.ElevatedButton(text="Add reminder", on_click=add_reminder_action),
            ],
        ),
        padding=ft.padding.all(15),
        border_radius=ft.border_radius.all(10),
        bgcolor="#D9D9D9",
        width=350,
        height=450
    )

    return add_reminder_dialog, show_add_reminder

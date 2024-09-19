import flet as ft
import json
import os
import schedule
import time
from datetime import datetime
from plyer import notification
from .tasks.add_reminder import add_reminder_win

def save_reminders(reminders):
    with open('json/reminders.json', 'w') as file:
        json.dump(reminders, file)


def load_reminders():
    if os.path.exists('json/reminders.json'):
        with open('json/reminders.json', 'r') as file:
            return json.load(file)
    return []

def delete_reminder(reminder, reminders):
    reminders.remove(reminder)
    save_reminders(reminders)

def reminders_btn(page, reminder, reminders, reminders_column):
    btn_txt_style = ft.TextStyle(
        font_family="Nohemi Regular",
        size=15
    )

    # The buttons Style
    canceled_btn_style = ft.ButtonStyle(
        text_style=btn_txt_style,
        bgcolor="#F44336",
        shape=ft.RoundedRectangleBorder(radius=16)
    )
    done_btn_style = ft.ButtonStyle(
        text_style=btn_txt_style,
        bgcolor="#4CAF50",
        shape=ft.RoundedRectangleBorder(radius=16)
    )

    def delete_reminder_handler(e):
        delete_reminder(reminder, reminders)
        reminders_column.controls.remove(reminder_container)
        save_reminders(reminders)
        page.update()

    title = reminder.get("title", "No Title")
    time = reminder.get("time", "No Time")

    reminder_container = ft.Container(
        margin=10,
        padding=10,
        bgcolor='#959595',
        width=325,
        height=130,
        border_radius=10,
        alignment=ft.alignment.center_left,
        content=ft.Row(
            controls=[
                ft.Column(
                    controls=[
                        ft.Text(
                            value=title,
                            size=25,
                            color="Black",
                            font_family="Nohemi Bold"
                        ),
                        ft.Row(
                            controls=[
                                ft.Text(
                                    value=time,
                                    size=15,
                                    color="#3B3B3B",
                                    font_family="Nohemi Light"
                                )
                            ]
                        ),
                        ft.Row(
                            controls=[
                                ft.ElevatedButton(
                                    "Done",
                                    on_click=delete_reminder_handler,
                                    width=115, 
                                    height=30,
                                    color="Black",
                                    style=done_btn_style
                                ),
                                ft.ElevatedButton(
                                    "Canceled",
                                    on_click=delete_reminder_handler,
                                    width=115, 
                                    height=30,
                                    color="Black",
                                    style=canceled_btn_style
                                )
                            ],
                        )
                    ],
                    expand=True
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.END
        )
    )
    return reminder_container

def QuickRemindersPage(page: ft.Page):
    def on_column_scroll(e: ft.OnScrollEvent):
        pass

    page.fonts = {
        "Nohemi Black": "fonts/Nohemi-Black.ttf",
        "Nohemi Bold": "fonts/Nohemi-Bold.ttf",
        "Nohemi Regular": "fonts/Nohemi-Regular.ttf",
        "Nohemi Light": "fonts/Nohemi-Light.ttf"
    }

    reminders_column = ft.Column()

    reminders = load_reminders()
    
    def add_new_reminder(reminder_title, reminder_time):
        if reminder_title:
            reminder = {
                "title": reminder_title,
                "time": reminder_time,
            }
            reminders.append(reminder)
            reminder_btn = reminders_btn(page, reminder, reminders, reminders_column)
            reminders_column.controls.append(reminder_btn)
            save_reminders(reminders)
            page.update()

    add_reminder_dialog, show_add_reminder = add_reminder_win(page, add_new_reminder)

    for reminder in reminders:
        reminder_btn = reminders_btn(page, reminder, reminders, reminders_column)
        reminders_column.controls.append(reminder_btn)
        # Schedule the reminder

    return ft.View(
        route="/quick_reminders",
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
                                on_click=lambda _: page.go("/")
                            ),
                            ft.Text(
                                " Quick Reminders",
                                size=27,
                                font_family="Nohemi Black",
                                color="White"
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,  # Center the header horizontally
                        spacing=10  # Adjust spacing as needed
                    ),
                    ft.Container(
                        content=reminders_column,
                        alignment=ft.alignment.center,  # Center the reminders column
                        margin=10
                    ),
                    ft.Row(
                        controls=[
                            ft.FloatingActionButton(
                                icon=ft.icons.ADD,
                                on_click=lambda _: show_add_reminder(None),
                                width=50,
                                height=50
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.END,  # Align the button to the end
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,  # Center all content vertically
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Center all content horizontally
                spacing=20  # Add spacing between elements
            ),
            add_reminder_dialog
        ]
    )

# Start the scheduling loop
if __name__ == "__main__":
    reminders = load_reminders()
    for reminder in reminders:
        schedule_reminder(reminder)
    run_schedule()

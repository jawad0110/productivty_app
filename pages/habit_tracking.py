import flet as ft
import json
import os
from datetime import datetime
from .tasks.add_habit import add_habit_win

def save_habits(habits):
    with open('json/habits.json', 'w') as file:
        json.dump(habits, file)

def load_habits():
    if os.path.exists('json/habits.json'):
        with open('json/habits.json', 'r') as file:
            return json.load(file)
    return []

def save_done_habits(done_habits):
    with open('json/done_habits.json', 'w') as file:
        json.dump(done_habits, file)

def load_done_habits():
    if os.path.exists('json/done_habits.json'):
        with open('json/done_habits.json', 'r') as file:
            return json.load(file)
    return []

def delete_habit(habit, habits):
    habits.remove(habit)
    save_habits(habits)

def delete_done_habit(habit, done_habits):
    done_habits.remove(habit)
    save_done_habits(done_habits)

def habits_btn(page, habit, habits, habits_column):
    def delete_habit_handler(e):
        delete_habit(habit, habits)
        habits_column.controls.remove(habit_container)
        save_habits(habits)
        page.update()

    def on_checkbox_changed(e):
        if e.control.value:  # if checked
            done_habits = load_done_habits()
            done_habits.append(habit)
            save_done_habits(done_habits)
            delete_habit(habit, habits)
            habits_column.controls.remove(habit_container)
            page.update()

    title = habit.get("title", "No Title")

    habit_container = ft.Container(
        margin=10,
        padding=10,
        bgcolor='#959595',
        width=325,
        height=65,
        border_radius=10,
        alignment=ft.alignment.center_left,
        content=ft.Row(
            controls=[
                ft.Column(
                    controls=[
                        ft.Checkbox(
                            label=title,
                            value=False,
                            on_change=on_checkbox_changed
                        )
                    ],
                    expand=True
                ),
                ft.IconButton(
                    icon=ft.icons.DELETE,
                    icon_color="#F44336",
                    icon_size=30,
                    on_click=delete_habit_handler,
                    
                )
            ],
            alignment=ft.MainAxisAlignment.END,  # Align all controls to the end (right)
            vertical_alignment=ft.CrossAxisAlignment.CENTER  # Center vertically
        )
    )
    return habit_container

def done_habits_btn(page, habit, done_habits, habits, habits_column):
    def delete_done_habit_handler(e):
        delete_done_habit(habit, done_habits)
        habits_column.controls.remove(habit_container)
        save_done_habits(done_habits)
        page.update()

    def on_checkbox_changed(e):
        if not e.control.value:  # if unchecked
            habits.append(habit)
            save_habits(habits)
            delete_done_habit(habit, done_habits)
            habits_column.controls.remove(habit_container)
            page.update()

    title = habit.get("title", "No Title")

    habit_container = ft.Container(
        margin=10,
        padding=10,
        bgcolor='#959595',
        width=325,
        height=50,
        border_radius=10,
        alignment=ft.alignment.center_left,
        content=ft.Row(
            controls=[
                ft.Column(
                    controls=[
                        ft.Checkbox(
                            label=title,
                            value=True,
                            on_change=on_checkbox_changed
                        )
                    ],
                    expand=True
                )
            ],
            alignment=ft.MainAxisAlignment.END,  # Align all controls to the end (right)
            vertical_alignment=ft.CrossAxisAlignment.CENTER  # Center vertically
        )
    )
    return habit_container

def HabitTrackingPage(page: ft.Page):
    def on_column_scroll(e: ft.OnScrollEvent):
        pass

    page.fonts = {
        "Nohemi Black": "fonts/Nohemi-Black.ttf",
        "Nohemi Bold": "fonts/Nohemi-Bold.ttf",
        "Nohemi Regular": "fonts/Nohemi-Regular.ttf",
        "Nohemi Light": "fonts/Nohemi-Light.ttf"
    }

    habits_column = ft.Column()
    habits = load_habits()
    done_habits = load_done_habits()
    
    def add_new_habit(habit_title):
        if habit_title:
            habit = {
                "title": habit_title,
            }
            habits.append(habit)
            habit_btn = habits_btn(page, habit, habits, habits_column)
            habits_column.controls.append(habit_btn)
            save_habits(habits)
            page.update()

    add_habit_dialog, show_add_habit = add_habit_win(page, add_new_habit)

    def show_not_done_habits(e):
        habits_column.controls.clear()
        for habit in habits:
            habit_btn = habits_btn(page, habit, habits, habits_column)
            habits_column.controls.append(habit_btn)
        page.update()

    def show_done_habits(e):
        habits_column.controls.clear()
        for habit in done_habits:
            habit_btn = done_habits_btn(page, habit, done_habits, habits, habits_column)
            habits_column.controls.append(habit_btn)
        page.update()

    for habit in habits:
        habit_btn = habits_btn(page, habit, habits, habits_column)
        habits_column.controls.append(habit_btn)

    return ft.View(
        route="/habits",
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
                                " Habits Tracker",
                                size=27,
                                font_family="Nohemi Black",
                                color="White"
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,  # Center the header horizontally
                        spacing=10  # Adjust spacing as needed
                    ),
                    ft.Row(
                        controls=[
                            ft.ElevatedButton(
                                text="Not Done Habits",
                                on_click=show_not_done_habits
                            ),
                            ft.ElevatedButton(
                                text="Done Habits",
                                on_click=show_done_habits
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,  # Center the buttons
                        spacing=10  # Adjust spacing as needed
                    ),
                    ft.Container(
                        content=habits_column,
                        alignment=ft.alignment.center,  # Center the habits column
                        margin=10
                    ),
                    ft.Row(
                        controls=[
                            ft.FloatingActionButton(
                                icon=ft.icons.ADD,
                                on_click=lambda _: show_add_habit(None),
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
            add_habit_dialog
        ]
    )

# Start the scheduling loop
if __name__ == "__main__":
    habits = load_habits()
    for habit in habits:
        schedule_habit(habit)
    run_schedule()

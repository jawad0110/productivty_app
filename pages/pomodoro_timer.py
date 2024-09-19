import flet as ft
import time
from threading import Thread, Event

class CountdownTimer:
    def __init__(self, page, hour_input, minute_input, second_input, colon1, colon2, countdown_text, stop_button, start_button, continue_button):
        self.page = page
        self.hour_input = hour_input
        self.minute_input = minute_input
        self.second_input = second_input
        self.colon1 = colon1
        self.colon2 = colon2
        self.countdown_text = countdown_text
        self.stop_button = stop_button
        self.start_button = start_button
        self.continue_button = continue_button
        self.time_left = 0
        self.running = False
        self.stop_event = Event()

    def set_time(self):
        h = int(self.hour_input.value or 0)
        m = int(self.minute_input.value or 0)
        s = int(self.second_input.value or 0)
        self.time_left = h * 3600 + m * 60 + s

    def start(self):
        self.running = True
        self.stop_event.clear()
        self.stop_button.visible = True
        self.start_button.visible = False
        self.continue_button.visible = False
        self.hour_input.visible = False
        self.minute_input.visible = False
        self.second_input.visible = False
        self.colon1.visible = False
        self.colon2.visible = False
        self.countdown_text.visible = True
        self.page.update()
        thread = Thread(target=self._countdown)
        thread.start()

    def stop(self):
        self.running = False
        self.stop_event.set()
        self.stop_button.visible = False
        self.continue_button.visible = True
        self.page.update()

    def reset(self):
        self.stop()
        self.time_left = 0
        self.update_text("00:00:00")
        self.hour_input.value = ""
        self.minute_input.value = ""
        self.second_input.value = ""
        self.hour_input.visible = True
        self.minute_input.visible = True
        self.second_input.visible = True
        self.colon1.visible = True
        self.colon2.visible = True
        self.countdown_text.visible = False
        self.start_button.visible = True
        self.continue_button.visible = False  # Ensure continue button is hidden
        self.page.update()

    def _countdown(self):
        while self.running and self.time_left > 0:
            if self.stop_event.is_set():
                break
            time.sleep(1)
            self.time_left -= 1
            self.update_text(self.seconds_to_hms(self.time_left))

    def update_text(self, time_str):
        self.countdown_text.value = time_str
        self.page.update()

    def seconds_to_hms(self, seconds):
        h = seconds // 3600
        m = (seconds % 3600) // 60
        s = seconds % 60
        return f"{h:02}:{m:02}:{s:02}"

def PomodoroTimerPage(page):
    # Register custom fonts
    page.fonts = {
        "Nohemi Black": "fonts/Nohemi-Black.ttf",
        "Nohemi Bold": "fonts/Nohemi-Bold.ttf",
        "Nohemi Regular": "fonts/Nohemi-Regular.ttf",
        "Nohemi Light": "fonts/Nohemi-Light.ttf"
    }

    # Create the UI elements for hour, minute, second
    hour_input = ft.TextField(value="", width=50, border_color="#a0c9fc", text_align=ft.TextAlign.CENTER, keyboard_type=ft.KeyboardType.NUMBER)
    minute_input = ft.TextField(value="", width=50, border_color="#a0c9fc", text_align=ft.TextAlign.CENTER, keyboard_type=ft.KeyboardType.NUMBER)
    second_input = ft.TextField(value="", width=50, border_color="#a0c9fc", text_align=ft.TextAlign.CENTER, keyboard_type=ft.KeyboardType.NUMBER)

    colon1 = ft.Text(value=":", size=40, visible=True)
    colon2 = ft.Text(value=":", size=40, visible=True)
    countdown_text = ft.Text(value="00:00:00", size=40, color="#a0c9fc", font_family="Nohemi Bold", text_align=ft.TextAlign.CENTER, visible=False)

    # Instantiate CountdownTimer with the page and UI elements
    timer = CountdownTimer(page, hour_input, minute_input, second_input, colon1, colon2, countdown_text, None, None, None)

    def start_countdown(e):
        timer.set_time()
        if timer.time_left > 0:
            timer.start()
        else:
            countdown_text.value = "Invalid time"
            page.update()

    def stop_countdown(e):
        timer.stop()

    def continue_countdown(e):
        timer.start()

    def reset_countdown(e):
        timer.reset()

    start_button = ft.ElevatedButton(
        text="Start",
        color="Black",
        on_click=start_countdown,
        style=ft.ButtonStyle(
            bgcolor="Green",
            text_style=ft.TextStyle(
                font_family="Nohemi Bold"
            )
        )
    )
    stop_button = ft.ElevatedButton(
        text="Stop",
        color="Black",
        on_click=stop_countdown,
        visible=False,
        style=ft.ButtonStyle(
            bgcolor="#FFA808",
            text_style=ft.TextStyle(
                font_family="Nohemi Bold"
            )
        )
    )
    continue_button = ft.ElevatedButton(
        text="Continue",
        color="Black",
        on_click=continue_countdown,
        visible=False,
        style=ft.ButtonStyle(
            bgcolor="Green",
            text_style=ft.TextStyle(
                font_family="Nohemi Bold"
            )
        )
    )

    reset_button = ft.ElevatedButton(
        text="Reset",
        color="Black",
        on_click=reset_countdown,
        style=ft.ButtonStyle(
            bgcolor="Red",
            text_style=ft.TextStyle(
                font_family="Nohemi Bold",
            )
        )
    )

    # Update timer instance with buttons after their creation
    timer.start_button = start_button
    timer.stop_button = stop_button
    timer.continue_button = continue_button

    # Arrange input fields and buttons in columns
    countdown_row = ft.Row(
        controls=[hour_input, colon1, minute_input, colon2, second_input],
        alignment=ft.MainAxisAlignment.CENTER
    )
    button_row = ft.Row(
        controls=[start_button, stop_button, reset_button, continue_button],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=10
    )
    content_column = ft.Column(
        controls=[
            countdown_row,
            countdown_text,
            ft.Container(height=30),
            button_row
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20
    )

    return ft.View(
        route="/time_tracking",
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
                        "Pomodoro Timer",
                        size=25,
                        font_family="Nohemi Black",
                        color="White",
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10
            ),
            ft.Container(height=50),  # Space between header and content
            content_column
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER  # Center the entire view
    )

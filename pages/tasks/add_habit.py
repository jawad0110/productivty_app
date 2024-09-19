import flet as ft

def add_habit_win(page, add_habit_callback):
    page.fonts = {
        "Nohemi Black": "fonts/Nohemi-Black.ttf",
        "Nohemi Bold": "fonts/Nohemi-Bold.ttf",
        "Nohemi Regular": "fonts/Nohemi-Regular.ttf",
        "Nohemi Light": "fonts/Nohemi-Light.ttf"
    }

    def show_add_habit(e):
        add_habit_dialog.visible = True
        page.update()

    def hide_add_habit(e):
        add_habit_dialog.visible = False
        page.clean()
        page.update()

    def add_habit_action(e):
        habit_title = title_field.value
    
        if habit_title:
            add_habit_callback(habit_title)
            hide_add_habit(e)
        else:
            print("All fields are required")

    text_style = ft.TextStyle(
        font_family="Nohemi Bold",
        size=20
    )

    # Create input fields
    title_field = ft.TextField(label="Title", bgcolor="#E8EDF2", color="#8B8E91")

    # Define the "add habit" dialog container
    add_habit_dialog = ft.Container(
        visible=False,
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Text("Add habit", size=24, weight="bold", color="Black", style=text_style),
                        ft.IconButton(
                            icon=ft.icons.CLOSE,
                            on_click=hide_add_habit,
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
                # Add habit button
                ft.ElevatedButton(text="Add habit", on_click=add_habit_action),
            ],
        ),
        padding=ft.padding.all(15),
        border_radius=ft.border_radius.all(10),
        bgcolor="#D9D9D9",
        width=350,
        height=250
    )

    return add_habit_dialog, show_add_habit

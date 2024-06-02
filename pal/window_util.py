import pytermgui as ptg


def weather_window(data, format: str):
    with ptg.WindowManager() as manager:
        window = (
            ptg.Window(
                "",
                ptg.Splitter(
                    ptg.Label(
                        f"[surface+1]{data['current']['condition']['text']}",
                        parent_align=0,
                    ),
                    ptg.Label(
                        f"[surface+3]{data['current'][f'temp_{format}']}°{format.capitalize()}",
                        parent_align=2,
                    ),
                ),
                ptg.Container(
                    ptg.Label(
                        f"[surface+1]Feels like: [surface+3]{data['current'][f'feelslike_{format}']}°{format.capitalize()}\n[surface+1]Humidity: [surface+3]{data['current']['humidity']}%",
                        parent_align=0,
                    ),
                    box="ROUNDED",
                ),
            )
            .set_title(f"{data['location']['name']}")
            .center()
        )
        manager.add(window)

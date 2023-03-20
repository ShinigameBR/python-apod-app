import customtkinter
import os
from PIL import Image
from apod import Apod


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Shin's APOD App")
        self.geometry("1100x630")

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # load images with light and dark mode image
        static_image_path = os.path.join(os.path.dirname(os.path.realpath(
            __file__)), "assets/imgs")
        apod_images_path = os.path.join(os.path.dirname(os.path.realpath(
            __file__)), "cache/imgs")
        self.iconbitmap(os.path.join(static_image_path, "logo.ico"))

        self.home_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(static_image_path, "home_dark.png")),
                                                 dark_image=Image.open(os.path.join(static_image_path, "home_light.png")), size=(20, 20))
        self.search_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(static_image_path, "search_dark.png")),
                                                   dark_image=Image.open(os.path.join(static_image_path, "search_light.png")), size=(20, 20))
        self.about_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(static_image_path, "about_dark.png")),
                                                  dark_image=Image.open(os.path.join(static_image_path, "about_light.png")), size=(20, 20))

        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(
            self.navigation_frame, text="Shin's APOD", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        # change frames buttons
        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Home",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.home_image, anchor="w", command=self.home_frame_button_event, font=customtkinter.CTkFont(size=15, weight="bold"))
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.search_frame_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Search",
                                                           fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                           image=self.search_image, anchor="w", command=self.search_frame_button_event, font=customtkinter.CTkFont(size=15, weight="bold"))
        self.search_frame_button.grid(row=2, column=0, sticky="ew")

        self.about_frame_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="About",
                                                          fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                          image=self.about_image, anchor="w", command=self.about_frame_button_event, font=customtkinter.CTkFont(size=15, weight="bold"))
        self.about_frame_button.grid(row=3, column=0, sticky="ew")

        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame, values=["System", "Dark", "Light"],
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(
            row=6, column=0, padx=20, pady=20, sticky="s")

        # create apod object
        self.apod = Apod()
        self.delete_cache = self.apod.erease_cached_images(apod_images_path)

        # create home frame
        self.home_frame = customtkinter.CTkScrollableFrame(
            self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)

        if not self.apod.get_status():
            self.home_frame_error_label = customtkinter.CTkLabel(
                self.home_frame, text="Erro ao buscar os dados!", font=customtkinter.CTkFont(size=15, weight="bold"))
            self.home_frame_error_label.grid(
                row=0, column=0, padx=20, pady=10)

        else:
            # getting the data from API
            try:
                self.apod_today_image = Image.open(self.apod.get_image())
            except:
                self.apod_today_image = Image.open(os.path.join(static_image_path, "noimage.png"))
            self.apod_today_title = self.apod.get_title()
            self.apod_today_date = self.apod.get_date()
            self.apod_today_description = self.apod.get_description()

            # original image size
            width, height = self.apod_today_image.size

            # target size (width, height)
            target_size = (640, 334)

            # aspect ratio
            aspect_ratio = width / height

            # compute new size
            if width > height:
                new_width = target_size[0]
                new_height = int(target_size[0] / aspect_ratio)
            else:
                new_height = target_size[1]
                new_width = int(target_size[1] * aspect_ratio)

            # showing data
            self.today_image = customtkinter.CTkImage(
                self.apod_today_image, size=(new_width, new_height))
            self.home_frame_image_label = customtkinter.CTkLabel(
                self.home_frame, text="", width=new_width, height=new_height, image=self.today_image)
            self.home_frame_image_label.grid(
                row=0, column=0, padx=20, pady=10)

            self.home_frame_title_label = customtkinter.CTkLabel(
                self.home_frame, text=self.apod_today_title, font=customtkinter.CTkFont(size=15, weight="bold"))
            self.home_frame_title_label.grid(
                row=1, column=0, padx=20, pady=10)

            self.home_frame_date_label = customtkinter.CTkLabel(
                self.home_frame, text=self.apod_today_date, font=customtkinter.CTkFont(size=15))
            self.home_frame_date_label.grid(
                row=2, column=0, padx=20, pady=10)

            self.home_frame_description_textbox = customtkinter.CTkTextbox(
                self.home_frame, width=600, font=customtkinter.CTkFont(size=14))
            self.home_frame_description_textbox.insert(
                "0.0", self.apod_today_description)
            self.home_frame_description_textbox.configure(
                state="disabled", wrap="word")
            self.home_frame_description_textbox.grid(
                row=3, column=0, padx=20, pady=10)

        # create second frame
        self.search_frame = customtkinter.CTkScrollableFrame(
            self, corner_radius=0, fg_color="transparent")
        self.search_frame.grid_columnconfigure(0, weight=1)

        self.search_frame_entry = customtkinter.CTkEntry(
            self.search_frame, placeholder_text="Ex.: 2022-12-31")
        self.search_frame_entry.grid(row=0, column=0, padx=20, pady=10)

        self.search_frame_button = customtkinter.CTkButton(
            self.search_frame, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text="Search", command=self.search_by_date_apod)
        self.search_frame_button.grid(row=1, column=0, padx=20, pady=0)

        # create third frame
        self.about_frame = customtkinter.CTkFrame(
            self, corner_radius=0, fg_color="transparent")
        self.about_frame.rowconfigure(0, weight=1)
        self.about_frame.columnconfigure(0, weight=1)

        self.about_frame_label = customtkinter.CTkLabel(
            self.about_frame, text="I'm just a student getting into programming, visit my Github and my personal website to see my journey.", font=customtkinter.CTkFont(size=32, weight="bold"), wraplength=400)
        self.about_frame_label.grid(
            row=0, column=0, sticky="nsew", padx=10, pady=10)

        # select default frame
        self.select_frame_by_name("home")

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(
            fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.search_frame_button.configure(
            fg_color=("gray75", "gray25") if name == "search_frame" else "transparent")
        self.about_frame_button.configure(
            fg_color=("gray75", "gray25") if name == "about_frame" else "transparent")

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "search_frame":
            self.search_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.search_frame.grid_forget()
        if name == "about_frame":
            self.about_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.about_frame.grid_forget()

    def home_frame_button_event(self):
        self.select_frame_by_name("home")

    def search_frame_button_event(self):
        self.select_frame_by_name("search_frame")

    def search_by_date_apod(self):
        self.apod.get_search(self.search_frame_entry.get())

        old_search_elements = self.search_frame.grid_slaves()
        for elem in old_search_elements:
            elem.destroy()

        self.search_frame_entry = customtkinter.CTkEntry(
            self.search_frame, placeholder_text="Ex.: 2022-12-31")
        self.search_frame_entry.grid(row=0, column=0, padx=20, pady=10)

        self.search_frame_button = customtkinter.CTkButton(
            self.search_frame, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text="Search", command=self.search_by_date_apod)
        self.search_frame_button.grid(row=1, column=0, padx=20, pady=0)

        if not self.apod.get_status():
            self.search_frame_error_label = customtkinter.CTkLabel(
                self.search_frame, text="Erro ao buscar os dados!", font=customtkinter.CTkFont(size=15, weight="bold"))
            self.search_frame_error_label.grid(
                row=2, column=0, padx=20, pady=10)

        else:
            # getting the data from API
            try:
                self.apod_search_image = Image.open(self.apod.get_image())
            except:
                self.apod_today_image = Image.open(os.path.join(self.static_image_path, "noimage.png"))
            self.apod_search_title = self.apod.get_title()
            self.apod_search_date = self.apod.get_date()
            self.apod_search_description = self.apod.get_description()

            # original image size
            width, height = self.apod_search_image.size

            # target size (width, height)
            target_size = (640, 334)

            # aspect ratio
            aspect_ratio = width / height

            # compute new size
            if width > height:
                new_width = target_size[0]
                new_height = int(target_size[0] / aspect_ratio)
            else:
                new_height = target_size[1]
                new_width = int(target_size[1] * aspect_ratio)

            # showing data
            self.search_image = customtkinter.CTkImage(
                self.apod_search_image, size=(new_width, new_height))
            self.search_frame_image_label = customtkinter.CTkLabel(
                self.search_frame, text="", width=new_width, height=new_height, image=self.search_image)
            self.search_frame_image_label.grid(
                row=2, column=0, padx=20, pady=10)

            self.search_frame_title_label = customtkinter.CTkLabel(
                self.search_frame, text=self.apod_search_title, font=customtkinter.CTkFont(size=15, weight="bold"))
            self.search_frame_title_label.grid(
                row=3, column=0, padx=20, pady=10)

            self.search_frame_date_label = customtkinter.CTkLabel(
                self.search_frame, text=self.apod_search_date, font=customtkinter.CTkFont(size=15))
            self.search_frame_date_label.grid(
                row=4, column=0, padx=20, pady=10)

            self.search_frame_description_textbox = customtkinter.CTkTextbox(
                self.search_frame, width=600, font=customtkinter.CTkFont(size=14))
            self.search_frame_description_textbox.insert(
                "0.0", self.apod_search_description)
            self.search_frame_description_textbox.configure(
                state="disabled", wrap="word")
            self.search_frame_description_textbox.grid(
                row=5, column=0, padx=20, pady=10)

    def about_frame_button_event(self):
        self.select_frame_by_name("about_frame")

    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)


if __name__ == "__main__":
    app = App()
    app.mainloop()

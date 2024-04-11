#!/usr/bin/env python3

import gi
import os
import conflicts
import subprocess
import threading
import shutil
import socket
from time import sleep
from queue import Queue
import ui.GUI as GUI
from ui.MessageDialog import MessageDialogBootloader
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf, GLib, Gdk 

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__)))
REMOTE_SERVER = "www.google.com"

css = """
box#stack_box{
    padding: 10px 10px 10px 10px;
}
button#button_grub_boot_enabled{
     font-weight: bold;
     background-color: @theme_base_color_button;
}
button#button_systemd_boot_enabled{
     font-weight: bold;
     background-color: @theme_base_color_button;
}
button#button_easy_install_enabled{
     font-weight: bold;
     background-color: @theme_base_color_button;
}
button#button_adv_install_enabled{
     font-weight: bold;
     background-color: @theme_base_color_button;
}
label#label_style {
    background-color: @theme_base_color;
    border-top: 1px solid @borders;
    border-bottom: 1px solid @borders;
    border-left: 1px solid @borders;
    border-right: 1px solid @borders;
    padding: 10px 10px 10px 10px;
    border-radius: 0px;
    font-size: 16px;
    font-weight: bold;
    color: pink;
}
label#label_style_eshan {
    background-color: @theme_base_color;
    border-top: 1px solid @borders;
    border-bottom: 1px solid @borders;
    border-left: 1px solid @borders;
    border-right: 1px solid @borders;
    padding: 10px 10px 10px 10px;
    border-radius: 0px;
    font-size: 16px;
    font-weight: bold;
    color: #F8C8DC;
}
"""

class Main(Gtk.Window):
    def __init__(self):
        super(Main, self).__init__(title="Snigdha OS Welcome")
        self.set_border_width(10)
        self.set_default_size(860, 450)
        self.set_icon_from_file(os.path.join(base_dir, "images/snigdhaos-welcome-small.png"))
        self.set_position(Gtk.WindowPosition.CENTER)
        self.results = ""
        if not os.path.exists(GUI.home + "/.config/snigdhaos-welcome/"):
            os.mkdir(GUI.home + "/.config/snigdhaos-welcome/")
            with open(GUI.Settings, "w") as f:
                f.write("autostart=True")
                f.close()
        self.style_provider = Gtk.CssProvider()
        self.style_provider.load_from_data(css, len(css))
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            self.style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )
        self.pkg_queue = Queue()
        self.pacman_lockfile = "/var/lib/pacman/db.lck"
        self.sudo_username = os.getlogin()
        self.calamares_polkit = "/usr/bin/calamares_polkit"
        self.session = None
        self.get_session()
        GUI.GUI(self, Gtk, GdkPixbuf)
        if GUI.username == GUI.user:
            threading.Thread(
                target=self.internet_notifier, args=(), daemon=True
            ).start()
    def get_session(self):
        try:
            self.session = os.environ.get("XDG_SESSION_TYPE")
        except Exception as e:
            print("Exception in get_session(): %s" % e)

    def on_settings_clicked(self, widget):
        self.toggle_popover()

    def toggle_popover(self):
        if self.popover.get_visible():
            self.popover.hide()
        else:
            self.popover.show_all()

    def file_check(self, path):
        if os.path.isfile(path):
            return True
        return False

    def on_mirror_clicked(self, widget):
        threading.Thread(target=self.mirror_update, daemon=True).start()

    def on_update_clicked(self, widget):
        print("Clicked")

    def convert_to_hex(self, rgba_color):
        red = int(rgba_color.red * 255)
        green = int(rgba_color.green * 255)
        blue = int(rgba_color.blue * 255)
        return "#{r:02x}{g:02x}{b:02x}".format(r=red, g=green, b=blue)

    def on_easy_install_clicked(self, widget):
        if not os.path.exists(self.pacman_lockfile):
            widget.set_name("button_easy_install_enabled")
            widget.get_child().set_markup(
                "<span size='large'>Offline Installation</span>"
            )
            selected_bg_color = widget.get_style_context().lookup_color(
                "theme_selected_bg_color"
            )
            if selected_bg_color[0] is True:
                theme_bg_hex_color = self.convert_to_hex(selected_bg_color[1])
                custom_css = css.replace("@theme_base_color_button", theme_bg_hex_color)
                self.style_provider.load_from_data(custom_css, len(custom_css))
            self.button_adv_install.set_name("button_adv_install")
            settings_beginner_file = "/etc/calamares/settings-beginner.conf"
            packages_no_sys_update_file = (
                "/etc/calamares/modules/packages-no-system-update.conf"
            )
            app_cmd = [
                "sudo",
                "cp",
                settings_beginner_file,
                "/etc/calamares/settings.conf",
            ]
            threading.Thread(target=self.run_app, args=(app_cmd,), daemon=True).start()
            app_cmd = [
                "sudo",
                "cp",
                packages_no_sys_update_file,
                "/etc/calamares/modules/packages.conf",
            ]
            threading.Thread(target=self.run_app, args=(app_cmd,), daemon=True).start()
            efi_file_check = self.file_check("/sys/firmware/efi/fw_platform_size")
            if efi_file_check is True:
                md = MessageDialogBootloader(
                    title="Choose Bootloader",
                    install_method="Offline Installation",
                    pacman_lockfile=self.pacman_lockfile,
                    run_app=self.run_app,
                    calamares_polkit=self.calamares_polkit,
                )
                md.show_all()
            else:
                subprocess.Popen([self.calamares_polkit, "-d"], shell=False)
        else:
            print(
                "[ERROR]: Pacman lockfile found %s, is another pacman process running ?"
                % self.pacman_lockfile
            )
            md = Gtk.MessageDialog(
                parent=self,
                flags=0,
                message_type=Gtk.MessageType.WARNING,
                buttons=Gtk.ButtonsType.OK,
                text="Pacman lockfile found %s, is another pacman process running ?"
                % self.pacman_lockfile,
                title="Warning",
            )
            md.run()
            md.destroy()

    def on_adv_install_clicked(self, widget):
        if not os.path.exists(self.pacman_lockfile):
            widget.set_name("button_adv_install_enabled")
            widget.get_child().set_markup(
                "<span size='large'>Online Installation</span>"
            )
            selected_bg_color = widget.get_style_context().lookup_color(
                "theme_selected_bg_color"
            )
            if selected_bg_color[0] is True:
                theme_bg_hex_color = self.convert_to_hex(selected_bg_color[1])
                custom_css = css.replace("@theme_base_color_button", theme_bg_hex_color)
                self.style_provider.load_from_data(custom_css, len(custom_css))
            self.button_easy_install.set_name("button_easy_install")
            settings_adv_file = "/etc/calamares/settings-advanced.conf"
            system_update_file = "/etc/calamares/modules/packages-system-update.conf"
            app_cmd = [
                "sudo",
                "cp",
                settings_adv_file,
                "/etc/calamares/settings.conf",
            ]
            threading.Thread(target=self.run_app, args=(app_cmd,), daemon=True).start()
            app_cmd = [
                "sudo",
                "cp",
                system_update_file,
                "/etc/calamares/modules/packages.conf",
            ]
            threading.Thread(target=self.run_app, args=(app_cmd,), daemon=True).start()
            efi_file_check = self.file_check("/sys/firmware/efi/fw_platform_size")
            if efi_file_check is True:
                md = MessageDialogBootloader(
                    title="Choose Bootloader",
                    install_method="Online Installation",
                    pacman_lockfile=self.pacman_lockfile,
                    run_app=self.run_app,
                    calamares_polkit=self.calamares_polkit,
                )
                md.show_all()
            else:
                subprocess.Popen([self.calamares_polkit, "-d"], shell=False)
        else:
            print(
                "[ERROR]: Pacman lockfile found %s, is another pacman process running ?"
                % self.pacman_lockfile
            )
            md = Gtk.MessageDialog(
                parent=self,
                flags=0,
                message_type=Gtk.MessageType.WARNING,
                buttons=Gtk.ButtonsType.OK,
                text="Pacman lockfile found %s, is another pacman process running ?"
                % self.pacman_lockfile,
                title="Warning",
            )
            md.run()
            md.destroy()
    def on_gp_clicked(self, widget):
        app_cmd = ["/usr/bin/gparted"]
        pacman_cmd = [
            "pkexec",
            "pacman",
            "-Sy",
            "gparted",
            "--noconfirm",
            "--needed",
        ]
        if not self.check_package_installed("gparted"):
            if not os.path.exists(self.pacman_lockfile):
                md = Gtk.MessageDialog(
                    parent=self,
                    flags=0,
                    message_type=Gtk.MessageType.WARNING,
                    buttons=Gtk.ButtonsType.NONE,
                    text="%s was not found" % "gparted",
                    title="Warning",
                )
                md.add_buttons("Yes", 1)
                md.add_buttons("No", 0)
                md.format_secondary_markup("Let Snigdha OS - Welcome install it ?")
                response = md.run()
                md.destroy()
                if response == 1:
                    threading.Thread(
                        target=self.check_package_queue, daemon=True
                    ).start()
                    threading.Thread(
                        target=self.install_package,
                        args=(
                            app_cmd,
                            pacman_cmd,
                            "gparted",
                        ),
                        daemon=True,
                    ).start()
            else:
                print(
                    "[ERROR]: Pacman lockfile found %s, is another pacman process running ?"
                    % self.pacman_lockfile
                )
                md = Gtk.MessageDialog(
                    parent=self,
                    flags=0,
                    message_type=Gtk.MessageType.WARNING,
                    buttons=Gtk.ButtonsType.OK,
                    text="Pacman lockfile found %s, is another pacman process running ?"
                    % self.pacman_lockfile,
                    title="Warning",
                )
                md.run()
                md.destroy()
        else:
            threading.Thread(target=self.run_app, args=(app_cmd,), daemon=True).start()

    def on_buttonarandr_clicked(self, widget):
        app_cmd = ["/usr/bin/arandr"]
        pacman_cmd = [
            "pkexec",
            "pacman",
            "-Sy",
            "arandr",
            "--noconfirm",
            "--needed",
        ]
        if not self.check_package_installed("arandr"):
            if not os.path.exists(self.pacman_lockfile):
                md = Gtk.MessageDialog(
                    parent=self,
                    flags=0,
                    message_type=Gtk.MessageType.WARNING,
                    buttons=Gtk.ButtonsType.NONE,
                    text="%s was not found\n" % "arandr",
                    title="Warning",
                )
                md.add_buttons("Yes", 1)
                md.add_buttons("No", 0)
                md.format_secondary_markup("Let Snigdha OS - Welcome install it ?")
                response = md.run()
                md.destroy()
                if response == 1:
                    threading.Thread(
                        target=self.check_package_queue, daemon=True
                    ).start()
                    threading.Thread(
                        target=self.install_package,
                        args=(
                            app_cmd,
                            pacman_cmd,
                            "arandr",
                        ),
                        daemon=True,
                    ).start()
            else:
                print(
                    "[ERROR]: Pacman lockfile found %s, is another pacman process running ?"
                    % self.pacman_lockfile
                )
                md = Gtk.MessageDialog(
                    parent=self,
                    flags=0,
                    message_type=Gtk.MessageType.WARNING,
                    buttons=Gtk.ButtonsType.OK,
                    text="Pacman lockfile found %s, is another pacman process running ?"
                    % self.pacman_lockfile,
                    title="Warning",
                )
                md.run()
                md.destroy()
        else:
            threading.Thread(target=self.run_app, args=(app_cmd,), daemon=True).start()
    def remove_dev_package(self, pacman_cmd, package):
        try:
            self.label_notify.set_name("label_style")
            GLib.idle_add(
                self.label_notify.show,
            )
            GLib.idle_add(
                self.label_notify.set_markup,
                "<span foreground='orange'><b>Removing dev package %s</b></span>"
                % package,
            )
            GLib.idle_add(
                self.label_notify.hide,
            )
            with subprocess.Popen(
                pacman_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                bufsize=1,
                universal_newlines=True,
            ) as process:
                while True:
                    if process.poll() is not None:
                        break

                    for line in process.stdout:
                        print(line.strip())

                if not self.check_package_installed(package):
                    print("[INFO]: Pacman %s uninstall completed" % package)
                    GLib.idle_add(
                        self.label_notify.show,
                    )
                    self.label_notify.set_name("label_style")
                    GLib.idle_add(
                        self.label_notify.set_markup,
                        "<span foreground='orange'><b>Dev package %s removed</b></span>"
                        % package,
                    )
                    GLib.idle_add(
                        self.label_notify.hide,
                    )
                else:
                    print("[ERROR]: Pacman %s uninstall failed" % package)
                    self.label_notify.set_name("label_style")
                    GLib.idle_add(
                        self.label_notify.show,
                    )
                    GLib.idle_add(
                        self.label_notify.set_markup,
                        "<span foreground='red'><b>Failed to remove dev package %s</b></span>"
                        % package,
                    )
        except Exception as e:
            print("[ERROR]: Exception in remove_dev_package(): %s" % e)
            self.label_notify.set_name("label_style")
            GLib.idle_add(
                self.label_notify.show,
            )
            GLib.idle_add(
                self.label_notify.set_markup,
                "<span foreground='red'><b>Failed to remove dev package %s</b></span>"
                % package,
            )
    def install_package(self, app_cmd, pacman_cmd, package):
        try:
            self.label_notify.set_name("label_style")
            GLib.idle_add(
                self.label_notify.set_markup,
                "<span foreground='cyan'><b>Installing %s</b></span>" % package,
            )
            with subprocess.Popen(
                pacman_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                bufsize=1,
                universal_newlines=True,
            ) as process:
                while True:
                    if process.poll() is not None:
                        break
                    for line in process.stdout:
                        print(line.strip())
                if self.check_package_installed(package):
                    self.pkg_queue.put((0, app_cmd, package))
                    print("[INFO]: Pacman package install completed")
                    self.label_notify.set_name("label_style")
                    GLib.idle_add(
                        self.label_notify.show,
                    )
                    GLib.idle_add(
                        self.label_notify.set_markup,
                        "<span foreground='purple'><b>Package %s installed</b></span>"
                        % package,
                    )
                    GLib.idle_add(
                        self.label_notify.hide,
                    )
                else:
                    self.pkg_queue.put((1, app_cmd, package))
                    print("[ERROR]: Pacman package install failed")
                    self.label_notify.set_name("label_style")
                    GLib.idle_add(
                        self.label_notify.show,
                    )
                    GLib.idle_add(
                        self.label_notify.set_markup,
                        "<span foreground='orange'><b>Package %s install failed</b></span>"
                        % package,
                    )
        except Exception as e:
            print("[ERROR]: Exception in install_package(): %s" % e)
            self.label_notify.set_name("label_style")
            GLib.idle_add(
                self.label_notify.show,
            )
            GLib.idle_add(
                self.label_notify.set_markup,
                "<span foreground='red'><b>Package install failed</b></span>",
            )
        finally:
            self.pkg_queue.put(None)

    def run_app(self, app_cmd):
        process = subprocess.run(
            app_cmd,
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
        )
        # for debugging print stdout to console
        if GUI.debug is True:
            print(process.stdout)

    def startup_toggle(self, widget):
        if widget.get_active() is True:
            if os.path.isfile(GUI.dot_desktop):
                shutil.copy(GUI.dot_desktop, GUI.autostart)
        else:
            if os.path.isfile(GUI.autostart):
                os.unlink(GUI.autostart)
        self.save_settings(widget.get_active())

    def save_settings(self, state):
        with open(GUI.Settings, "w") as f:
            f.write("autostart=" + str(state))
            f.close()

    def load_settings(self):
        line = "True"
        if os.path.isfile(GUI.Settings):
            with open(GUI.Settings, "r") as f:
                lines = f.readlines()
                for i in range(len(lines)):
                    if "autostart" in lines[i]:
                        line = lines[i].split("=")[1].strip().capitalize()
                f.close()
        return line

    def on_link_clicked(self, widget, link):
        t = threading.Thread(target=self.weblink, args=(link,))
        t.daemon = True
        t.start()

    def on_social_clicked(self, widget, event, link):
        t = threading.Thread(target=self.weblink, args=(link,))
        t.daemon = True
        t.start()

    def _on_info_clicked(self, widget, event):
        window_list = Wnck.Screen.get_default().get_windows()
        state = False
        for win in window_list:
            if "Information" in win.get_name():
                state = True
        if not state:
            w = conflicts.Conflicts()
            w.show_all()

    def weblink(self, link):
        # webbrowser.open_new_tab(link)
        try:
            # use xdg-open to use the default browser to open the weblink
            subprocess.Popen(
                ["xdg-open", link],
                shell=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
        except Exception as e:
            print("Exception in opening weblink(): %s" % e)

    def is_connected(self):
        try:
            host = socket.gethostbyname(REMOTE_SERVER)
            s = socket.create_connection((host, 80), 2)
            s.close()

            return True
        except:  # noqa
            pass

        return False

    def tooltip_callback(self, widget, x, y, keyboard_mode, tooltip, text):
        tooltip.set_text(text)
        return True

    def internet_notifier(self):
        bb = 0
        dis = 0
        while True:
            if not self.is_connected():
                dis = 1
                GLib.idle_add(self.button_mirrors.set_sensitive, False)
                self.label_notify.set_name("label_style")
                GLib.idle_add(
                    self.label_notify.set_markup,
                    f"<span foreground='yellow'><b>No internet!</b>\n"
                    f"Snigdha OS will <b>not</b> install any additional packages!</span>",
                )  # noqa
            else:
                self.label_notify.set_name("")
                if bb == 0 and dis == 1:
                    GLib.idle_add(self.button_mirrors.set_sensitive, True)
                    GLib.idle_add(self.label_notify.set_text, "")
                    bb = 1
            sleep(3)

    def check_package_installed(self, package):
        try:
            subprocess.check_output("pacman -Qi " + package, shell=True, stderr=subprocess.STDOUT)
            return True
        except subprocess.CalledProcessError:
            return False
        
    def mirror_update(self):
        GLib.idle_add(
            self.label_notify.set_markup,
            f"<span foreground='cyan'>Updating Arch Mirrorlist\n"
            f"This may take some time, please wait...</span>",
        )  # noqa
        GLib.idle_add(self.button_mirrors.set_sensitive, False)
        subprocess.run(
            [
                "pkexec",
                "/usr/bin/rate-mirrors",
                "--concurrency",
                "40",
                "--disable-comments",
                "--allow-root",
                "--save",
                "/etc/pacman.d/mirrorlist",
                "arch",
            ],
            shell=False,
        )
        print("Update mirrors completed")
        GLib.idle_add(
            self.label_notify.set_markup,
            f"<span foreground='cyan'>Updating Chaotic Aur Mirrorlist\n"
            f"This may take some time, please wait...</span>",
        )  # noqa
        GLib.idle_add(self.button_mirrors.set_sensitive, False)
        subprocess.run(
            [
                "pkexec",
                "/usr/bin/rate-mirrors",
                "--concurrency",
                "40",
                "--disable-comments",
                "--allow-root",
                "--save",
                "/etc/pacman.d/chaotic-mirrorlist",
                "chaotic-aur",
            ],
            shell=False,
        )
        print("Update mirrors completed")
        GLib.idle_add(self.label_notify.set_markup, "<b>Mirrorlist updated</b>")
        GLib.idle_add(self.button_mirrors.set_sensitive, True)

    def MessageBox(self, title, message):
        md = Gtk.MessageDialog(
            parent=self,
            flags=0,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            text=title,
        )
        md.format_secondary_markup(message)
        md.run()
        md.destroy()

if __name__ == "__main__":
    w = Main()
    w.connect("delete-event", Gtk.main_quit)
    w.show_all()
    Gtk.main()

# Author: Erik Dubois [Arcolinux]
# Adopted for Snigdha OS

import os
import getpass
from os.path import expanduser
from ui.Stack import Stack
from ui.StackSwitcher import StackSwitcher

debug = False
# debug = True

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
home = expanduser("~")
username = getpass.getuser()

app_discord = "#"
app_website = "https://snigdhaos.org/"
app_forums = "https://forum.snigdhaos.org/"
app_facebook = "https://facebook.com/Snigdha-OS/"
app_twitter = "https://twitter.com/Snigdha-OS/"

if debug:
    user = username
else:
    user = "whoami"

Settings = home + "/.config/snigdhaos-welcome/settings.conf"
Skel_Settings = "/etc/skel/.config/snigdhaos-welcome/settings.conf"
dot_desktop = "/usr/share/applications/snigdhaos-welcome.desktop"
autostart = home + "/.config/autostart/snigdhaos-welcome.desktop"


def GUI(self, Gtk, GdkPixbuf):
    # initialize main vbox
    self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
    self.vbox.set_halign(Gtk.Align.CENTER)
    self.add(self.vbox)

    headerbar = Gtk.HeaderBar()
    headerbar.set_title("Snigdha OS Welcome - Optimized for Performance and Customization")
    headerbar.set_show_close_button(True)

    self.set_titlebar(headerbar)

    # x11 shows icon inside headerbar twice, only set icon when on wayland
    if self.session is not None:
        if self.session == "wayland":
            headerbar.pack_start(
                Gtk.Image().new_from_pixbuf(
                    GdkPixbuf.Pixbuf().new_from_file_at_size(
                        os.path.join(base_dir, "images/snigdhaos-welcome-small.png"), 16, 16
                    )
                )
            )

    # initialize the stack
    stack = Stack(transition_type="CROSSFADE")

    # initialize the stack-switcher
    stack_switcher = StackSwitcher(stack)

    vbox_stack_sidebar = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=25)
    vbox_stack_sidebar.set_name("stack_box")

    vbox_stack_sidebar.add(stack_switcher)
    vbox_stack_sidebar.add(stack)

    self.vbox.add(vbox_stack_sidebar)

    # vbox to contain all the installation controls
    vbox_install_stack = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vbox_install_stack.set_halign(Gtk.Align.CENTER)

    hbox_install_buttons = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox_install_buttons.set_halign(Gtk.Align.CENTER)

    vbox_quit = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vbox_quit.set_halign(Gtk.Align.CENTER)

    hbox_util_buttons = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox_util_buttons.set_halign(Gtk.Align.CENTER)

    vbox_welcome_title = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
    vbox_welcome_title.set_halign(Gtk.Align.CENTER)

    vbox_welcome_message = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
    vbox_welcome_message.set_halign(Gtk.Align.CENTER)

    vbox_install_stack.pack_start(vbox_welcome_title, False, False, 0)
    vbox_install_stack.pack_start(vbox_welcome_message, False, False, 0)
    vbox_install_stack.pack_start(hbox_install_buttons, False, False, 0)
    # vbox_install_stack.pack_start(hbox_second_row_buttons, False, False, 0)
    vbox_install_stack.pack_start(hbox_util_buttons, False, False, 0)
    vbox_install_stack.pack_start(vbox_quit, False, False, 0)

    # vbox to contain all the information text
    vbox_info_stack = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
    vbox_info_stack.set_halign(Gtk.Align.CENTER)

    vbox_info = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
    vbox_info_stack.pack_start(vbox_info, False, False, 0)

    # vbox to contain credits text
    vbox_credits_stack = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
    vbox_credits_stack.set_halign(Gtk.Align.CENTER)

    vbox_credits = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
    vbox_credits_stack.pack_start(vbox_credits, False, False, 0)

    hbox_social_links = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=15)
    hbox_social_links.set_halign(Gtk.Align.CENTER)

    # social links with images
    hbox_social_img = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=25)
    hbox_social_img.set_halign(Gtk.Align.CENTER)

    label_discord = Gtk.Label(xalign=0, yalign=0)
    label_discord.set_markup(
        "<a href='%s' title='%s'>%s</a>" % (app_discord, app_discord, "Discord")
    )

    label_telegram = Gtk.Label(xalign=0, yalign=0)
    label_telegram.set_markup(
        "<a href='%s' title='%s'>%s</a>" % (app_facebook, app_facebook, "Facebook")
    )

    label_youtube = Gtk.Label(xalign=0, yalign=0)
    label_youtube.set_markup(
        "<a href='%s' title='%s'>%s</a>" % (app_twitter, app_twitter, "Twitter")
    )

    label_forums = Gtk.Label(xalign=0, yalign=0)
    label_forums.set_markup(
        "<a href='%s' title='%s'>%s</a>" % (app_forums, app_forums, "Forums")
    )

    # ======================================================================
    #                   SOCIAL LINKS
    # ======================================================================

    # facebook

    fb_event = Gtk.EventBox()
    pbfb = GdkPixbuf.Pixbuf().new_from_file_at_size(
        os.path.join(base_dir, "images/facebook.png"), 64, 64
    )
    fbimage = Gtk.Image().new_from_pixbuf(pbfb)
    fb_event.add(fbimage)
    fb_event.connect(
        "button_press_event",
        self.on_social_clicked,
        "https://www.facebook.com/Snigdha-OS/",
    )

    # twitter
    tw_event = Gtk.EventBox()
    pbtw = GdkPixbuf.Pixbuf().new_from_file_at_size(
        os.path.join(base_dir, "images/twitter.png"), 64, 64
    )
    twimage = Gtk.Image().new_from_pixbuf(pbtw)
    tw_event.add(twimage)
    tw_event.connect(
        "button_press_event",
        self.on_social_clicked,
        "https://twitter.com/snigdhaos",
    )

    # mewe
    mew_event = Gtk.EventBox()
    pbmew = GdkPixbuf.Pixbuf().new_from_file_at_size(
        os.path.join(base_dir, "images/github.png"), 64, 64
    )
    mewimage = Gtk.Image().new_from_pixbuf(pbmew)
    mew_event.add(mewimage)
    mew_event.connect(
        "button_press_event",
        self.on_social_clicked,
        "https://github.com/Snigdha-OS",
    )

    label_social_padding = Gtk.Label(xalign=0, yalign=0)
    label_social_padding.set_text("     ")

    # tooltips
    fb_event.set_property("has-tooltip", True)
    tw_event.set_property("has-tooltip", True)
    mew_event.set_property("has-tooltip", True)

    fb_event.connect("query-tooltip", self.tooltip_callback, "Facebook")
    tw_event.connect("query-tooltip", self.tooltip_callback, "Twitter")
    mew_event.connect("query-tooltip", self.tooltip_callback, "Github")

    hbox_social_img.add(fb_event)
    hbox_social_img.add(tw_event)
    hbox_social_img.add(mew_event)

    label_info_header1 = Gtk.Label(xalign=0, yalign=0)
    label_info_header1.set_name("label_style")
    label_info_header1.set_justify(Gtk.Justification.CENTER)
    label_info_header1.set_halign(Gtk.Align.CENTER)

    label_info_header2 = Gtk.Label(xalign=0.5, yalign=0.5)
    label_info_header2.set_name("label_style")
    label_info_header2.set_justify(Gtk.Justification.CENTER)
    label_info_header2.set_halign(Gtk.Align.CENTER)
    label_info_header2.set_markup("<b>You have the freedom of choice</b>")

    label_info2 = Gtk.Label(xalign=0.5, yalign=0.5)
    label_info2.set_justify(Gtk.Justification.CENTER)

    if debug is True:
        label_info_header1.set_markup("<b>Snigdha OS - Arctic Installer</b>")

        desc = (
            f"Clean You Computer With GParted before installing Snigdha OS.\n"
            f"During the <b>Online Installation</b> many options will be open to you.\n\n"
            f"<b>Offline Installation</b> does not require internet connection.\n"
            f"<b>Online installation</b> (Recommended) requires a working internet connection"
        )

        desc2 = (
            f"Welcome to A Blazing Fast and Optimized Operating System.\n"
            f"Snigdha OS\n"
            f"Follow our facebook Page to get update about latest news and upcoming features.\n"
            f"Also you can follow us on github and suggest more features.\n"
            f"Get Registered for beta testing[Beta Image may be unstable.]\n\n"
        )

        label_info2.set_markup(desc2)

    else:
        label_info_header1.set_markup("<b>Welcome to Snigdha OS - Arctic</b>")
        desc = (
            f"Welcome to A Blazing Fast and Optimized Operating System.\n"
            f"Snigdha OS\n"
            f"Follow our facebook Page to get update about latest news and upcoming features.\n"
            f"Also you can follow us on github and suggest more features.\n"
            f"Get Registered for beta testing[Beta Image may be unstable.]\n\n"
        )

    label_info = Gtk.Label(xalign=0, yalign=0)
    label_info.set_markup(desc)
    label_info.set_justify(Gtk.Justification.CENTER)

    vbox_info.pack_start(label_info_header1, False, False, 0)
    vbox_info.pack_start(label_info, False, False, 0)
    if len(label_info2.get_text()) > 0:
        vbox_info.pack_start(label_info_header2, False, False, 0)
        vbox_info.pack_start(label_info2, False, False, 0)
    vbox_info.pack_start(hbox_social_links, False, False, 0)
    vbox_info.pack_start(hbox_social_img, False, False, 0)

    stack.add_titled(vbox_install_stack, "Install Snigdha OS", "Install Snigdha OS")
    autostart = eval(self.load_settings())
    hbox_notify = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    hbox_notify.set_halign(Gtk.Align.CENTER)
    hbox_footer_buttons = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    self.label_notify = Gtk.Label(xalign=0.5, yalign=0.5)
    self.label_notify.set_justify(Gtk.Justification.CENTER)
    hbox_notify.pack_end(self.label_notify, False, False, 0)
    pixbuf = GdkPixbuf.Pixbuf().new_from_file_at_size(
        os.path.join(base_dir, "images/snigdhaos-welcome.png"), 300, 300
    )
    image = Gtk.Image().new_from_pixbuf(pixbuf)

    label_welcome_message = Gtk.Label(xalign=0, yalign=0)
    label_welcome_message.set_name("label_style_eshan")
    if username == user:
        label_welcome_message.set_text(
            "Use Offline Installation in case Online Installation fails!"
        )
    else:
        label_welcome_message.set_text(
            "The options below will help you get started on Snigdha OS\nIf You are having any problem, Feel free to ask on our forum!"
        )
    vbox_welcome_title.pack_start(image, True, False, 0)
    vbox_welcome_message.pack_start(label_welcome_message, True, False, 0)
    button_gparted = Gtk.Button(label="")
    button_gparted_label = button_gparted.get_child()
    button_gparted_label.set_markup("Run GParted")
    button_gparted.connect("clicked", self.on_gp_clicked)
    button_gparted.set_size_request(100, 50)
    button_gparted.set_property("has-tooltip", True)
    button_gparted.connect("query-tooltip", self.tooltip_callback, "Launch GParted")

    self.button_easy_install = Gtk.Button(label="")
    button_easy_install_label = self.button_easy_install.get_child()
    button_easy_install_label.set_markup(
        "<span size='large'>Offline Installation</span>"
    )
    self.button_easy_install.connect("clicked", self.on_easy_install_clicked)
    self.button_easy_install.set_size_request(300, 60)
    self.button_easy_install.set_property("has-tooltip", True)
    self.button_easy_install.connect(
        "query-tooltip", self.tooltip_callback, "No internet connection required"
    )
    self.button_adv_install = Gtk.Button(label="")
    button_adv_label = self.button_adv_install.get_child()
    button_adv_label.set_markup(
        "<span size='large'>Online Installation</span>"
    )
    self.button_adv_install.connect("clicked", self.on_adv_install_clicked)
    self.button_adv_install.set_size_request(300, 60)
    self.button_adv_install.set_property("has-tooltip", True)
    self.button_adv_install.connect(
        "query-tooltip", self.tooltip_callback, "Internet connection required!"
    )
    self.button_mirrors = Gtk.Button(label="")
    button_mirrors_label = self.button_mirrors.get_child()
    button_mirrors_label.set_markup("Update Mirrors")
    self.button_mirrors.connect("clicked", self.on_mirror_clicked)
    self.button_mirrors.set_size_request(100, 50)
    self.button_mirrors.set_property("has-tooltip", True)
    self.button_mirrors.connect(
        "query-tooltip", self.tooltip_callback, "Update Mirrorlist"
    )
    button_resolution = Gtk.Button(label="Fix Screen Resolution")
    button_resolution.set_size_request(100, 50)
    button_resolution.set_property("has-tooltip", True)
    button_resolution.connect("query-tooltip", self.tooltip_callback, "Launch Arandr")
    button_resolution.connect("clicked", self.on_buttonarandr_clicked)

    if username == user:
        hbox_util_buttons.pack_start(self.button_mirrors, False, True, 0)
        hbox_util_buttons.pack_start(button_gparted, False, True, 0)
        if self.session == "x11":
            hbox_util_buttons.pack_start(button_resolution, False, True, 0)
        hbox_install_buttons.pack_start(self.button_easy_install, True, True, 0)
        hbox_install_buttons.pack_end(self.button_adv_install, True, True, 0)

    else:

        self.button_mirrors.get_child().set_markup("Update Mirrors")

        button_resolution.get_child().set_markup("<b>Screen Resolution</b>")

        hbox_install_buttons.pack_start(self.button_mirrors, False, True, 0)

        if self.session == "x11":
            hbox_install_buttons.pack_start(button_resolution, False, True, 0)

    label_creds = Gtk.Label(xalign=0)
    label_creds.set_markup("User: whoami | Pass: No Password")
    label_creds.set_name("label_style")

    hbox_user = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)

    hbox_user.pack_start(label_creds, False, False, 0)

    label_credits_title = Gtk.Label(xalign=0.5, yalign=0.5)
    label_credits_title.set_name("label_style")
    label_credits_title.set_markup("<b>Meet The Developers</b>")
    label_credits_title.set_halign(Gtk.Align.CENTER)
    label_credits_title.set_justify(Gtk.Justification.CENTER)

    label_credits_support = Gtk.Label(xalign=0.5, yalign=0.5)
    label_credits_support.set_name("label_style")
    label_credits_support.set_markup(
        f"For support or to report any issues use <b><a href='{app_forums}' title='{app_forums}'>Snigdha OS Forum</a></b>"
    )
    label_credits_support.set_halign(Gtk.Align.CENTER)
    label_credits_support.set_justify(Gtk.Justification.CENTER)

    label_credits = Gtk.Label(xalign=0, yalign=0)
    label_credits.set_markup(
        f"Eshanized\n"
        f"Iconized\n"
        f"Snigdha\n"
    )
    label_credits.set_justify(Gtk.Justification.CENTER)
    label_credits.set_line_wrap(True)
    label_credits.set_halign(Gtk.Align.CENTER)

    vbox_credits.pack_start(label_credits_title, False, False, 0)
    vbox_credits.pack_start(label_credits, False, False, 0)
    vbox_credits.pack_start(label_credits_support, False, False, 0)

    button_quit = Gtk.Button(label="")
    button_quit.get_child().set_markup("EXIT")
    button_quit.set_size_request(100, 40)
    button_quit.connect("clicked", Gtk.main_quit)

    vbox_quit.pack_start(button_quit, False, False, 0)

    check = Gtk.CheckButton(label="Autostart")
    check.set_property("has-tooltip", True)
    check.connect(
        "query-tooltip",
        self.tooltip_callback,
        "Untick if you do not want Snigdha OS Welcome to run @startup!",
    )
    check.connect("toggled", self.startup_toggle)
    check.set_active(autostart)

    hbox_footer_buttons.set_halign(Gtk.Align.CENTER)

    if username == user:
        hbox_footer_buttons.pack_start(hbox_user, True, False, 0)

        vbox_auto_start = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        vbox_auto_start.set_halign(Gtk.Align.CENTER)
        vbox_auto_start.pack_end(check, True, False, 0)
        self.vbox.pack_end(vbox_auto_start, True, False, 0)
    else:
        hbox_footer_buttons.pack_end(check, False, False, 0)

    self.vbox.pack_start(hbox_notify, False, False, 5)  # notify label

    self.vbox.pack_end(hbox_footer_buttons, False, False, 0)  # Footer

def on_buttonatt_clicked(self, widget):
    #     app_cmd = [
    #         "/usr/bin/archlinux-tweak-tool",
    #     ]
    #     pacman_cmd = [
    #         "pkexec",
    #         "pacman",
    #         "-Sy",
    #         "archlinux-tweak-tool-git",
    #         "--noconfirm",
    #         "--needed",
    #     ]

    #     dev_package = "archlinux-tweak-tool-dev-git"

    #     if self.check_package_installed(dev_package):
    #         print("[WARN]: %s package found ..removing it" % dev_package)
    #         self.remove_dev_package(
    #             ["pkexec", "pacman", "-Rs", dev_package, "--noconfirm"], dev_package
    #         )

    #     if not self.check_package_installed("archlinux-tweak-tool-git"):
    #         if not os.path.exists(self.pacman_lockfile):
    #             md = MessageDialog(
    #                 title="Install Package",
    #                 message="<b>Arch Linux Tweak Tool</b> is missing, Let Snigdha OS - Welcome install it ?",
    #             )

    #             md.show_all()
    #             md.run()
    #             md.destroy()

    #             if md.response is True:
    #                 threading.Thread(
    #                     target=self.check_package_queue, daemon=True
    #                 ).start()
    #                 threading.Thread(
    #                     target=self.install_package,
    #                     args=(
    #                         app_cmd,
    #                         pacman_cmd,
    #                         "archlinux-tweak-tool-git",
    #                     ),
    #                     daemon=True,
    #                 ).start()
    #         else:
    #             print(
    #                 "[ERROR]: Pacman lockfile found %s, is another pacman process running ?"
    #                 % self.pacman_lockfile
    #             )
    #             md = Gtk.MessageDialog(
    #                 parent=self,
    #                 flags=0,
    #                 message_type=Gtk.MessageType.WARNING,
    #                 buttons=Gtk.ButtonsType.OK,
    #                 text="Pacman lockfile found %s, is another pacman process running ?"
    #                 % self.pacman_lockfile,
    #                 title="Warning",
    #             )
    #             md.run()
    #             md.destroy()
    #     else:
    #         threading.Thread(target=self.run_app, args=(app_cmd,), daemon=True).start()

    # def check_package_installed(self, package):
    #     pacman_cmd = ["pacman", "-Qi", package]
    #     try:
    #         process = subprocess.run(
    #             pacman_cmd,
    #             shell=False,
    #             stdout=subprocess.PIPE,
    #             stderr=subprocess.STDOUT,
    #             universal_newlines=True,
    #         )

    #         if process.returncode == 0:
    #             # package is installed
    #             return True
    #         else:
    #             return False
    #     except subprocess.CalledProcessError as e:
    #         # package is not installed
    #         return False

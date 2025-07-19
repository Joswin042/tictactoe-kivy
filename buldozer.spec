[app]
title = TicTacToe
package.name = tictactoe
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3,kivy
orientation = portrait
fullscreen = 1
android.api = 33
android.minapi = 21
android.ndk = 25b
android.arch = armeabi-v7a
android.permissions = INTERNET

[buildozer]
log_level = 2
warn_on_root = 1

[python]
android.entrypoint = org.kivy.android.PythonActivity
android.logical_filters = *:S python:D

[android]
android.allow_backup = True
